from typing import Optional
from agent_pipeline.Agent.Memory.standard import SlidingWindowMemory

class DOMAwareMemoryManager(SlidingWindowMemory):
    def __init__(self, history_window: int = 6, scratchpad_window: int = 20):
        super().__init__(history_window, scratchpad_window)
        self.current_dom_payload: str = ""
        self.ACTIVE_MARKER = "<<ACTIVE_DOM_SNAPSHOT>>"

    def prepare_for_new_snapshot(self):
        print("[MemoryManager] Preparing for new snapshot...")
        found_active = False
        for i in range(len(self.scratchpad)):
            if self.ACTIVE_MARKER in self.scratchpad[i]:
                print(f"[MemoryManager] Minimizing old DOM snapshot at scratchpad index {i}.")
                self.scratchpad[i] = self.scratchpad[i].replace(
                    self.ACTIVE_MARKER, 
                    "[Old DOM Snapshot minimized to save tokens]"
                )
                found_active = True
        
        if not found_active:
            print("[MemoryManager] No active snapshot found to minimize.")

    def add_scratchpad_entry(self, entry: str):
        if "tool 'take_snapshot'" in entry and "'status': 'success'" in entry:
            try:
                parts = entry.split("'message':", 1)
                
                if len(parts) == 2:
                    header = parts[0]
                    heavy_body = parts[1].rstrip("}") 
                    
                    self.current_dom_payload = heavy_body
                    print(f"[MemoryManager] Captured new DOM payload (Length: {len(heavy_body)} chars).")
                    
                    lightweight_entry = f"{header}'message': '{self.ACTIVE_MARKER}'}}"
                    
                    super().add_scratchpad_entry(lightweight_entry)
                    print("[MemoryManager] Added lightweight marker entry to scratchpad.")
                    return
                else:
                    print("[MemoryManager] Warning: Snapshot format unexpected. Could not split message.")
            except Exception as e:
                print(f"[MemoryManager] Error parsing snapshot entry: {e}")
                super().add_scratchpad_entry(entry)
                return

        super().add_scratchpad_entry(entry)

    def get_scratchpad(self) -> str:
        if not self.scratchpad:
            return "No actions taken yet."
        
        raw_text = "\n".join(self.scratchpad[-self.scratchpad_window:])
        
        if self.ACTIVE_MARKER in raw_text:
            final_text = raw_text.replace(self.ACTIVE_MARKER, self.current_dom_payload)
            return final_text
        
        return raw_text

    def clear_scratchpad(self):
        print("[MemoryManager] Clearing scratchpad and resetting DOM payload.")
        super().clear_scratchpad()
        self.current_dom_payload = ""