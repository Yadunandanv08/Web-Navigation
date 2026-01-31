import json
import inspect
from typing import get_type_hints, Annotated
import re

def parse_tool_call(tool_call: str) -> dict | None:
    if "<tool_call>" not in tool_call or "</tool_call>" not in tool_call:
        return None

    try:
        json_str = tool_call.split("<tool_call>", 1)[1].split("</tool_call>", 1)[0].strip()
        
        json_str = re.sub(r'^```json\s*', '', json_str)
        json_str = re.sub(r'^```\s*', '', json_str)
        json_str = re.sub(r'\s*```$', '', json_str)
        
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        json_str = re.sub(r'\\\n\s*', '', json_str)
        json_str = json_str.replace('\n', ' ')

        if json_str.startswith("{{") and json_str.endswith("}}"):
            json_str = json_str[1:-1]

        return json.loads(json_str)
    
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Failed.\nError: {e}\nBad String: {json_str}")
        return None


def generate_available_tools(tools_list: list) -> str:
    tool_definitions = []
    for tool in tools_list:
        signature = inspect.signature(tool)
        type_hints = get_type_hints(tool)

        params = {}
        if signature.parameters:
            props = {}
            required = []
            for name, param in signature.parameters.items():
                p_type = type_hints.get(name, str)
                param_def = {}

                if p_type is str:
                    param_def["type"] = "string"
                elif p_type is int:
                    param_def["type"] = "integer"
                elif p_type is float:
                    param_def["type"] = "number"
                elif p_type is bool:
                    param_def["type"] = "boolean"
                elif p_type is list or getattr(p_type, "__origin__", None) is list:
                    param_def["type"] = "array"
                    param_def["items"] = {"type": "string"} 
                elif p_type is dict or getattr(p_type, "__origin__", None) is dict:
                    param_def["type"] = "object"
                else:
                    param_def["type"] = "string"

                props[name] = param_def
                
                if param.default == inspect.Parameter.empty:
                    required.append(name)

            params["properties"] = props
            params["required"] = required

        tool_definitions.append({
            "name": tool.__name__,
            "description": (tool.__doc__ or "").strip(),
            "parameters": params
        })

    return "<tools>\n" + json.dumps(tool_definitions, indent=4) + "\n</tools>"