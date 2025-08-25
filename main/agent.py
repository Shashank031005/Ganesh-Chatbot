# This file should be located at: main/agent.py
from gpt4all import GPT4All
import os
from dotenv import load_dotenv
from .prompt import prompt as ganesha_prompt # Assumes you have a prompt.py file
from pydantic import BaseModel
from typing import Optional
import json

# --- Load environment variables and set up model path ---
load_dotenv()
model_path = os.getenv("MODEL_PATH")
if not model_path:
    # Default model path if not set in .env
    # IMPORTANT: Update this path to where your model is actually located
    model_path = r"C:\Users\Admin\AppData\Local\nomic.ai\GPT4All\Meta-Llama-3-8B-Instruct.Q4_0.gguf"

# --- Initialize the language model ---
try:
    model = GPT4All(model_path, device="cpu", allow_download=False)
except Exception as e:
    print(f"Error loading model file: {model_path}")
    print(f"Details: {e}")
    print("Please download the model or set the correct path in your .env file")
    model = None

# --- Define the response structure using Pydantic ---
class GaneshResponse(BaseModel):
    """A structured class to hold the response from the agent, validated by Pydantic."""
    lang: str
    blessing_open: str
    answer: str
    blessing_close: str
    refusal: bool
    refusal_reason: Optional[str] = ""

    def to_dict(self):
        """
        Converts the Pydantic model object into a JSON-serializable dictionary.
        This ensures compatibility with the Flask backend which calls this method.
        """
        return self.model_dump()

# --- Main function to get the response from the LLM ---
def get_ganesh_response(user_input: str) -> GaneshResponse:
    """
    Generates a structured response from the local LLM based on user input.
    """
    if model is None:
        print("Model not loaded. Returning a fallback error response.")
        return GaneshResponse(
            lang='en',
            blessing_open='',
            answer='I apologize, my connection to the divine consciousness is currently unavailable. Please try again later.',
            blessing_close='',
            refusal=True,
            refusal_reason='LLM model not loaded'
        )
        
    print(f"Agent received text: '{user_input}'")
    
    # Use a chat session to interact with the model
    with model.chat_session(system_prompt=ganesha_prompt) as session:
        raw_response_text = session.generate(user_input, max_tokens=500) # Increased max_tokens
        
        print(f"Raw LLM Output:\n{raw_response_text}")
        
        # Attempt to parse the LLM's JSON output
        try:
            # Pydantic v2 has a robust JSON validation method
            parsed_data = GaneshResponse.model_validate_json(raw_response_text)
        except Exception as e:
            print(f"Failed to parse LLM response into Pydantic model. Error: {e}")
            # Fallback response if the LLM output is not valid JSON
            parsed_data = GaneshResponse(
                lang='en',
                blessing_open='',
                answer="I heard your words, but my thoughts are unclear at this moment. Please rephrase your question, and I shall try again to offer guidance.",
                blessing_close='',
                refusal=True,
                refusal_reason='LLM output was not valid JSON'
            )
    
    return parsed_data
