import os
from dotenv import load_dotenv
from groq import Groq
from typing import List, Dict
from agent_pipeline.Agent.Abstactions.AbstractLLM import AbstractLLMClient

load_dotenv()

class GroqClient(AbstractLLMClient):

    def __init__(self, model_name=None):
        super().__init__(model_name)
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = model_name or os.getenv("GROQ_MODEL")

    def _convert_history(self, history):
        return [
            {"role": m["role"], "content": m["content"]}
            for m in history
        ]

    def generate_response(self, prompt, history):
        groq_history = self._convert_history(history)

        response = self.client.chat.completions.create(
            messages=groq_history,
            model=self.model_name
        )

        return response.choices[0].message.content

    
    