# This is a sample Python script.

# Press ⌃F5 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from Retriver import simple_similarity_search
from SystemPrompt import RagTemplate
from Call_llm import LLM_Pipeline

LLM = LLM_Pipeline(model_id="Qwen/Qwen2-1.5B-Instruct")

def main():
    # input prompt
    while True:
        user_input = input("Enter your prompt (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break 
        
        Context_Response = simple_similarity_search(user_input)
        context = Context_Response.data[0]['content'] if Context_Response.data else "No relevant context found."
        input_prompt = RagTemplate(query=user_input, context=context)
        
        # call the LLM with the input prompt and context
        
        llm_response = LLM.call_llm(input_prompt)
        llm_response = llm_response[0]['generated_text'][1]['content']
        print(f"LLM Response: {llm_response}")
    # place input prompt and context in an prompt template/ system prompt
    # call the LLM with the prompt and context
    # get the response from the LLM


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

