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
        
    def strip_none(self, d: dict) -> dict:
        return {k: v for k, v in d.items() if v is not None}
    
    def format_planner_line(self, el: dict) -> str:
        """
        Convert a structured element dict into a compact planner format:
        id:role|primary_text|flags
        """
        el_id = el["id"]
        role = el["role"]

        primary = el.get("name") or el.get("text") or ""

        if primary and (" " in primary or "|" in primary or ":" in primary):
            primary = f'"{primary}"'

        parts = [f"{el_id}:{role}|{primary}"]

        parent = el.get("parent")
        if parent is not None:
            parts.append(f"p={parent}")

        return "|".join(parts)



        #changes
        self.embedder = Embedder()
        self.retriever = Retriever(self.embedder)

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
            self.strip_none({
                "id": el.id,
                "role": el.role,
                # "scope": el.scope,
                "name": el.name,
                "text": el.text,
                "parent": el.parent,
                # "states": el.states,
            })
            for el in self.element_store.all()
            ]

            planner_snapshot = [
                self.format_planner_line(el)
                for el in data
            ]


            with open("snapshot.yaml", "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

            
            final_output = (
                f"status: success\n"
                f"snapshot:\n"
                f"{planner_snapshot}"
            )

            # print(f"Compressed Output to Agent:\n{final_output}...\n")
            return final_output
        except Exception as e:
            return {"status": "error", "reason": str(e)}
        
        self.element_store.clear()
        
        self._parse_and_store(raw_snapshot)
        
        elements = self.element_store.all()
        texts_to_index = []
        metadata = []

     #   summary = []
        for el in elements:
            desc = f"Role: {el.role}, Name: {el.name}, Text: {el.text}"
            texts_to_index.append(desc)
            metadata.append({"id":el.id,"role":el.role,"name":el.name})
#
 #           if el.role in ['textbox', 'combobox', 'button', 'checkbox', 'radio']:
  #              summary.append(f"- {el.role}: '{el.name or el.text}'")

        self.retriever.index_data(texts_to_index, metadata)
   #     readable_summary = "\n".join(summary[:15]) # Limit summary size to save tokens
    #    return f"Snapshot indexed successfully. Discovered elements:\n{readable_summary}\n\nUse retrieve_element for specific IDs."


        data = [
        {
            "id": el.id,
            "role": el.role,
            "scope": el.scope,
            "name": el.name,
            "text": el.text,
            "parent": el.parent,
            "states": el.states,
        }
        for el in self.element_store.all()
    ]

        return {
            "status": "success",
            "message": f"{yaml.dump(data, allow_unicode=True, sort_keys=False)}"
        }


    def retrieve_element(self, query: str) -> str:
        """Finds the most relevant element IDs based on a natural language query."""
        results = self.retriever.retrieve(query, top_k=3)
        return yaml.dump(results, allow_unicode=True)
    
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
