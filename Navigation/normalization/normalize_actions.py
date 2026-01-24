import json
import ast
import re

def _clean_llm_string(text: str) -> str:
    text = re.sub(r"```[a-zA-Z]*", "", text)
    text = text.replace("```", "")
    return text.strip()

def _normalize_ids(ids) -> list[str]:
    
    if ids is None:
        return []

    if isinstance(ids, int):
        return [str(ids)]

    if isinstance(ids, str):
        ids = _clean_llm_string(ids)
        
        try:
            return [str(i) for i in json.loads(ids)]
        except (json.JSONDecodeError, TypeError):
            pass

        try:
            val = ast.literal_eval(ids)
            if isinstance(val, list):
                return [str(i) for i in val]
        except (ValueError, SyntaxError):
            pass

   
        if "," in ids:
            return [i.strip() for i in ids.split(",") if i.strip()]
        
        return [ids] if ids else []

    if isinstance(ids, list):
        return [str(i) for i in ids]
    
    if isinstance(ids, (tuple, set)):
        return [str(i) for i in ids]

    return []

def _normalize_actions(actions) -> list[dict]:

    if actions is None:
        return []

    parsed_actions = []

    if isinstance(actions, str):
        actions = _clean_llm_string(actions)
        
        try:
            parsed_actions = json.loads(actions)
        except json.JSONDecodeError:
            
            try:
                parsed_actions = ast.literal_eval(actions)
            except (ValueError, SyntaxError):
         
                if ":" in actions:
                    temp_map = {}
                    
                    pairs = [p for p in actions.split(',') if p.strip()]
                    
                    for pair in pairs:
                       
                        if ":" in pair:
                            k, v = pair.split(":", 1)
                            temp_map[k.strip()] = v.strip()
                    parsed_actions = temp_map
                else:
                    raise ValueError(f"Could not parse actions string: {actions}")
    else:
        parsed_actions = actions

    final_list = []

    if isinstance(parsed_actions, dict):
        if "element_id" in parsed_actions and "text" in parsed_actions:
            final_list.append(parsed_actions)
        
   
        else:
            for k, v in parsed_actions.items():
                final_list.append({"element_id": str(k), "text": str(v)})
    
    elif isinstance(parsed_actions, list):
        final_list = parsed_actions
    
    else:
        raise ValueError(f"Unsupported type for actions: {type(parsed_actions)}")

    sanitized_results = []
    for action in final_list:
        if not isinstance(action, dict):
            continue
            
        e_id = action.get("element_id")
        text = action.get("text")

        if e_id is not None and text is not None:
            sanitized_results.append({
                "element_id": str(e_id), 
                "text": str(text)        
            })

    return sanitized_results