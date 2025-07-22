# requirements: pip install "fastapi[all]" uvicorn
# To run: uvicorn api_server:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- 1. IMPORT YOUR RAG MODULES ---
# Make sure these files are in the same directory.
from Retriver import simple_similarity_search
from SystemPrompt import RagTemplate
from Call_llm import LLM_Pipeline

# --- 2. DEFINE DATA MODELS (with Pydantic) ---
# FastAPI uses Pydantic models for request and response validation,
# serialization, and documentation. This ensures the data flowing
# in and out of your API is exactly what you expect.
class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    answer: str

# --- 3. INITIALIZE MODELS (ONE TIME) ---
# This logic remains the same. The LLM is loaded once on startup.
print("Initializing LLM Pipeline... This may take a moment.")
LLM = LLM_Pipeline(model_id="Qwen/Qwen2-1.5B-Instruct")
print("LLM Pipeline Initialized. Server is ready.")

# Initialize the FastAPI application
app = FastAPI()


# --- 4. WRAP YOUR PIPELINE LOGIC IN A FUNCTION ---
# This function is identical to the one in the Flask version.
# Its core logic is framework-agnostic.
def run_rag_pipeline(user_prompt: str) -> str:
    """
    This function encapsulates the core logic from your main.py.
    It takes a user prompt, retrieves context, and generates an answer.
    """
    try:
        print(f"Received prompt: '{user_prompt}'")

        # 1. Retrieve context
        print("Step 1: Retrieving context...")
        Context_Response = simple_similarity_search(user_prompt)
        
        # 2. Extract context text
        context = Context_Response.data[0]['content'] if Context_Response and Context_Response.data else "No relevant context found."
        print("Step 2: Context extracted.")
        
        # 3. Create the final prompt
        input_prompt = RagTemplate(query=user_prompt, context=context)
        print("Step 3: Prompt template created.")

        # 4. Call the LLM
        print("Step 4: Calling the LLM...")
        llm_response_raw = LLM.call_llm(input_prompt)
        
        # 5. Extract the final answer
        final_answer = llm_response_raw[0]['generated_text'][1]['content']
        print("Step 5: Answer generated successfully.")
        
        return final_answer

    except Exception as e:
        print(f"An error occurred in the RAG pipeline: {e}")
        # In FastAPI, it's common to raise an HTTPException for errors.
        # However, to keep client compatibility, we can also return a string.
        # For a more robust API, you might handle this differently.
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing the request.")


# --- 5. CREATE THE API ENDPOINT ---
# The decorator changes to `@app.post`. We define the response model
# for automatic documentation and serialization.
@app.post("/api/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Handles incoming queries from the client application.
    - FastAPI automatically validates the incoming request against `QueryRequest`.
    - The `async` keyword allows for concurrent handling of requests.
    """
    try:
        answer = run_rag_pipeline(request.prompt)
        return QueryResponse(answer=answer)
    except HTTPException as http_exc:
        # Re-raise the exception from the pipeline to be handled by FastAPI
        raise http_exc
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")


# --- How to Run ---
# 1. Save this file as `api_server.py`.
# 2. Install FastAPI and Uvicorn: `pip install "fastapi[all]"`
# 3. In your terminal, run the server: `uvicorn api_server:app --reload`

