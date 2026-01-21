from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.element_store import ElementStore
import json


class ActionTools:
    def __init__(self, session: BrowserManager, element_store: ElementStore):
        self.session = session
        self.element_store = element_store
    

    def click_element(self, element_id):
        element = self.element_store.get(element_id)
        page = self.session.get_page()

        try:
        
            if element.tag_name == "a" and element.attributes.get("href"):
                page.goto(element.attributes["href"])
                return {"status": "success", "method": "goto"}

            
            locator = page.locator(element.selector).first
            locator.wait_for(state="visible", timeout=3000)
            locator.scroll_into_view_if_needed()
            locator.click(force=True, timeout=3000)

            return {"status": "success", "method": "dom_click"}

        except Exception:
            if element.text:
                page.get_by_text(element.text, exact=False).first.click(force=True)
                return {"status": "success", "method": "text_fallback"}

            raise



    def type_in_element(self, element_id: str, text: str):
        """
        Types text into specified element by its ID.
        """
        try:
            element = self.element_store.get(element_id)
            page = self.session.get_page()
            
            locator = page.locator(element.selector)
            locator.fill(text)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def set_date(self, element_id: str, date_str: str):
        """
        Sets the date in a date input field.
        """
        try:
            element = self.element_store.get(element_id)
            page = self.session.get_page()
            locator = page.locator(element.selector)
            
            if element.attributes.get('type') == 'date':
                locator.fill(date_str)
                return {"status": "success", "method": "native_date_input"}
            
            
            try:
                locator.click()
                locator.fill(date_str)
                page.keyboard.press("Enter")
                return {"status": "success", "method": "text_fill"}
            except:
                pass

            page.evaluate(
                "(element, value) => { element.value = value; element.dispatchEvent(new Event('input', {bubbles: true})); element.dispatchEvent(new Event('change', {bubbles: true})); }", 
                locator.element_handle(), 
                date_str
            )
            return {"status": "success", "method": "js_injection"}

        except Exception as e:
            return {"status": "error", "reason": str(e)}
        
    def press_key(self, key: str):
        """
        Presses a key on the keyboard.
        """
        try:
            page = self.session.get_page()
            page.keyboard.press(key)
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "reason": str(e)}
        
    def mark_checked(self, element_id: str):
        """
        Marks a checkbox or radio button as checked (ARIA-safe).
        """
        try:
            element = self.element_store.get(element_id)
            page = self.session.get_page()

            role = element.attributes.get("role")

            if role not in ("checkbox", "radio"):
                return {
                    "status": "error",
                    "reason": f"check_element not supported for role '{role}'"
                }

            locator = page.locator(element.selector).first
            locator.wait_for(state="visible", timeout=10000)

            is_checked = locator.get_attribute("aria-checked") == "true"

            if is_checked:
                return {
                    "status": "ok",
                    "message": "Element already checked"
                }

            locator.click(timeout=10000)

            if locator.get_attribute("aria-checked") != "true":
                return {
                    "status": "error",
                    "reason": "Failed to check element"
                }

            return {"status": "ok"}

        except Exception as e:
            return {"status": "error", "reason": str(e)}
    def execute_batch(self, actions):
        """
        Executes a sequence of actions on the page in a single tool call.
        Format: [{"type": "type", "id": "1", "text": "hello"}, {"type": "click", "id": "2"}]
        Supported types: 'click', 'type', 'press_key'.
        """
        if isinstance(actions, str):
            try:
                actions = json.loads(actions)
            except json.JSONDecodeError:
                return {"status": "error", "reason": "Invalid JSON format for actions."}

        results = []
        for action in actions:
            a_type  = action.get('type')
            e_id = action.get('id')
            try:
                if a_type == 'click':
                    results.append(self.click_element(e_id))
                elif a_type == 'type':
                    results.append(self.type_in_element(e_id, action.get('text', '')))
                elif a_type == 'press_key':
                    results.append(self.press_key(action.get('key', '')))
            except Exception as e:
                results.append({"status": "error", "id": e_id, "reason": str(e)})
        return results
