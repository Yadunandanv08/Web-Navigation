import os
from typing import List, Dict
from openai import OpenAI
from agent_pipeline.Agent.Abstactions.AbstractLLM import AbstractLLMClient


class GitHubModelsClient(AbstractLLMClient):

    def __init__(self, model_name: str = None):
        super().__init__(model_name)

        self.client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=os.getenv("GITHUB_API_KEY")
        )

        self.model_name = model_name or os.getenv(
            "GITHUB_MODEL", "openai/gpt-4o-mini"
        )

    def _convert_history(self, history: List[Dict]) -> List[Dict]:
        
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in history
        ]

    def generate_response(self, messages: List[Dict]) -> str:
        messages = self._convert_history(messages)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0,
            max_tokens=4096,
            top_p=1
        )

        return response.choices[0].message.content
