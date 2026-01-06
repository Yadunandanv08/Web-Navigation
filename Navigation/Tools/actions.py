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

            locator = page.get_by_role(
                element.role,
                name=element.name
            )

            locator.click()
            return {"status": "ok"}
            
        except Exception as e:
            print(f"Error clicking element: {str(e)}")
            return {"status": "error", "reason": str(e)}
        
    def type_in_element(self, element_id:str, text: str):
        """
        Types text into specified element by its ID.
        """
        try:
            element = self.element_store.get(element_id)
            page = self.session.get_page()

            locator = page.get_by_role(
                element.role,
                name=element.name
            )

            locator.fill(text)
            return {"status": "ok"}
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
        
