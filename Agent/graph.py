import os
import PyPDF2
import json
import spacy
from dbHandler import Neo4jDBHandler
from collections import  Counter


class Neo4jGraphBuilder:
    def __init__(self):
        self.db_handler = Neo4jDBHandler()
    
    def add_constraints(self):
        with self.db_handler.session() as Session:
            Session.run("create constraint if not exist for (p:Person) REQUIRE p.nmae IS UNIQUE")
            Session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (o:Organization) REQUIRE o.name IS UNIQUE")
            # Add other constraints as needed for your entity types
    def build_graph_from_chunks(self, text_chunks: list[str]):
        """Processes a list of list of text chunks to build the graph."""
        print("Building graph form text chunks...")
        
        for i, chunk in enumerate(text_chunks):
            print(f"  - Processing chunk {i+1}/{len(text_chunks)}")
            triples = llm_extract_graph(chunk)
            if triples: 
                self._create_graph_from_triples(triples)
        print("Graph building completed.")


