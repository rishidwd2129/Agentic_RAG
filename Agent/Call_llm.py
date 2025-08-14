import torch
from transformers import pipeline


class LLM_Pipeline:
    def __init__(self, model_id: str = "Qwen/Qwen2-1.5B-Instruct"):
        """
        The CONSTRUCTOR: This is called ONLY ONCE when you create the object.
        """
        print("Initializing pipeline and loading the model...")
        # The model is loaded here, just one time.
        self.pipe = pipeline(
            "text-generation",
            model=model_id,
            # ... other parameters
            
        )
        print("Model loaded successfully!")
        
    
    def call_llm(self, messages:list, max_output:int = 250):
    # 2. Define your prompt using a chat format
        # messages = [
        #     {"role": "user", "content": prompt},
        # ]

        # 3. Generate the response
        # The pipeline automatically applies the correct chat template for the model.
        outputs = self.pipe(
            messages,
            max_new_tokens=max_output,  # The maximum number of tokens to generate
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )
        return outputs
if __name__ == "__main__":
    llm = LLM_Pipeline(model_id="Qwen/Qwen2-1.5B-Instruct")

    prompt = "What is the capital of France?"
    response = llm.call_llm(prompt)
    print(response)  # This will print the response from the LLM
    # 4. Print the generated text
    # The response is located in the 'generated_text' of the output.
    # We access the last message, which is the assistant's reply.
    # print("\n--- Model Response ---")
    # print(outputs[0]["generated_text"][-1]["content"])


