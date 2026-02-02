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

    def generate_response(self, messages):
        messages = self._convert_history(messages)

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




# import os
# import json
# import requests
# from datetime import datetime
# from dotenv import load_dotenv
# from typing import List, Dict
# from agent_pipeline.Agent.Abstactions.AbstractLLM import AbstractLLMClient

# load_dotenv()

# class OpenRouterClient(AbstractLLMClient):

#     def __init__(self, model_name=None, log_file="openrouter_log.txt"):
#         super().__init__(model_name)
#         self.api_key = os.getenv("OPEN_ROUTER_API_KEY")
#         self.model_name = model_name or os.getenv("OPEN_ROUTER_MODEL")
#         self.api_url = "https://openrouter.ai/api/v1/chat/completions"
#         self.log_file = log_file

#     def _convert_history(self, history: List[Dict]):
#         return [
#             {"role": m["role"], "content": m["content"]}
#             for m in history
#         ]

#     def _log_interaction(self, messages, response_content):
#         """Helper to append request/response to the log file."""
#         try:
            
#             with open(self.log_file, "a", encoding="utf-8") as f:
                
                
#                 # Pretty print the messages list
#                 f.write(json.dumps(messages, indent=2, ensure_ascii=False))
                
#                 f.write(str(response_content))
                
                
#         except Exception as e:
#             print(f"Warning: Failed to write to log file: {e}")

#     def generate_response(self, messages):
#         try:
#             # Convert messages first
#             converted_messages = self._convert_history(messages)

#             payload = {
#                 "model": self.model_name,
#                 "messages": converted_messages
#             }

#             headers = {
#                 "Authorization": f"Bearer {self.api_key}",
#                 "Content-Type": "application/json",
#             }

#             response = requests.post(
#                 url=self.api_url,
#                 headers=headers,
#                 data=json.dumps(payload)
#             )

#             # Raise error for bad status codes
#             response.raise_for_status()
            
#             data = response.json()
#             content = data["choices"][0]["message"]["content"]

#             # Log success
#             self._log_interaction(converted_messages, content)

#             return content

#         except Exception as e:
#             # Log failure
#             self._log_interaction(self._convert_history(messages), f"ERROR: {str(e)}")
#             raise e