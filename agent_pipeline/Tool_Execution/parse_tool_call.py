import json
import inspect
from typing import get_type_hints, Annotated

def parse_tool_call(tool_call: str) -> dict:
    
    json_str = tool_call.split("<tool_call>")[1].split("</tool_call>")[0]
    return json.loads(json_str)

def generate_available_tools(tools_list: list) -> str:
    tool_definitions = []
    for tool in tools_list:
        signature = inspect.signature(tool)
        type_hints = get_type_hints(tool)

        params = {}
        if signature.parameters:
            props = {}
            for name, param in signature.parameters.items():
                p_type = type_hints.get(name, str)

                param_def = {"type": "string"}  
                if getattr(p_type, "__origin__", None) is Annotated:
                    base_type, format_hint = p_type.__args__
                    if base_type is str:
                        param_def["type"] = "string"
                    elif base_type is int:
                        param_def["type"] = "integer"
                    elif base_type is float:
                        param_def["type"] = "number"
                    if isinstance(format_hint, str):
                        param_def["format"] = format_hint
                elif p_type is int:
                    param_def["type"] = "integer"
                elif p_type is float:
                    param_def["type"] = "number"

                props[name] = param_def
            params["properties"] = props

        tool_definitions.append({
            "name": tool.__name__,
            "description": (tool.__doc__ or "").strip(),
            "parameters": params
        })

    return "<tools>\n" + json.dumps(tool_definitions, indent=4) + "\n</tools>"

