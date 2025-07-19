import os
from supabase import create_client, Client
from dotenv import load_dotenv



class SupabaseDBHandler:
    _instance = None # Class-level variable to hold the single instance

    def __new__(cls):
        if cls._instance is None:
            # Only create a new instnace if one doesn't already exist
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




# load_dotenv()
#
# # Initialize clients
# print(os.getenv("SUPABASE_URL"))
# supabase_url = os.getenv("SUPABASE_URL")
# supabase_key = os.getenv("SUPABASE_KEY")

# supabase: Client = create_client(supabase_url, supabase_key)
