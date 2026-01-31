from agent_pipeline.Agent.Abstactions.AbstractMemory import MemoryManager
from typing import List, Dict

class SlidingWindowMemory(MemoryManager):
    def __init__(self, history_window: int = 6, scratchpad_window: int = 10):
        self.history = []
        self.scratchpad = []
        self.history_window = history_window
        self.scratchpad_window = scratchpad_window

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_context(self) -> str:
        recent_msgs = self.history[-self.history_window:]
        if not recent_msgs:
            return "No previous conversation."
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_msgs])

    def get_raw_history(self) -> List[Dict[str, str]]:
        return self.history

    def add_scratchpad_entry(self, entry: str):
        self.scratchpad.append(entry)

    def get_scratchpad(self) -> str:
        if not self.scratchpad:
            return "No actions taken yet."
        
        recent_steps = self.scratchpad[-self.scratchpad_window:]
        return "\n".join(recent_steps)

    def clear_scratchpad(self):
        self.scratchpad = []

    def get_raw_scratchpad(self) -> List[str]:
        return self.scratchpad