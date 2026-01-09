from typing import Optional, List, Dict, Any

class Element:
    def __init__(
        self,
        element_id: str,
        tag_name: str,
        selector: str,  
        attributes: Dict[str, str],
        text: str,
        states: Optional[Dict[str, bool]] = None,
    ):
        self.id = element_id
        self.tag_name = tag_name
        self.selector = selector
        self.attributes = attributes or {}
        self.text = text
        self.states = states or {}

    def __repr__(self):
        return f"<Element id={self.id} tag={self.tag_name} selector={self.selector}>"

class ElementStore:
    def __init__(self):
        self._elements: Dict[str, Element] = {}

    def add(self, element: Element):
        self._elements[element.id] = element

    def get(self, element_id: str) -> Element:
        if element_id not in self._elements:
            raise KeyError(f"Element '{element_id}' not found")
        return self._elements[element_id]

    def clear(self):
        self._elements.clear()

    def all(self):
        return list(self._elements.values())