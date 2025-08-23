from gpt4all import GPT4All
import os
from dotenv import load_dotenv
from prompt import prompt as ganesha_prompt
from pydantic import BaseModel
from typing import Optional
import json

load_dotenv()
model_path = os.getenv("model_path")
model = GPT4All(model_path,device = "cpu",allow_download=False)

class GaneshResponse(BaseModel):
    lang: str
    blessing_open: str
    answer: str
    blessing_close: str
    refusal: bool
    refusal_reason: Optional[str] = ""

with model.chat_session(system_prompt = ganesha_prompt) as session:
    user_input = "Christianity sucks"
    raw = session.generate(user_input)
    
    try:
        data = GaneshResponse.model_validate_json(raw)
    except Exception:
        try:
            data = GaneshResponse(**json.loads(raw))
        except Exception:
            print("Invalid response:", raw)
            data = None
    
    