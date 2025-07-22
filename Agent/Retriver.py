import asyncio # You need this for async operations
import time
import shutil
import os
import logging
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from langchain.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Make sure dbHandler.py is accessible
from dbHandler import SupabaseDBHandler 
# Make sure Embeddings.py is accessible (assuming it contains EmbeddingEncoder)
from Embeddings import EmbeddingEncoder 

# Instantiate the DB handler and Embedding encoder globally.
# Their instantiation is synchronous, but their internal *initialization* of clients/models is async.
supabasedbhandler : SupabaseDBHandler = SupabaseDBHandler()
embeddingencoder: EmbeddingEncoder  = EmbeddingEncoder() # Assumes EmbeddingEncoder has an async init method





def simple_similarity_search(
    query_text: str,
    top_k: int = 5,
    similarity_threshold: float = 0.7,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    logger.info(f"Initiating similarity search for query: '{query_text}'")

    # embeddingencoder._async_init() # Ensure encoder is initialized
    query_embedding = embeddingencoder.get_embedding(query_text)
    logger.info("Query embedding generated.")

    supabase_client =  supabasedbhandler.get_client() # Get initialized client
    logger.info("Supabase client obtained.")

    if metadata_filter is None:
        metadata_filter = {}

    try:
        logger.info(f"Calling Supabase RPC function 'match_document_chunks' with params: "
                    f"top_k={top_k}, threshold={similarity_threshold}, filter={metadata_filter}")
        
        response =  supabase_client.rpc(
            'match_document_chunks', 
            {
                'query_embedding': query_embedding,
                'match_count': top_k,
                'match_threshold': similarity_threshold,
                'filter_metadata': metadata_filter
            }
        ).execute()
        
        return response

    except Exception as e:
        logger.error(f"An unexpected error occurred during document retrieval: {e}")
        return []
    
        
if __name__ == "__main__":
    # query = "What is the main theme of the book?"
    # query = "where she went back to the table, half hoping that she might find another key?"
    query = "Training Data Fead to which ML models ?"
    # results = simple_similarity_search(query, top_k=5, similarity_threshold=0.7)
    results = simple_similarity_search(query)
    print(results.data[0]['content'])
    # for result in results:
    #     print(result)
    