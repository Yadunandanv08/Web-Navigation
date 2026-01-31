import json
import inspect
from typing import get_type_hints, Annotated
import re

def parse_tool_call(tool_call: str) -> dict | None:
    match = re.search(r'<tool_call>(.*?)</tool_call>', tool_call, re.DOTALL)
    if not match:
        return None
    
    raw_content = match.group(1).strip()
    
    clean_content = re.sub(r'^```\w*\s*', '', raw_content)
    clean_content = re.sub(r'\s*```$', '', clean_content) 
    
    start_index = clean_content.find('{')
    end_index = clean_content.rfind('}')
    
    if start_index == -1 or end_index == -1:
        print(f"JSON Parsing Failed: No JSON object found in tag content: {raw_content}")
        return None
        
    json_candidate = clean_content[start_index : end_index + 1]
    
    try:
        return json.loads(json_candidate)
    except json.JSONDecodeError as e:
        try:
            normalized = json_candidate.replace('\n', ' ') 
            return json.loads(normalized)
        except:
            print(f"JSON Parsing Failed.\nError: {e}\nBad String: {json_candidate}")
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