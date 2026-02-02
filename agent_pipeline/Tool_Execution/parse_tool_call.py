import json
import re
import inspect
from typing import get_type_hints

def parse_tool_calls(response_text: str) -> list[dict]:
    tool_calls = []
    
    matches = re.finditer(r'<tool_call>(.*?)</tool_call>', response_text, re.DOTALL)
    
    for match in matches:
        raw_content = match.group(1).strip()
        
        clean_content = re.sub(r'^```\w*\s*', '', raw_content)
        clean_content = re.sub(r'\s*```$', '', clean_content)
        
        pattern = r'(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)'
        clean_content = re.sub(pattern, lambda m: m.group(1) if m.group(1) else "", clean_content, flags=re.MULTILINE|re.DOTALL)
        
        clean_content = re.sub(r',\s*([\]}])', r'\1', clean_content)

        try:
            parsed_data = json.loads(clean_content)
            
            if isinstance(parsed_data, list):
                tool_calls.extend(parsed_data)
            elif isinstance(parsed_data, dict):
                tool_calls.append(parsed_data)
                
        except json.JSONDecodeError as e:
            try:
                normalized = clean_content.replace('\n', ' ')
                parsed_data = json.loads(normalized)
                if isinstance(parsed_data, list):
                    tool_calls.extend(parsed_data)
                elif isinstance(parsed_data, dict):
                    tool_calls.append(parsed_data)
            except:
                print(f"Skipping malformed tool block due to error: {e}")
                print(f"Failed content snippet: {clean_content[:100]}...")
                continue

    return tool_calls


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
                if name in ["self", "cls"]:
                    continue

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
                    
                    item_def = {"type": "string"}
                    
                    if hasattr(p_type, "__args__") and p_type.__args__:
                        inner_type = p_type.__args__[0]
                        
                        if inner_type is dict:
                            item_def = {"type": "object"} 
                        elif inner_type is int:
                            item_def = {"type": "integer"}
                        elif inner_type is float:
                            item_def = {"type": "number"}
                            
                    param_def["items"] = item_def

                elif p_type is dict or getattr(p_type, "__origin__", None) is dict:
                    param_def["type"] = "object"
                else:
                    param_def["type"] = "string"

                props[name] = param_def
                
                if param.default == inspect.Parameter.empty:
                    required.append(name)

            params["properties"] = props
            if required:
                params["required"] = required

        tool_definitions.append({
            "name": tool.__name__,
            "description": (tool.__doc__ or "").strip(),
            "parameters": params
        })

    return "<tools>" + json.dumps(tool_definitions, separators=(',', ':')) + "</tools>"