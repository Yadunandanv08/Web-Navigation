import re
import json
from playwright.sync_api import sync_playwright

active_sessions = {}


def open_page(session_id:str, url:str):
    """Opens the webpage and initializes a session"""

    if session_id in active_sessions:
        p, browser, _, _ = active_sessions.pop(session_id)
        try:
            browser.close()
        except Exception as e:
            print(f"Error closing browser for session {session_id}: {e}")

    if not re.match(r'^https?://', url):
        url = "https://" + url

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url, timeout=60000)

    active_sessions[session_id] = (p, browser, page, {})
    return f"page opened successfully with session_id: {session_id}"


def get_element(session_id: str):
    """
    Extracts interactive elements from the webpage for performing actions.
    """
    if session_id not in active_sessions:
        return "Error: session not found"
    
    p, browser, page, _ = active_sessions[session_id]

    try:
        # Ensure the page is ready (Hydration fix)
        page.wait_for_load_state('networkidle', timeout=5000)
    except Exception as e:
        print(f"Warning: Network idle timeout: {e}")

    
    snapshot = page.accessibility.snapshot(interesting_only=True)
    
    interactive_elements = []
    element_map = {} 
    element_id_counter = 1

    def process_node(node):
        nonlocal element_id_counter
        
        valid_roles = [
            'button', 'link', 'textbox', 'searchbox', 
            'combobox', 'menuitem', 'checkbox', 'radio', 'tab'
        ]
        
        role = node.get('role', 'generic')
        name = node.get('name', '').strip()
        
        if role in valid_roles and (name or role in ['textbox', 'searchbox', 'combobox']):
            element_id = str(element_id_counter)
            
            element_map[element_id] = {
                "role": role,
                "name": name
            }
            
            interactive_elements.append({
                "id": element_id,
                "role": role,
                "name": name,
                "description": f"[{role}] {name}" 
            })
            
            element_id_counter += 1

        for child in node.get('children', []):
            process_node(child)

    if snapshot:
        process_node(snapshot)

    active_sessions[session_id] = (p, browser, page, element_map)

    if not interactive_elements:
        return json.dumps({"message": "No interactive elements found."}, indent=2)

    return json.dumps(interactive_elements, indent=2)


def click_element(session_id: str, element_id: str):
    """Clicks an element using its Role and Name from the snapshot."""
    if session_id not in active_sessions:
        return "Error: Session not found."
    
    _, _, page, element_map = active_sessions[session_id]
    
    target = element_map.get(element_id)
    if not target:
        return f"Error: Element ID '{element_id}' not found. Please refresh snapshot."

    try:
        locator = page.get_by_role(target['role'], name=target['name'], exact=False).first
        
        locator.highlight()
        locator.click(timeout=10000)
        return f"Clicked {target['role']} '{target['name']}' successfully."
        
    except Exception as e:
        return f"Error clicking element '{element_id}': {e}"
    

def type_in_element(session_id: str, element_id: str, text: str):
    """Types text into an element using Role/Name."""
    if session_id not in active_sessions:
        return "Error: Session not found."
    
    _, _, page, element_map = active_sessions[session_id]
    
    target = element_map.get(element_id)
    if not target:
        return f"Error: Element ID '{element_id}' not found."

    try:
        locator = page.get_by_role(target['role'], name=target['name'], exact=False).first
        
        locator.highlight()
        locator.fill(text, timeout=10000) 
        return f"Typed '{text}' successfully."
        
    except Exception as e:
        return f"Error typing in element '{element_id}': {e}"
    

def press_key(session_id: str, key: str):
    """Presses a key on the keyboard."""
    if session_id not in active_sessions:
        return "Error: Session not found."
    _, _, page, _ = active_sessions[session_id]
    page.keyboard.press(key)
    return f"Pressed key '{key}' successfully."