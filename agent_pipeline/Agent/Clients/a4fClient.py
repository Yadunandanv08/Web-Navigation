import os
from openai import OpenAI
from agent_pipeline.Agent.Abstactions.AbstractLLM import AbstractLLMClient

class A4FClient(AbstractLLMClient):

    def __init__(self, model_name=None):
        super().__init__(model_name)
        self.client = OpenAI(
            base_url="https://api.a4f.co/v1",
            api_key=os.getenv("A4F_API_KEY"),
        )
        self.model_name = model_name or os.getenv("A4F_MODEL")

    def generate_response(self, prompt, history):
        
        formatted_messages = []
        for msg in history:
            role = msg["role"].lower()
            
            if role == "model": 
                role = "assistant"
                
            formatted_messages.append({
                "role": role,
                "content": msg["content"]
            })

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_messages,
                temperature=0 
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"Error calling A4F API: {str(e)}"