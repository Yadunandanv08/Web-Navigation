# from nav2.Browser.manager import BrowserManager
# from nav2.Tools.Models.element import ElementStore
# from nav2.normalization.normalize_actions import _normalize_actions, _normalize_ids
# from nav2.Tools.ToolHelpers.action_helper import _observe_and_report
# from nav2.Tools.perception import PerceptionTools 
# import time
# import random

# class ActionTools:
#     def __init__(
#         self, 
#         session: BrowserManager, 
#         element_store: ElementStore,
#         perception_tools: PerceptionTools  
#     ):
#         self.session = session
#         self.element_store = element_store
#         self.perception = perception_tools 


#     def click_elements(self, element_ids: list[str]):
#         """
#             Clicks on a list of web elements identified by their unique IDs.
#             Args:
#                 element_ids (list[str]): A list of EXACT integer IDs found by the perception agent.
#                                         Example: ['12', '45', '88']
#         """
#         try:
#             page = self.session.get_page()
#             results = []
#             element_ids = _normalize_ids(element_ids)
#             wait_range = (0.3, 0.8)

#             for element_id in element_ids:
#                 try:
#                     element = self.element_store.get(element_id)
#                     if not element:
#                         raise ValueError(f"Element ID '{element_id}' not found.")

#                     locator = page.locator(element.selector).first
#                     locator.wait_for(state="visible", timeout=3000)
#                     locator.scroll_into_view_if_needed()
#                     locator.click(timeout=60000)

#                     time.sleep(random.uniform(*wait_range))
#                     results.append({"element_id": element_id, "status": "ok"})

#                 except Exception as e:
#                     results.append({
#                         "element_id": element_id,
#                         "status": "error",
#                         "reason": str(e)
#                     })

#             base_result = {
#                 "status": "partial" if any(r["status"] == "error" for r in results) else "ok",
#                 "results": results
#             }

#             print(_observe_and_report(base_result, self.perception))

#             return _observe_and_report(base_result, self.perception)

#         except Exception as e:
#             return {"status": "error", "reason": str(e)}
        
#     def type_in_elements(self, actions: list[dict]):
#         """
#         Types text into specified fields.
#         Args:
#             actions (list[dict]): [{"element_id": "5", "text": "John"}]
#         """

#         try:
#             page = self.session.get_page()
#             results = []

#             actions = _normalize_actions(actions)
#             typing_delay_range = (50, 120)
#             field_wait_range = (0.4, 1.0)

#             for action in actions:
#                 time.sleep(0.5)
#                 element_id = action.get("element_id", "UNKNOWN")

#                 try:
#                     if "element_id" not in action or "text" not in action:
#                         raise ValueError("Action missing 'element_id' or 'text'")

#                     text = action["text"]
#                     element = self.element_store.get(element_id)

#                     if not element:
#                         raise ValueError(f"Element ID '{element_id}' not found in store.")

#                     locator = page.locator(element.selector).first
#                     locator.wait_for(state="visible", timeout=60000)
#                     locator.scroll_into_view_if_needed()

#                     # Focus field
#                     locator.click()
#                     time.sleep(random.uniform(0.1, 0.3))

#                     # Clear and type
#                     locator.fill("")
#                     locator.type(text, delay=random.randint(*typing_delay_range))

#                     time.sleep(random.uniform(*field_wait_range))

#                     results.append({
#                         "element_id": element_id,
#                         "status": "ok"
#                     })

#                 except Exception as e:
#                     results.append({
#                         "element_id": element_id,
#                         "status": "error",
#                         "reason": str(e)
#                     })

#             base_result = {
#                 "status": "partial" if any(r["status"] == "error" for r in results) else "ok",
#                 "results": results
#             }

#             print(_observe_and_report(base_result, self.perception))

#             return _observe_and_report(base_result, self.perception)

#         except Exception as e:
#             return {"status": "error", "reason": str(e)}

from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element import ElementStore
from Navigation.normalization.normalize_actions import _normalize_actions, _normalize_ids
from Navigation.Tools.ToolHelpers.action_helper import _observe_and_report
from Navigation.Tools.perception import PerceptionTools 
import time
import random
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class ActionTools:
    def __init__(self, session, element_store, perception_tools,file_path):
        self.session = session
        self.element_store = element_store
        self.perception = perception_tools
        self.file_path = file_path 

    def click_elements(self, element_ids: list[str]):
        """
            Clicks on a list of web elements identified by their unique IDs.
        """
        results = []
        try:
            page = self.session.get_page()
            for eid in element_ids:
                try:
                    el = self.element_store.get(eid)
                    if not el: raise ValueError(f"ID {eid} not found")
                    loc = page.locator(el.selector).first
                    loc.wait_for(state="visible", timeout=3000)
                    loc.click(timeout=5000)
                    results.append({"element_id": eid, "status": "ok"})
                except Exception as e: results.append({"element_id": eid, "status": "error", "reason": str(e)})
            
            base = {"status": "partial" if any(r["status"]=="error" for r in results) else "ok", "results": results}
            time.sleep(3)
            return _observe_and_report(base, self.perception)
        except Exception as e: return {"status": "error", "reason": str(e)}

    def type_in_elements(self, entries: list[dict]):
        """
        Types text into a list of web elements.

        Args:
            entries (list[dict]): A list of data entries to type. 
                                  Each entry MUST be a dictionary with:
                                  - "element_id" (str): The ID of the field.
                                  - "text" (str): The text to type.
        """
        results = []
        try:
            page = self.session.get_page()
            
            for entry in entries: 
                eid = entry.get("element_id")
                text = entry.get("text")
                
                try:
                    el = self.element_store.get(eid)
                    if not el: raise ValueError(f"ID {eid} not found")
                    loc = page.locator(el.selector).first
                    loc.fill("")
                    loc.type(text)
                    results.append({"element_id": eid, "status": "ok"})
                except Exception as e: 
                    results.append({"element_id": eid, "status": "error", "reason": str(e)})

            base = {"status": "partial" if any(r["status"]=="error" for r in results) else "ok", "results": results}
            
            return _observe_and_report(base, self.perception)
        except Exception as e: 
            return {"status": "error", "reason": str(e)}


    def set_date(self, element_id: str, date_str: str):
        """
        Sets the date in a date input field. Date should be in YYYY-MM-DD format
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
    


    
    def upload_file(self, element_id: str):
        """
        Uploads a file to a file input id
        """
        try:
            page = self.session.get_page()
            el = self.element_store.get(element_id)
            if not el: raise ValueError(f"ID {element_id} not found")
            
            locator = page.locator(el.selector).first
            locator.wait_for(state="visible", timeout=3000)

            
            try:
                with page.expect_file_chooser(timeout=2000) as fc_info:
                    locator.click()
                
                file_chooser = fc_info.value
                file_chooser.set_files(self.file_path)
                return _observe_and_report({"status": "ok", "results": [{"element_id": element_id, "status": "uploaded"}]}, self.perception)

            except PlaywrightTimeoutError:
                print("Direct upload timed out. Searching for Google Picker modal...")
                
                time.sleep(2)

                browse_btn = None
                
                if page.get_by_text("Browse", exact=True).is_visible():
                    browse_btn = page.get_by_text("Browse", exact=True)
                elif page.get_by_text("Select files from your device").is_visible():
                    browse_btn = page.get_by_text("Select files from your device")
                
                if not browse_btn:
                    for frame in page.frames:
                        try:
                            if frame.get_by_text("Browse", exact=True).is_visible():
                                browse_btn = frame.get_by_text("Browse", exact=True)
                                print("Found 'Browse' button inside an iframe.")
                                break
                            if frame.get_by_text("Select files from your device").is_visible():
                                browse_btn = frame.get_by_text("Select files from your device")
                                print("Found 'Select files' button inside an iframe.")
                                break
                        except:
                            continue 

                if browse_btn:
                    with page.expect_file_chooser(timeout=10000) as fc_info:
                        browse_btn.click()
                    
                    file_chooser = fc_info.value
                    file_chooser.set_files(self.file_path)
                    
                    time.sleep(3) 
                    
                    return _observe_and_report({"status": "ok", "results": [{"element_id": element_id, "status": "uploaded_via_modal"}]}, self.perception)
                else:
                    raise Exception("Could not find 'Browse' or 'Select files' button in any frame.")

        except Exception as e:
            return {"status": "error", "reason": str(e)}