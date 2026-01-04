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

            count = locator.count()
            if count > 1:
                locator.first.click()
                return {"status": "warning", "message": f"Found {count} elements for '{element.name}'. Clicked the first one."}
            
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
