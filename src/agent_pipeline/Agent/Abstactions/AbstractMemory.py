from abc import ABC, abstractmethod
from typing import List, Dict, Any

class MemoryManager(ABC):
    """Abstract base class for memory management strategies."""
    
    @abstractmethod
    def add_message(self, role: str, content: str):
        """Adds a permanent message to conversation history."""
        pass

    @abstractmethod
    def get_context(self) -> str:
        """Retrieves the formatted conversation history for the prompt."""
        pass
    
    @abstractmethod
    def get_raw_history(self) -> List[Dict[str, str]]:
        """Returns the raw list of conversation messages."""
        pass

    @abstractmethod
    def add_scratchpad_entry(self, entry: str):
        """Adds a log entry (observation/thought) to the current task's scratchpad."""
        pass

    @abstractmethod
    def get_scratchpad(self) -> str:
        """Retrieves the formatted scratchpad for the prompt."""
        pass

    @abstractmethod
    def clear_scratchpad(self):
        """Clears the scratchpad. Usually called at the start of a new user goal."""
        pass
    
    @abstractmethod
    def get_raw_scratchpad(self) -> List[str]:
        """Returns the raw list of scratchpad entries."""
        pass