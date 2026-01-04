from typing import Optional, List, Dict


class Element:
    def __init__(
        self,
        element_id: str,
        role: str,
        name: str,
        states: Optional[Dict[str, bool]] = None,
        path: Optional[List[str]] = None,
    ):
        self.id = element_id         
        self.role = role            
        self.name = name              
        self.states = states or {}    
        self.path = path or []        

    def __repr__(self):
        return f"<Element id={self.id} role={self.role} name={self.name}>"


class ElementStore:
    def __init__(self):
        self._elements: Dict[str, Element] = {}

    def add(self, element: Element):
        self._elements[element.id] = element

    def get(self, element_id: str) -> Element:
        if element_id not in self._elements:
            raise KeyError(f"Element '{element_id}' not found")
        return self._elements[element_id]

    def remove(self, element_id: str):
        self._elements.pop(element_id, None)

    def clear(self):
        self._elements.clear()

    def all(self):
        return list(self._elements.values())

    def __len__(self):
        return len(self._elements)
