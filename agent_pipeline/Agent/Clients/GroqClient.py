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

    def generate_response(self, messages):
        try:
            groq_history = self._convert_history(messages)

            response = self.client.chat.completions.create(
                messages=groq_history,
                model=self.model_name
            )

            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"GroqClient failed to generate response: {e}")
    
    


# import os
# import json
# from datetime import datetime
# from dotenv import load_dotenv
# from groq import Groq
# from typing import List, Dict
# from agent_pipeline.Agent.Abstactions.AbstractLLM import AbstractLLMClient

# load_dotenv()

# class GroqClient(AbstractLLMClient):

#     def __init__(self, model_name=None, log_file="groq_log.txt"):
#         super().__init__(model_name)
#         self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#         self.model_name = model_name or os.getenv("GROQ_MODEL")
#         self.log_file = log_file

#     def _convert_history(self, history):
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
#             groq_history = self._convert_history(messages)

#             response = self.client.chat.completions.create(
#                 messages=groq_history,
#                 model=self.model_name
#             )

#             content = response.choices[0].message.content
            
#             # Log the interaction before returning
#             self._log_interaction(groq_history, content)

#             return content
            
#         except Exception as e:
#             # You might want to log the error too
#             self._log_interaction(messages, f"ERROR: {str(e)}")
#             raise ValueError(f"GroqClient failed to generate response: {e}")