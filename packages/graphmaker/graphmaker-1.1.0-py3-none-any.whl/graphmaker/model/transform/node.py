from enum import Enum
from typing import Tuple


class NodeIndexType(Enum):
    TEXT = "text"
    RANGE = "range"


class Node:
    def __init__(
        self,
        label: str,
        new_attributes: list[str],
        existing_attributes: list[str] = [],
        *,
        engine,
        uniques: list[Tuple[str, NodeIndexType]] = [],
        indexes: list[Tuple[str, NodeIndexType]] = [],
        ignore_index=False,
    ):
        # self.label = f"`{label}`"
        # self.attributes = [f"`{a}`" for a in attributes]
        # self.uniques = [(f"`{a}`", b) for a, b in uniques]
        # self.indexes = [(f"`{a}`", b) for a, b in indexes]
        self.label = label
        self.new_attributes = new_attributes
        self.existing_attributes = existing_attributes
        self.uniques = uniques
        self.indexes = indexes + uniques
        if len(self.indexes) == 0:
            self.indexes = [(x, NodeIndexType.TEXT) for x in self.new_attributes]
        self.ignore_index = ignore_index
        self.engine = engine

    def create_index(self):
        if self.ignore_index:
            return []
        q = []
        
        if self.engine == "neo4j":
            print("TODO")
        else:
            q.append(f"CREATE INDEX ON :{self.label}")
        for key in self.uniques:
            if self.engine == "neo4j":
                q.append(f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{self.label}) REQUIRE n.{key[0]} IS UNIQUE")
            else:
                q.append(f"CREATE CONSTRAINT ON (n:{self.label}) ASSERT n.{key[0]} IS UNIQUE")
        for key in self.indexes:
            if key[1] == "text":
                if self.engine == "neo4j":
                    q.append(f"CREATE TEXT INDEX IF NOT EXISTS FOR (n:{self.label}) ON (n.{key[0]})")
                else:
                    q.append(f"CREATE INDEX ON :{self.label}({key[0]})")
            else:
                if self.engine == "neo4j":
                    q.append(f"CREATE INDEX IF NOT EXISTS FOR (n:{self.label}) ON (n.{key[0]})")
                else:
                    q.append(f"CREATE INDEX ON :{self.label}({key[0]})")
        return q

    def create(self, engine="neo4j", periodic=False, batch_size=1000) -> str:
        attr_string = ", ".join([f"n.`{att}` = row.`{att}`" for att in self.new_attributes])
        key_string = ", ".join([f"{key[0]}: row.{key[0]}" for key in self.indexes])
        query = f"""
        UNWIND $batch AS row
        CREATE (n:{self.label} {{{key_string}}})
        SET {attr_string}
        """
        if not periodic:
            return query
        elif engine == "neo4j":
            return f"""
            CALL apoc.periodic.iterate(
                '{query}',
                {{batchSize: {batch_size}, parallel: true}}
            )
        """
        else:
            return f"""
            CALL periodic.iterate(
                '{query}',
                {{batch_size: {batch_size}}}
            )
        """

    def create_or_merge_query(self, engine="neo4j", periodic=False, batch_size=1000) -> str:
        attr_string = ", ".join([f"n.`{att}` = row.`{att}`" for att in self.new_attributes])
        match_string = ", ".join([f"{att}: row.{att}" for att in self.existing_attributes])
        key_string = ", ".join([f"{key[0]}: row.{key[0]}" for key in self.indexes])
        if key_string == "":
            return self.create()
        q = f"""
        UNWIND $batch AS row
        MERGE (n:{self.label} {{{key_string}}})
        ON CREATE SET {attr_string}
        ON MATCH SET {attr_string}
        """ if match_string == "" else f"""
        UNWIND $batch AS row
        MATCH (n:{self.label} {{{match_string}}})
        SET {attr_string}
        """
        if not periodic:
            return q
        elif engine == "neo4j":
            return f"""
            CALL apoc.periodic.iterate(
                '{q}',
                {{batchSize: {batch_size}, parallel: true}}
            )
        """
        else:
            return f"""
            CALL periodic.iterate(
                '{q}',
                {{batch_size: {batch_size}}}
            )
        """
