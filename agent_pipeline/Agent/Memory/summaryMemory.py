
from agent_pipeline.Agent.Abstactions.AbstractMemory import MemoryManager
from typing import List, Dict

class SummaryMemory(MemoryManager):
    
    def __init__(self, llm_client, max_tokens=1000):
        self.history = []
        self.summary = ""
        self.llm_client = llm_client
        self.max_tokens = max_tokens 

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        # If len(history) > limit:
        #    new_summary = llm_client.summarize(self.summary + oldest_messages)
        #    self.summary = new_summary
        #    remove oldest_messages

    def get_context(self) -> str:
        recent_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history[-5:]])
        return f"Summary of past events: {self.summary}\n\nRecent Chat:\n{recent_str}"

    def get_raw_history(self) -> List[Dict[str, str]]:
        return self.history