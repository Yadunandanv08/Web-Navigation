
from Navigation.Tools.Models.element import Element
from typing import Dict

class ElementStore:
    def __init__(self):
        self._elements: Dict[str, Element] = {}

    def add(self, element: Element):
        self._elements[element.id] = element

    def get(self, element_id: str) -> Element:
        return self._elements[element_id]

    def remove(self, element_id: str):
        self._elements.pop(element_id, None)

    def by_scope(self, scope: str):
        return [e for e in self._elements.values() if e.scope == scope]

    def all(self):
        return list(self._elements.values())

    def clear(self):
        self._elements.clear()
