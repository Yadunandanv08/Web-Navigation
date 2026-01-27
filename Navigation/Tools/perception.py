from pyexpat.errors import messages
import yaml
import json
import re
from typing import List, Dict, Any, Optional

from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element import Element
from Navigation.Tools.element_store import ElementStore
from Navigation.DomMemoryManager import DOMAwareMemoryManager
from agent_pipeline.Agent.Clients.GroqClient import GroqClient

class PerceptionTools:
    def __init__(self, session: BrowserManager, element_store: ElementStore, MemoryManager: Optional[DOMAwareMemoryManager] = None):
        self.session = session
        self.element_store = element_store
        self.memory_manager = MemoryManager

    def compress_snapshot(
        self,
        snapshot: List[Dict],
        llm_client=None
    ) -> List[Dict]:
        
        try:

            if llm_client is None:
                llm_client = GroqClient()

            system_prompt = """
    You are a specialized DOM Compressor for an Agentic AI.
    Your goal is to reduce token usage by removing "noise" while preserving the "signal" required for navigation and interaction.

    ### INPUT DATA:
    A raw snapshot of webpage elements (JSON/YAML).

    ### COMPRESSION RULES:

    1. **FILTERING (What to Keep):**
    - **Interactables:** ALWAYS keep elements with roles: button, link, textbox, checkbox, radio, combobox, listbox, option, img (if clickable).
    - **Context:** Keep headings or text ONLY if they provide essential labels for a nearby input that has a generic name.
    - **Status:** Keep elements indicating state (e.g., [disabled], [selected]).
    - **NOTE:** If any field requires heading or text to understand context, keep that field. Summarize text if possible without losing context. 

    2. **STRUCTURAL INTEGRITY:**
    - **The Orphan Rule:** If you keep a child element, you MUST keep its `parent` element (by ID).
    - **Tree Preservation:** Maintain the valid chain of `parent` references.

    3. **MATRIX GROUPING (High Compression):**
    - **Pattern:** If you see 3+ sibling checkboxes or radios that share the same context but differ only by a specific label (e.g., "Familiar", "Proficient", "Expert"), GROUP them.
    - **Format:** Return a single object with `role: grouped_choice`, a `context` field (the shared topic), and an `options` dictionary mapping `{id: label}`.
    - *Example:* Instead of 3 objects, return:
        `{"role": "grouped_choice", "context": "Cloud Platforms", "parent": "4", "options": {"5": "Familiar", "6": "Proficient", "7": "Expert"}}`

    4. **MINIFICATION:**
    - **Null Removal:** Remove keys with null/empty values.
    - **Text Cleaning:**
        - Remove repetitive prefixes in names (e.g., "Familiar, response for X" -> "Familiar").
        - Summarize long instructions (e.g., "Please select..." -> "Instruction").

    ### OUTPUT FORMAT:
    - Return the result in clean **YAML** format.
    - Do NOT use Markdown code blocks.
    - Do NOT include conversational text..
    """

            user_prompt = yaml.safe_dump(snapshot, allow_unicode=True, sort_keys=False)

            response = llm_client.generate_response(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            cleaned = response.strip()
            if "```" in cleaned:
                match = re.search(r"```(?:yaml|json)?(.*?)```", cleaned, re.DOTALL)
                if match:
                    cleaned = match.group(1).strip()

            return cleaned
        except Exception as e:
            raise ValueError(f"Failed to parse compressed snapshot: {e}")



    def take_snapshot(self) -> str:
        """
        Takes snapshot of the current page to obtain element
        ids for actions or the page summary.
        """
        page = self.session.get_page()

        try:
            raw_snapshot = page.locator("body").aria_snapshot()
            
            
            self.element_store.clear()
            
            self._parse_and_store(raw_snapshot)
            
            data = [
            {
                "id": el.id,
                "role": el.role,
                # "scope": el.scope,
                "name": el.name,
                "text": el.text,
                "parent": el.parent,
                # "states": el.states,
            }
            for el in self.element_store.all()
            ]

            with open("snapshot.yaml", "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

            compressed_snapshot = self.compress_snapshot(
            snapshot=data,
            )
            final_output = (
                f"status: success\n"
                f"snapshot:\n"
                f"{compressed_snapshot}"
            )

            print(f"Compressed Output to Agent:\n{final_output}...\n")
            return final_output
        except Exception as e:
            return {"status": "error", "reason": str(e)}
    
    def _parse_and_store(self, snapshot_text: str) -> None:
        lines = snapshot_text.split('\n')
        
        parent_stack: List[tuple[int, str]] = []
        
        seen_counters: Dict[tuple, int] = {}
        
        pattern = re.compile(r'^(\s*)-\s+(\w+)(?:\s+"([^"]*)")?(?:\s+(.*))?$')
        
        element_counter = 1

        for line in lines:
            if not line.strip(): continue

            match = pattern.match(line)
            if match:
                indent_str, role, quoted_name, remainder_text = match.groups()
                
                indent_level = len(indent_str)

                while parent_stack and parent_stack[-1][0] >= indent_level:
                    parent_stack.pop()
                
                parent_id = parent_stack[-1][1] if parent_stack else None

                name = quoted_name if quoted_name else ""
                
                raw_text = remainder_text.strip() if remainder_text else ""
                
                text_content = raw_text if raw_text and raw_text != name else None

                key = (role, name)
                current_index = seen_counters.get(key, 0)
                seen_counters[key] = current_index + 1
                
                safe_name = name.replace('"', '\\"')
                
                if safe_name:
                    base_locator = f'role={role}[name="{safe_name}"]'
                else:
                    base_locator = f'role={role}'
                
                precise_locator = f'{base_locator} >> nth={current_index}'

                el_id = str(element_counter)
                
                el = Element(
                    id=el_id,
                    role=role,
                    locator=precise_locator,
                    scope="global",
                    name=name if name else None,
                    text=text_content,
                    parent=parent_id
                )
                
                self.element_store.add(el)
                
                parent_stack.append((indent_level, el_id))
                element_counter += 1