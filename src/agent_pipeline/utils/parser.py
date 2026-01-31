import re, json

def extract_tagged_json(text: str, tag: str):
    matches = re.findall(rf'<{tag}>(.*?)</{tag}>', text, re.S)
    if not matches:
        return None
    raw = matches[-1].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            return json.loads(raw.replace("'", '"'))
        except:
            return None
        
def extract_tagged_content(text: str, tag: str) -> str | None:
    pattern = f'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
