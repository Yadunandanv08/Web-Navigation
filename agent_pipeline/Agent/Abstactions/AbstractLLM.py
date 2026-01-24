from typing import List, Dict

class AbstractLLMClient:

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.history = []
    
    def generate_response(self, prompt: str, history: List[Dict[str, str]]) -> str:
        raise NotImplementedError("generate_response not implemented")