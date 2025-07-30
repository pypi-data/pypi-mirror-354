class Edge:
    def __init__(
        self,
        label,
        source_label,
        target_label,
        attributes,
        keys,
        source_attribute_mapping,
        target_attribute_mapping,
    ):
        self.label = f"`{label}`"
        self.source_label = source_label
        self.target_label = target_label
        self.attributes = attributes
        self.keys = keys
        self.source_attribute_mapping = source_attribute_mapping
        self.target_attribute_mapping = target_attribute_mapping

    def create_index(self):
        return [f"CREATE INDEX IF NOT EXISTS FOR ()-[r:{self.label}]-() ON ({', '.join(f'r.{key}' for key in self.keys)})"]

    def create_or_merge_query(self, engine="neo4j", periodic=False, batch_size=1000) -> str:
        if self.attributes:
            edge_attr_string = ", ".join([f"r.{att} = row.{att}" for att in self.attributes])
            set_clause = f"ON CREATE SET {edge_attr_string}\n ON MATCH SET {edge_attr_string}"
        else:
            set_clause = ""

        source_attr_string = ", ".join([f"{attr} = row.{attr}" for attr in self.source_attribute_mapping])
        target_attr_string = ", ".join([f"{attr} = row.{attr}" for attr in self.target_attribute_mapping])
        query = f"""
            UNWIND $batch AS row
            MATCH (a:{self.source_label} {{{source_attr_string}}}),
            (b:{self.target_label} {{{target_attr_string}}})
            MERGE (a)-[r:{self.label} {{{', '.join(f'r.{key} = row.{key}' for key in self.keys)}}}]->(b)
            {set_clause}
            """
        if not periodic:
            return query
        elif engine == "neo4j":
            return f"""
            CALL apoc.periodic.iterate(
                '{query}',
                {{batchSize: {batch_size}, parallel: false}}
            )
        """
        else:
            return f"""
            CALL periodic.iterate(
                '{query}',
                {{batch_size: {batch_size}}}
            )
            YIELD success, number_of_executed_batches
            RETURN success, number_of_executed_batches;
        """
