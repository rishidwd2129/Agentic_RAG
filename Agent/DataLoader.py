import asyncio
from langchain.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter
import time
import shutil
from dbHandler import SupabaseDBHandler # Import the pre-initialized db_handler instance
from Embeddings import EmbeddingEncoder
supabasedbhandler : SupabaseDBHandler = SupabaseDBHandler()
embeddingencoder: EmbeddingEncoder  = EmbeddingEncoder()
DATA_PATH = "Data/Markdown_Docs"

def load_txt_doc():
    loader = DirectoryLoader(DATA_PATH, glob = "*.md")
    documents = loader.load()
    return documents

def text_splitter(documents: list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= 1000,
        chunk_overlap=500,
        length_function= len,
        add_start_index = True,
    )
    chunk = splitter.split_documents(documents)
    # print(f"Split.{len(documents)} documents into {len(chunk)} chunks.")
    # document = chunk[1000]
    # print(document.page_content)
    # print(document.metadata)
    return chunk

def loadembeddings(supabase,data):
    supabase.table("document_chunks").insert(data).execute()

def chunkstodb(document_name: str, chunks: list[str])->None:
    # Store document chunks with embeddings in the Supabase.
    supabase = supabasedbhandler.get_client()
    total = len(chunks)
    start_time = time.time()
    for i, chunk in enumerate(chunks):
        print(f"Progress: {i+1}/{total}")
        chunk_content = chunk.page_content
        embedding = embeddingencoder.get_embedding(chunk_content)
        data = {
            "document_name": document_name,
            "content": chunk_content,
            "chunk_number": i,
            "embedding": embedding,
            "meta_data": chunk.metadata,
        }
        loadembeddings(supabase,data)
        # supabase.table("document_chunks").insert(data).execute()

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.4f} seconds")

def chunktoGraph():
    pass
    

if __name__ == "__main__":
    document = load_txt_doc()
    chunks = text_splitter(document)
    # print(type(chunks))
    # for i, chunk in enumerate(chunks):
    #     print(f"chunk : {chunk}\nindex: {i}")
    #     break
    chunkstodb(document_name="document_chunks", chunks=chunks)


