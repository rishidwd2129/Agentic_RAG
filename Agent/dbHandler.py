import os
from supabase import create_client, Client
from neo4j import GraphDatabase
from dotenv import load_dotenv



class SupabaseDBHandler:
    _instance = None # Class-level variable to hold the single instance

    def __new__(cls):
        if cls._instance is None:
            # Only create a new instance if one doesn't already exist
            cls._instance = super(SupabaseDBHandler, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL and Supabase API key must be set in .env file")
        # SupabaseDBHandler.supabase_client =  create_client(supabase_url, supabase_key)
            
        self.supabase: Client = create_client(supabase_url, supabase_key)
        print("Supabase client initialized.")


    def get_client(self):
        """Return the Supabase client instance""" 
       
        return self.supabase 


class Neo4jDBHandler:
    _instance = None # Class-level variable to hold the single instance

    def __init__(self):
        """
        Initializes the database driver.
        Make sure your Neo4j instance is running.
        """
        try:
            self._driver = GraphDatabase.driver(uri = os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")))
            self.driver.verify_connectivity()
            print("Successfully connected to Neo4j.")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            self._driver = None

    def close(self):
        """Closes the database connection."""
        if self._driver is not None:
            self._driver.close()
            print("Neo4j connection closed.")


if __name__ == "__main__":
    db_handler = Neo4jDBHandler()
    


# load_dotenv()
#
# # Initialize clients
# print(os.getenv("SUPABASE_URL"))
# supabase_url = os.getenv("SUPABASE_URL")
# supabase_key = os.getenv("SUPABASE_KEY")

# supabase: Client = create_client(supabase_url, supabase_key)
