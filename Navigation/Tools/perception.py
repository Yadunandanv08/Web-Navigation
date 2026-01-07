from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element_store import Element, ElementStore
from typing import Dict, Any, List, Optional
import yaml


class PerceptionTools:
    def __init__(self, session: BrowserManager, element_store: ElementStore):
        self.session = session
        self.element_store = element_store
    
    def take_snapshot(self):
        """
        Returns the raw accessibility tree snapshot of the current page.
        Call each time before performing any action to get the latest state.
        """

        try:

            page = self.session.get_page()
            snapshot = page.accessibility.snapshot(interesting_only=False)
            if snapshot is None:
                return {"status": "error", "reason": "No accessibility snapshot available"}
            
            self.element_store.clear()
            extracted_elements = self._parse_accessibility_tree(snapshot) 


            yaml_snapshot = []
            for element in extracted_elements:
                self.element_store.add(element)

                

                yaml_snapshot.append({
                    "id": element.id,
                    "role": element.role,
                    "name": element.name,
                    "states": {k: v for k, v in element.states.items() if v},
                    "path": element.path
                })
            
            with open("snapshot.yaml", "w", encoding="utf-8") as f:
                yaml.dump(yaml_snapshot, f, sort_keys=False, default_flow_style=False)

            return yaml.dump(yaml_snapshot, sort_keys=False, default_flow_style=False)
        
        except Exception as e:
            return f"Error taking snapshot: {str(e)}"
        
    def _parse_accessibility_tree(self, root_node: Dict[str, Any]) -> List[Element]:
        
        elements = []
        _id_counter = 1

        def traverse(node: Dict[str, Any]):
            nonlocal _id_counter
            
           
            role = node.get("role", "generic")
            name = node.get("name", "")
            
        
            interactive_roles = {
                "button", "link", "textbox", "checkbox", "radio", 
                "combobox", "listbox", "tab", "menuitem", "switch",
                "heading", "paragraph", "alert", "StaticText", "text"
            }
            
            is_interactive = (role in interactive_roles and name) 
            
            if is_interactive:
                
                el = Element(
                    element_id=str(_id_counter),
                    role=role,
                    name=name,
                    states={
                        "checked": node.get("checked"),
                        "disabled": node.get("disabled"),
                        "expanded": node.get("expanded"),
                        "focused": node.get("focused")
                    },
                    path=node.get("path", [])
                )
                elements.append(el)
                _id_counter += 1

            # Recursively traverse children
            children = node.get("children", [])
            for child in children:
                traverse(child)

        traverse(root_node)
        return elements
        

    