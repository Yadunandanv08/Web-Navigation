from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.element_store import ElementStore
from Navigation.normalization.normalize_actions import _normalize_actions, _normalize_ids
import time
import random


class ActionTools:
    def __init__(self, session: BrowserManager, element_store: ElementStore):
        self.session = session
        self.element_store = element_store

    def click_elements(self, element_ids: list[str]):
        """
            Clicks on a list of web elements identified by their unique IDs.
            
            Args:
                element_ids (list[str]): A list of EXACT integer IDs found by the perception agent.
                                        Example: ['12', '45', '88']
        """
        try:
            page = self.session.get_page()
            results = []

            element_ids = _normalize_ids(element_ids)
            wait_range = (0.3, 0.8)

            for element_id in element_ids:
                time.sleep(0.5)
                
                try:
                    element = self.element_store.get(element_id)
                    
                    if not element:
                        raise ValueError(f"Element ID '{element_id}' not found in store.")

                    locator = page.locator(element.selector).first
                    locator.wait_for(state="visible", timeout=3000)
                    locator.scroll_into_view_if_needed()
                    locator.click(timeout=60000)

                    time.sleep(random.uniform(*wait_range))

                    results.append({"element_id": element_id, "status": "ok"})

                except Exception as e:
                    if 'element' in locals() and element and element.text and len(element.text) < 40 and not element.text.startswith("["):
                         try:
                            page.get_by_text(element.text, exact=False).first.click(timeout=3000)
                            time.sleep(random.uniform(*wait_range))
                            results.append({
                                "element_id": element_id,
                                "status": "ok",
                                "method": "text_fallback"
                            })
                         except Exception as fallback_e:
                             results.append({
                                "element_id": element_id,
                                "status": "error",
                                "reason": f"Standard failed: {str(e)}, Fallback failed: {str(fallback_e)}"
                            })
                    else:
                        results.append({
                            "element_id": element_id,
                            "status": "error",
                            "reason": str(e)
                        })
            time.sleep(0.5)

            return {
                "status": "partial" if any(r["status"] == "error" for r in results) else "ok",
                "results": results
            }

        except Exception as e:
            print(e)
            return {"status": "error", "reason": str(e)}    

        
    def type_in_elements(self, actions: list[dict]):
        """
    Types text into specified fields.
    
    Args:
        actions (list[dict]): A list of dictionaries where each dict has "element_id" and "text".
                              Example: [{"element_id": "5", "text": "John"}, {"element_id": "7", "text": "Doe"}]
    """
        try:
            page = self.session.get_page()
            results = []

            actions = _normalize_actions(actions)
            typing_delay_range=(50, 120)
            field_wait_range=(0.4, 1.0)

            for action in actions:
                time.sleep(0.5)
                id = action.get("element_id", "UNKNOWN")

                try:
                    if "element_id" not in action or "text" not in action:
                        raise ValueError("Action missing 'element_id' or 'text' key")

                    text = action["text"]
                    element = self.element_store.get(id)

                    if not element:
                        raise ValueError(f"Element ID '{id}' not found in store.")

                    locator = page.locator(element.selector).first
                    locator.wait_for(state="visible", timeout=60000)
                    locator.scroll_into_view_if_needed()

                    locator.click()
                    time.sleep(random.uniform(0.1, 0.3))

                    locator.fill("")
                    locator.type(text, delay=random.randint(*typing_delay_range))

                    time.sleep(random.uniform(*field_wait_range))

                    results.append({
                        "element_id": id,
                        "status": f"typed in {text} successfully"
                    })

                except Exception as e:
                    results.append({
                        "element_id": id,
                        "status": "error",
                        "reason": str(e)
                    })

            return {
                "status": "partial" if any(r["status"] == "error" for r in results) else "ok",
                "results": results
            }
        except Exception as e:
            print(e)
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
