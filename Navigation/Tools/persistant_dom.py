from typing import List, Dict, Any, Set
from Navigation.Tools.Models.element import Element
from Navigation.Tools.element_store import ElementStore

class PersistentDOM:
    def __init__(self, element_store: ElementStore, change_threshold: int = 20):
        self.store = element_store
        self.change_threshold = change_threshold
        self._max_id_counter = 0
        
        if self.store.all():
            self._max_id_counter = max([int(e.id) for e in self.store.all()])

    def process_snapshot(self, parsed_candidates: List[dict]) -> Dict[str, Any]:
        """
        Reconciles new snapshot with existing store.
        """
        processed_ids = set()
        
        snapshot_diff = {
            "added": [],
            "removed": [],
            "updated": [],
            "kept": []
        }

        old_fingerprints: Dict[str, str] = {} 
        temp_role_counts = {}
        
        for el in self.store.all():
            key = (el.role, el.name)
            idx = temp_role_counts.get(key, 0)
            temp_role_counts[key] = idx + 1
            
            sig = f"{el.role}|{el.name}|{idx}" 
            old_fingerprints[sig] = el.id

        seen_new_counters = {} 
        
        for candidate in parsed_candidates:
            role = candidate['role']
            name = candidate['name']
            
            key = (role, name)
            idx = seen_new_counters.get(key, 0)
            seen_new_counters[key] = idx + 1
            
            signature = f"{role}|{name}|{idx}"
            
            if signature in old_fingerprints:
                existing_id = old_fingerprints[signature]
                existing_el = self.store.get(existing_id)
                
                is_modified = False
                
                if existing_el.selector != candidate['locator']:
                    existing_el.selector = candidate['locator']
                    is_modified = True
                
                if existing_el.text != candidate['text']:
                    existing_el.text = candidate['text']
                    is_modified = True
                    
                processed_ids.add(existing_id)
                
                if is_modified:
                    snapshot_diff["updated"].append(existing_el)
                else:
                    snapshot_diff["kept"].append(existing_el)
                    
            else:
                self._max_id_counter += 1
                new_id = str(self._max_id_counter)
                
                new_el = Element(
                    id=new_id,
                    role=candidate['role'],
                    locator=candidate['locator'],
                    scope="global",
                    name=candidate['name'],
                    text=candidate['text'],
                    parent=candidate['parent']
                )
                
                self.store.add(new_el)
                processed_ids.add(new_id)
                snapshot_diff["added"].append(new_el)

        current_store_ids = set(self.store._elements.keys())
        removed_ids = current_store_ids - processed_ids
        
        for r_id in removed_ids:
            el = self.store.get(r_id)
            snapshot_diff["removed"].append(el)
            self.store.remove(r_id)

        return snapshot_diff

    def format_diff_view(self, diff: Dict) -> str:
        total_changes = len(diff['added']) + len(diff['removed']) + len(diff['updated'])
        total_current = len(self.store.all())

        if total_changes > self.change_threshold or (total_current > 0 and total_changes > (total_current * 0.5)):
            return "major_change"
        
        if total_changes == 0:
            return "no_change"
            
        return "incremental"