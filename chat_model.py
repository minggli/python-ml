from typing import List
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

class LlamaChat:
    def __init__(self):
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf",
                                                       use_auth_token=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-2-7b-hf",
            torch_dtype=torch.float16,  # Use float16 for efficiency
            device_map="auto",  # Automatically choose best device (CPU/GPU)
            use_auth_token=True
        )

        # Create HuggingFace pipeline
        pipe = HuggingFacePipeline(
            pipeline=pipeline("text-generation",
                              model=self.model,
                              tokenizer=self.tokenizer,
                              max_new_tokens=10)
        )
        
        # Set up conversation template
        template = """The following is a friendly conversation between a human and an AI assistant.
        
Current conversation:
{history}
Human: {input}
AI Assistant:"""
        
        prompt = PromptTemplate(input_variables=["history", "input"], template=template)
        
        # Create conversation chain with memory
        self.conversation = ConversationChain(
            llm=pipe,
            prompt=prompt,
            memory=ConversationBufferMemory()
        )
    
    def chat(self, message: str) -> str:
        """
        Send a message to the chat model and get a response.
        
        Args:
            message (str): The user's input message
            
        Returns:
            str: The model's response
        """
        response = self.conversation.predict(input=message)
        return response.strip()

def main():
    # Initialize chat model
    print("Initializing chat model...")
    chat_model = LlamaChat()
    
    print("Chat model ready! Type 'quit' to exit.")
    
    # Simple chat loop
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break
            
        try:
            response = chat_model.chat(user_input)
            print(f"\nAssistant: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()