import os
from google import genai
from google.genai import types
from typing import List, Dict

from agent_pipeline.Agent.Abstactions.AbstractLLM import AbstractLLMClient
    
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

    def generate_response(self, messages):
        gem_history = self._convert_history(messages)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=gem_history,
            config=types.GenerateContentConfig(temperature=0)
        )
        import time
        # time.sleep(10)  

        return response.text




# import os
# import json
# from datetime import datetime
# from google import genai
# from google.genai import types
# from typing import List, Dict

# from agent_pipeline.Agent.Abstactions.AbstractLLM import AbstractLLMClient


# class GeminiClient(AbstractLLMClient):

#     def __init__(self, model_name=None, log_file="gemini_log.txt"):
#         super().__init__(model_name)
#         self.client = genai.Client()
#         self.model_name = model_name or os.getenv("GEMINI_MODEL")
#         self.log_file = log_file

#     def _convert_history(self, history):
#         gem_history = []
#         for m in history:
#             role = m["role"]
#             content = m["content"]

#             if role == "user":
#                 gem_role = "user"
#             elif role in ["assistant", "system"]:
#                 gem_role = "model"
#             else:
#                 continue

#             gem_history.append({
#                 "role": gem_role,
#                 "parts": [{"text": content}]
#             })

#         return gem_history

#     def _log_interaction(self, messages, response_content):
#         """Append request/response to Gemini log file."""
#         try:

#             with open(self.log_file, "a", encoding="utf-8") as f:
                
#                 f.write(json.dumps(messages, indent=2, ensure_ascii=False))

#                 f.write(str(response_content))
               

#         except Exception as e:
#             print(f"Warning: Failed to write Gemini log: {e}")

#     def generate_response(self, messages):
#         gem_history = self._convert_history(messages)

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model_name,
#                 contents=gem_history,
#                 config=types.GenerateContentConfig(temperature=0)
#             )

#             text = response.text

#             # Log before returning
#             self._log_interaction(gem_history, text)

#             return text

#         except Exception as e:
#             self._log_interaction(gem_history, f"ERROR: {str(e)}")
#             raise ValueError(f"GeminiClient failed to generate response: {e}")

