import re
from typing import List
from agent_pipeline.Agent.Memory.standard import SlidingWindowMemory

class DOMAwareMemoryManager(SlidingWindowMemory):
    def __init__(self, history_window: int = 6, scratchpad_window: int = 8):
        super().__init__(history_window, scratchpad_window)
       
        self.active_dom_payload: str = ""
        self.MARKER = "<<ACTIVE_DOM_SNAPSHOT>>"

    def add_scratchpad_entry(self, entry: str):
        """
        Intercepts log entries. If it detects a 'take_snapshot' result, 
        it effectively 'minimizes' the previous snapshot in history 
        and stores the new one as the active payload.
        """
        snapshot_pattern = r"(Observation \d+:.*tool 'take_snapshot'.*Result:.*)(elements:\s*\n)(.*)"
        match = re.search(snapshot_pattern, entry, re.DOTALL)

        if match:
            for i in range(len(self.scratchpad)):
                if self.MARKER in self.scratchpad[i]:
                    self.scratchpad[i] = self.scratchpad[i].replace(
                        self.MARKER, 
                        "\n[PREVIOUS DOM SNAPSHOT MINIMIZED TO SAVE TOKENS]\n"
                    )

            header_info = match.group(1) 
            heavy_content = match.group(3) 
            
            self.active_dom_payload = heavy_content.strip()

            lightweight_entry = f"{header_info}\n[CURRENT PAGE STATE]:\n{self.MARKER}"
            super().add_scratchpad_entry(lightweight_entry)
            
            print(f"[Memory] New DOM Snapshot captured. Length: {len(self.active_dom_payload)} chars.")
            
        else:
            super().add_scratchpad_entry(entry)

    def get_scratchpad(self) -> str:
        """
        Reconstructs the scratchpad. 
        It finds the entry with <<ACTIVE_DOM_SNAPSHOT>> and injects the heavy payload there.
        All other (older) snapshots will remain minimized text.
        """
        if not self.scratchpad:
            return "No actions taken yet."
        
        visible_entries = self.scratchpad[-self.scratchpad_window:]
        raw_text = "\n\n".join(visible_entries)
        
        if self.MARKER in raw_text:
            return raw_text.replace(self.MARKER, self.active_dom_payload)
        
        return raw_text