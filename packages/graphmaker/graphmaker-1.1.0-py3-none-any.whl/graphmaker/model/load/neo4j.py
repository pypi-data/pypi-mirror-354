import pandas as pd
from tqdm import tqdm
from graphmaker.model.extract import DataProvider
import time
import json
from graphmaker.model.transform import Node, Edge
from neo4j import GraphDatabase
import hashlib


class Neo4jLoader:
    def __init__(self, uri, user, password, engine, batch_size=1000):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.user = user
        self.engine = engine
        self.batch_size = batch_size

    def connect(self, database_name, create=True):
        self.database_name = database_name
        if database_name != "memgraph" and create and database_name != "neo4j" and self.user == "neo4j":
            with self.driver.session(database="neo4j") as session:
                while True:
                    try:
                        session.run(f"CREATE DATABASE {database_name} IF NOT EXISTS WAIT")
                        break
                    except Exception as e:
                        print(e)
                        for i in tqdm(range(20), desc="Sleeping 20s before reconnecting"):
                            time.sleep(1)
                        print("Reconnecting to the database in connection...")
                        self.connect(self.database_name)

        self.session = self.driver.session(database=database_name)

    def delete_database(self, database_name):
        with self.driver.session(database="neo4j") as session:
            session.run(f"DROP DATABASE {database_name} IF EXISTS WAIT")

    def close(self):
        self.session.close()
        self.driver.close()
        print("Neo4j Connection closed.")

    def delete_label(self, label, use_apoc=True, completely=False):
        print(f"Deleting label {label}...")
        if use_apoc:
            self.session.run(
                f"CALL apoc.periodic.iterate('MATCH (n:{label}) RETURN n', 'DETACH DELETE n', {{batchSize:10000}})")
        else:
            query = f"""
            MATCH (n:{label})
            WITH n LIMIT 10000
            DETACH DELETE n
            RETURN count(n) as deleted
            """
            while True:
                result = self.session.run(query)
                if result.single()["deleted"] == 0:
                    break

        if completely:
            if self.engine == "neo4j":
                cnames = self.run_query("SHOW CONSTRAINTS YIELD name as cname return *").data()
                for cname in cnames:
                    if label in cname["cname"]:
                        print("dropping neo4j constraint", cname)
                        self.run_query(f"DROP CONSTRAINT {cname['cname']} IF EXISTS")
                inames = self.run_query("SHOW INDEX YIELD name as iname return *").data()
                for iname in inames:
                    if label in iname["iname"]:
                        print("dropping neo4j index", iname)
                        self.run_query(f"DROP INDEX {iname['iname']} IF EXISTS")
            else:
                schema = json.loads(self.run_query("SHOW SCHEMA INFO").data()[0]["schema"])
                for constraint in schema["node_constraints"]:
                    if label in constraint['labels'][0]:
                        print("dropping memgraph constraint", constraint)
                        self.run_query(
                            f"DROP CONSTRAINT ON (n:{constraint['labels'][0]}) ASSERT EXISTS (n.{constraint['properties'][0]})")
                for index in schema["node_indexes"]:
                    if label in index['labels'][0]:
                        print("dropping memgraph index", index)
                        if len(index['properties']) > 0:
                            self.run_query(f"DROP INDEX ON :{index['labels'][0]}({index['properties'][0]})")
                        self.run_query(f"DROP INDEX ON :{index['labels'][0]}")
        print(f"Label {label} deleted.")

    def clear_db(self, completely=False, use_apoc=False, labels=None):
        assert (completely and labels is None) or not completely
        if not labels:
            labels = self.run_query("MATCH (n) RETURN DISTINCT labels(n) AS labels").data()
            if not labels or len(labels) == 0:
                print("No labels found in the database.")
                return
            labels = [label["labels"][0] for label in labels if label["labels"] and len(label["labels"]) > 0]
        print("Clearing database...")
        if use_apoc:
            self.run_query("CALL apoc.periodic.iterate('MATCH (n) RETURN n', 'DETACH DELETE n', {batchSize:10000})")
        else:
            for label_name in labels:
                print("deleting", label_name)
                query = f"""
                MATCH (n:{label_name})
                WITH n LIMIT 10000
                DETACH DELETE n
                RETURN count(n) as deleted
                """
                while True:
                    result = self.run_query(query)
                    if result.single()["deleted"] == 0:
                        break

        if completely:
            if self.engine == "neo4j":
                cnames = self.run_query("SHOW CONSTRAINTS YIELD name as cname return *").data()
                for cname in cnames:
                    self.run_query(f"DROP CONSTRAINT {cname['cname']} IF EXISTS")
                inames = self.run_query("SHOW INDEX YIELD name as iname return *").data()
                for iname in inames:
                    print("dropping index", iname)
                    self.run_query(f"DROP INDEX {iname['iname']} IF EXISTS")
            else:
                schema = json.loads(self.run_query("SHOW SCHEMA INFO").data()[0]["schema"])
                for constraint in schema["node_constraints"]:
                    self.run_query(
                        f"DROP CONSTRAINT ON (n:{constraint['labels'][0]}) ASSERT EXISTS (n.{constraint['properties'][0]})")
                for index in schema["node_indexes"]:
                    print("dropping index", index['labels'][0], index['properties'])
                    if len(index['properties']) > 0:
                        self.run_query(f"DROP INDEX ON :{index['labels'][0]}({index['properties'][0]})")
                    self.run_query(f"DROP INDEX ON :{index['labels'][0]}")
        # self.run_query("CALL apoc.schema.assert({},{},true) YIELD label, key RETURN *")
        print("Database cleared.")

    def run_query(
        self,
        query,
        parameters=None,
        **kwargs,
    ):
        try:
            ret = self.session.run(query, parameters, **kwargs)
            return ret
        except Exception as e:
            # print(query)
            # print(parameters)
            print(e)
            for i in tqdm(range(20), desc="Sleeping 20s before reconnecting"):
                time.sleep(1)
            print("Reconnecting to the database to rerun query...")
            self.connect(self.database_name)
            return self.run_query(query, parameters, **kwargs)

    def get_count(self):
        with self.session.begin_transaction() as transaction:
            query = "MATCH (n) RETURN count(n) AS count"
            result = transaction.run(query).single()
            return result["count"]

    def connect_nodes(self, rows, source, target, label, attributes, batch_size=None, periodic=False):
        def number2Str(num):
            # Use a short unique hash for each number
            return "col_" + hashlib.md5(str(num).encode()).hexdigest()[:8]

        # Fix: map for all columns in the row, not just attributes
        # number2StrMap = {i: number2Str(i) for i in range(len(source["attributes"]) + len(target["attributes"]) + len(attributes))}
        number2StrMap = {i: number2Str(i) for i in range(len(rows[0]))}

        source_attr_string = ", ".join([f"{attr[0]}: row.{number2StrMap[attr[1]]}" for attr in source["attributes"]])
        target_attr_string = ", ".join([f"{attr[0]}: row.{number2StrMap[attr[1]]}" for attr in target["attributes"]])
        edge_attr_string = ", ".join([f"r.{attr[0]} = row.{number2StrMap[attr[1]]}" for attr in attributes])

        columns = [f"{number2StrMap[i]}" for i in range(len(rows[0]))]
        batched_rows = [dict(zip(columns, row)) for i, row in enumerate(rows)]

        # Use instance batch_size if method batch_size is None
        if batch_size is None:
            batch_size = self.batch_size

        # If batch_size is not provided, process all rows as one batch.
        
        if batch_size == -1:
            for row in tqdm(batched_rows, desc=f"Connecting {source['label']} and {target['label']} (row by row)"):
                # Dynamically build attribute strings for non-null values
                source_attr_parts = []
                source_where_parts = []
                for attr in source["attributes"]:
                    key, idx = attr
                    val = row[columns[idx]]
                    # Modified: handle None or empty string for WHERE clause
                    if val is None or (isinstance(val, str) and val == ""):
                        source_where_parts.append(f"(a.{key} IS NULL OR a.{key} = '' OR b.{key} = 'nan')")
                    elif pd.notna(val):
                        source_attr_parts.append(f"{key}: {json.dumps(val)}")
                        source_where_parts.append(f"a.{key} = {json.dumps(val)}")
                source_attr_string_row = ", ".join(source_attr_parts)
                source_where_string_row = " AND ".join(source_where_parts)

                target_attr_parts = []
                target_where_parts = []
                for attr in target["attributes"]:
                    key, idx = attr
                    val = row[columns[idx]]
                    # Modified: handle None or empty string for WHERE clause
                    if val is None or (isinstance(val, str) and val == ""):
                        target_where_parts.append(f"(b.{key} IS NULL OR b.{key} = '' OR b.{key} = 'nan')")
                    elif pd.notna(val):
                        target_attr_parts.append(f"{key}: {json.dumps(val)}")
                        target_where_parts.append(f"b.{key} = {json.dumps(val)}")
                target_attr_string_row = ", ".join(target_attr_parts)
                target_where_string_row = " AND ".join(target_where_parts)

                # Add error if either is empty
                if not source_where_string_row or not target_where_string_row:
                    raise ValueError("Source or target WHERE clause is empty. This indicates missing or invalid attributes for source or target node.")

                edge_attr_parts = []
                for attr in attributes:
                    key, idx = attr
                    val = row[columns[idx]]
                    if val is not None and pd.notna(val):
                        edge_attr_parts.append(f"r.{key} = {json.dumps(val)}")
                edge_attr_string_row = ", ".join(edge_attr_parts) if edge_attr_parts else ""

                query = f"""MATCH (a:{source["label"]}), (b:{target["label"]}) WHERE {source_where_string_row} AND {target_where_string_row} MERGE (a)-[r:{label}]->(b)"""
                if edge_attr_string_row:
                    query += f" ON CREATE SET {edge_attr_string_row} ON MATCH SET {edge_attr_string_row}"

                print((query))
                self.run_query(query)
        elif batch_size is None or periodic is False:
            query = f"""
                UNWIND $batch AS row
                MATCH (a:{source["label"]} {{{source_attr_string}}}),
                (b:{target["label"]} {{{target_attr_string}}})
                MERGE (a)-[r:{label}]->(b)
                ON CREATE SET {edge_attr_string}
                ON MATCH SET {edge_attr_string}
                """
            if batch_size is None or periodic is True:
                batch_size = len(batched_rows)
            total_batches = (len(batched_rows) + batch_size - 1) // batch_size
            for i in tqdm(range(total_batches), desc=f"Connecting {source['label']} and {target['label']}"):
                batch = batched_rows[i * batch_size: (i + 1) * batch_size]
                self.run_query(query, {"batch": batch})
        elif periodic and self.engine == "neo4j":
            print(f"Connecting {source['label']} and {target['label']} with apoc.periodic.iterate...")
            query = f"""
                CALL apoc.periodic.iterate(
                  'UNWIND $batch AS row
                   MATCH (a:{source["label"]} {{{source_attr_string}}}),
                     (b:{target["label"]} {{{target_attr_string}}})',
                  'MERGE (a)-[r:{label}]->(b)
                   ON CREATE SET {edge_attr_string}
                   ON MATCH SET {edge_attr_string}',
                  {{batchSize: {batch_size}}})
                YIELD success, number_of_executed_batches
                RETURN success, number_of_executed_batches
                """
            self.run_query(query, {"batch": batched_rows})
            print(f"Connected {source['label']} and {target['label']}")
        elif periodic and self.engine == "memgraph":
            print(f"Connecting {source['label']} and {target['label']} with periodic.iterate...")
            query = f"""
                CALL periodic.iterate(
                  'UNWIND $batch AS row
                   MATCH (a:{source["label"]} {{{source_attr_string}}}),
                     (b:{target["label"]} {{{target_attr_string}}})
                   MERGE (a)-[r:{label}]->(b)
                   ON CREATE SET {edge_attr_string}
                   ON MATCH SET {edge_attr_string}',
                  {{batch_size: {batch_size}}})
                YIELD success, number_of_executed_batches
                RETURN success, number_of_executed_batches
                """
            self.run_query(query, {"batch": batched_rows})
            print(f"Connected {source['label']} and {target['label']}")
        else:
            raise ValueError("error on periodic")
        
    def connect_nodes_value_counts(self, file: DataProvider, 
                                   source_label: str, 
                                   target_label: str,
                                   label: str, 
                                   source_attributes: list[str] = None, 
                                   target_attributes: list[str] = None, 
                                   attributes: list[tuple[str, int]] = [],
                                   *, 
                                   batch_size=None,
                                   periodic=False):
    
        columns = file.columns()
        if source_attributes is None:
            source_attributes = []
            query = f"MATCH (n:{source_label}) RETURN keys(n) AS attrs LIMIT 1"
            result = self.run_query(query)
            record = result.single().data()
            if record and "attrs" in record:
                source_attributes = [attr for attr in record["attrs"] if attr in columns]
            else:
                raise ValueError(f"No attributes found for label {source_label}")
        if target_attributes is None:
            target_attributes = []
            query = f"MATCH (n:{target_label}) RETURN keys(n) AS attrs LIMIT 1"
            result = self.run_query(query)
            record = result.single().data()
            if record and "attrs" in record:
                target_attributes = [attr for attr in record["attrs"] if attr in columns]
            else:
                raise ValueError(f"No attributes found for label {target_label}")
        if not source_attributes or not target_attributes:
            raise ValueError(f"Source or target attributes are empty for labels {source_label} and {target_label}")

        all_attributes = source_attributes + target_attributes + attributes

        value_counts = file.value_counts_multiple(source_attributes + target_attributes).values
        source_input = dict(label=source_label, attributes=[(attr, i) for i, attr in enumerate(source_attributes)])
        target_input = dict(label=target_label, attributes=[(attr, i + len(source_input["attributes"])) for i, attr in enumerate(target_attributes)])

        attributes_input = [(attr[0], i+len(all_attributes)) for i, attr in enumerate(attributes)]
        attributes_input.append(("Count", len(all_attributes) + len(attributes)))

        # Use instance batch_size if method batch_size is None
        if batch_size is None:
            batch_size = self.batch_size

        return self.connect_nodes(
            value_counts,
            source=source_input,
            target=target_input,
            label=label,
            attributes=attributes_input,
            batch_size=batch_size,
            periodic=periodic,
        )        

    def load(
        self,
        batch: list[list[str, str | int | float]],
        columns: list[str],
        entities: list[Node | Edge],
        *,
        force_create=False,
        batch_size=None,
        periodic=False,
    ):
        rows = batch
        if isinstance(batch[0], dict):
            rows = [[str(value) if not isinstance(value, (int, float)) else value for value in row.values()]
                    for row in rows]

        if len(columns) != len(rows[0]):
            print(len(columns), len(rows[0]))
            print(columns)
            print(rows[0])
            print(list(batch[0].keys()))
            print(set(batch[0].keys()) - set(columns))
            print(set(columns) - set(batch[0].keys()))
            raise ValueError("Number of columns does not match the number of values in the rows.")
        pass

        # Create indexes
        for e in entities:
            for q in e.create_index():
                self.run_query(q)

        # Use instance batch_size if method batch_size is None
        if batch_size is None:
            batch_size = self.batch_size

        # Create or merge nodes
        for e in entities:
            query = e.create_or_merge_query(engine=self.engine, periodic=periodic, batch_size=batch_size) if not force_create else e.create(
                engine=self.engine, periodic=periodic, batch_size=batch_size)
            if periodic or batch_size is None:
                batched_rows = [dict(zip(columns, row)) for row in rows]
                self.run_query(query, {"batch": batched_rows})
            else:
                total_batches = (len(rows) + batch_size - 1) // batch_size
                for i in tqdm(range(total_batches), desc=f"Loading {e.label} node/edge"):
                    batch = rows[i * batch_size: (i + 1) * batch_size]
                    batched_rows = [dict(zip(columns, row)) for row in batch]
                    self.run_query(query, {"batch": batched_rows})

    def load_unique_node(self, file: DataProvider, entity_map: list[dict], merge_uniques=False, *,
                         label=None, force_create=False, ignore_index=False):
        unique_keys = [u["column"] for u in entity_map]
        node_types_uniques = [(u["key"], u.get("type", "text")) for u in entity_map if u.get("unique")]
        node_types_indexes = [(u["key"], u.get("type", "text")) for u in entity_map
                    if u.get("index", True) and (u["key"], u.get("type", "text")) not in node_types_uniques]

        # Separate entity_map entries with new=True
        new_node_keys = [u["key"] for u in entity_map if u.get("new", False) is True]
        base_node_keys = [u["key"] for u in entity_map if not u.get("new", False)]
        all_keys = list(dict.fromkeys([u["key"] for u in entity_map]))

        node_key = label if label is not None else [u["key"] for u in entity_map if u.get("label")][0]
        assert node_key

        # If there are new=True keys, handle them as a separate node
        if new_node_keys and len(new_node_keys) > 0:
            self.load(
                file.unique_multiple(unique_keys).values,
                all_keys,
                [Node(node_key, new_node_keys, base_node_keys, uniques=node_types_uniques, indexes=node_types_indexes,
                      ignore_index=ignore_index, engine=self.engine)],
                force_create=force_create,
            )
        else:
            if merge_uniques:
                self.load(
                    pd.concat([file.unique_multiple([u]).iloc[:, 0] for u in unique_keys]).to_frame().values,
                    base_node_keys,
                    [Node(node_key, base_node_keys, uniques=node_types_uniques, indexes=node_types_indexes, ignore_index=ignore_index, engine=self.engine)],
                    force_create=force_create,
                )
            else:
                self.load(
                    file.unique_multiple(unique_keys).values,
                    base_node_keys,
                    [Node(node_key, base_node_keys, uniques=node_types_uniques, indexes=node_types_indexes, ignore_index=ignore_index, engine=self.engine)],
                    force_create=force_create,
                )
        print(f"Loaded {node_key}")

    def load_row_by_row(self, file: DataProvider, node: Node, batch_size=1000, columns=None):
        columns = file.columns() if columns is None else columns
        total = file.total_rows()
        for batch in tqdm(file.next(), total=(total // batch_size) + 1, desc=f"Importing file row-by-row to node {node.label}"):
            self.load(batch, columns, [node])
