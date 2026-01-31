# from typing import Optional, List, Dict, Any

# class Element:
#     def __init__(
#         self,
#         id: str,
#         role: str,
#         locator: str,
#         scope: str,

#         tag: Optional[str] = None,
#         name: Optional[str] = None,
#         label: Optional[str] = None,
#         text: Optional[str] = None,

#         states: Optional[Dict[str, bool]] = None,
#         parent: Optional[str] = None,
#     ):
#         self.id = id
#         self.role = role
#         self.selector = locator
#         self.scope = scope
#         self.tag_name = tag
#         self.name = name
#         self.label = label
#         self.text = text
#         self.attributes: Dict[str, Any] = {}
#         self.states = states if states is not None else {}
#         self.parent = parent
        

#     def __repr__(self):
#         return f"<Element id={self.id} tag={self.tag_name} selector={self.selector}>"



from typing import Optional, Dict, Any

class Element:
    def __init__(
        self,
        id: str,
        role: str,
        locator: str,
        scope: str,
        tag: Optional[str] = None,
        name: Optional[str] = None,
        label: Optional[str] = None,
        text: Optional[str] = None,
        states: Optional[Dict[str, bool]] = None,
        parent: Optional[str] = None,
    ):
        self.id = id
        self.role = role
        self.selector = locator
        self.scope = scope
        self.tag_name = tag
        self.name = name
        self.label = label
        self.text = text
        self.attributes: Dict[str, Any] = {}
        self.states = states if states is not None else {}
        self.parent = parent

    def __repr__(self):
        # Added parent to repr for easier debugging
        return f"<Element id={self.id} role={self.role} name={self.name} parent={self.parent}>"