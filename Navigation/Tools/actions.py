from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element_store import ElementStore


class ActionTools:
    def __init__(self, session: BrowserManager, element_store: ElementStore):
        self.session = session
        self.element_store = element_store
    
    def click_element(self, element_id: str):
        """
        Clicks on specified element by its ID.
        """
        try:
            element = self.element_store.get(element_id)
            page = self.session.get_page()

            locator = page.locator(element.selector)
            
            locator.scroll_into_view_if_needed()
            locator.click()
            return {"status": "success"}
            
        except Exception as e:
            return {"status": "error", "reason": str(e)}

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
        Handles standard date inputs and Google Form style text-dates.
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
        Marks a checkbox or radio button as checked.
        """

        try:
            element = self.element_store.get(element_id)
            page = self.session.get_page()

            if element.role not in ("checkbox", "radio"):
                return {
                    "status": "error",
                    "reason": f"check_element not supported for role '{element.role}'"
                }
            
            locator = page.get_by_role(
                element.role,
                name=element.name,
                exact=False
            ).first

            if locator.is_checked():
                return {
                    "status": "ok",
                    "message": "Element already checked"
                }
            
            locator.click(timeout=10000)

            if not locator.is_checked():
                return {
                    "status": "error",
                    "reason": "Failed to check element"
                }

            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "reason": str(e)}
            