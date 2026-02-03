from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element import Element, ElementStore
from Navigation.Tools.change_observer import ChangeObserver
from Navigation.Tools.ToolHelpers.perception_helper import _parse_and_store_logic, format_planner_line, strip_none

class PerceptionTools:
    def __init__(self, session: BrowserManager, element_store: ElementStore):
        self.session = session
        self.element_store = element_store
        self.change_observer = ChangeObserver(element_store)

    def take_snapshot(self) -> str:
        """
        Full reset. Clears memory, creates fresh IDs 1..N.
        """
        try:
            page = self.session.get_page()
            raw_snapshot = page.locator("body").aria_snapshot()
            # print(raw_snapshot)
            
            self.element_store.clear()
            fresh_elements = self.change_observer._parse_fresh_dom(raw_snapshot)
            
            for i, el in enumerate(fresh_elements, 1):
                el.id = str(i)
                self.element_store.add(el)
            
            planner_lines = [format_planner_line(el) for el in fresh_elements]
            print("snapshot:", planner_lines)
            return (
                f"status: success\n"
                f"snapshot_type: full\n"
                f"elements:\n{planner_lines}"
            )
        except Exception as e:
            return f"status: error\nreason: {str(e)}"

    def observe(self) -> str:
        try:
            page = self.session.get_page()
            raw_snapshot = page.locator("body").aria_snapshot()
            
            result = self.change_observer.reconcile(raw_snapshot)
            
            final_elements = result["elements"]
            new_ids = result["new_ids"]
            updated_ids = result["updated_ids"]
            removed_count = result["removed_count"]
            stability = result["stability_score"]

            
            IS_NAVIGATION = False
            
            if stability >= 0.8:
                IS_NAVIGATION = False
                
            elif stability < 0.6:
                IS_NAVIGATION = True
                
            else:
                 
                 if removed_count > len(new_ids):
                     IS_NAVIGATION = True

            if IS_NAVIGATION:
                self.element_store.clear()
                for i, el in enumerate(final_elements, 1):
                    el.id = str(i)
                    self.element_store.add(el)
                
                planner_lines = [format_planner_line(el) for el in final_elements]
                return (
                    f"status: success\n"
                    f"observation: Major page content change detected (Navigation). IDs reset.\n"
                    f"elements:\n" + "\n".join(planner_lines)
                )

           
            self.element_store.clear()
            for el in final_elements:
                self.element_store.add(el)
            
            parts = []
            
            if updated_ids:
                parts.append(f"Values updated in {len(updated_ids)} fields.")

            if new_ids or removed_count > 0:
                parts.append(f"Layout updated: {len(new_ids)} new items, {removed_count} removed.")
                
                if new_ids:
                    # Only show new IDs
                    new_objs = [self.element_store.get(nid) for nid in new_ids]
                    lines = [format_planner_line(el) for el in new_objs]
                    parts.append("New Elements (Use these IDs):\n" + "\n".join(lines))
            
            if not parts:
                return "status: success\nobservation: No significant visual changes."
                
            return f"status: success\nobservation: {' '.join(parts)}"

        except Exception as e:
            return f"status: error\nreason: {str(e)}"