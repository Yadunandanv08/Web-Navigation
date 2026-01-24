import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict
from agent_pipeline.Agent.Abstactions.AbstractLLM import AbstractLLMClient

load_dotenv()

class OpenRouterClient(AbstractLLMClient):

    def __init__(self, model_name=None):
        super().__init__(model_name)
        self.api_key = os.getenv("OPEN_ROUTER_API_KEY")
        self.model_name = model_name or os.getenv("OPEN_ROUTER_MODEL")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def _convert_history(self, history: List[Dict]):
        return [
            {"role": m["role"], "content": m["content"]}
            for m in history
        ]

    def generate_response(self, prompt, history):
        messages = self._convert_history(history)

        payload = {
            "model": self.model_name,
            "messages": messages
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            url=self.api_url,
            headers=headers,
            data=json.dumps(payload)
        )

        # raise error
        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]
