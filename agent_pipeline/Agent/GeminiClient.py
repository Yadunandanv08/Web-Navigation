import os
from google import genai
from google.genai import types
from typing import List, Dict

from agent_pipeline.Agent.AbstractLLM import AbstractLLMClient
    
class GeminiClient(AbstractLLMClient):

    def __init__(self, model_name=None):
        super().__init__(model_name)
        self.client = genai.Client()
        self.model_name = model_name or os.getenv("GEMINI_MODEL")

    def _convert_history(self, history):
        gem_history = []
        for m in history:
            role = m["role"]
            content = m["content"]
            
            if role == "user":
                gem_role = "user"
            elif role in ["assistant", "system"]:
                gem_role = "model" 
            else:
                continue 

            gem_history.append({
                "role": gem_role,
                "parts": [{"text": content}]
            })
            
        return gem_history

    def generate_response(self, prompt, history):
        gem_history = self._convert_history(history)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=gem_history,
            config=types.GenerateContentConfig(temperature=0)
        )

        return response.text
