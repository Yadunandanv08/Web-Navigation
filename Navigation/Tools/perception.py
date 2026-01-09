from Navigation.Browser.manager import BrowserManager
from Navigation.Tools.Models.element_store import Element, ElementStore
import yaml
import json

class PerceptionTools:
    def __init__(self, session: BrowserManager, element_store: ElementStore):
        self.session = session
        self.element_store = element_store
    
    def take_snapshot(self):
        """
        Injects JS to find interactive elements, generates robust selectors,
        and stores them.
        """
        try:
            page = self.session.get_page()
            
            dom_script = """
            () => {
                const getCssPath = (el) => {
                    if (!(el instanceof Element)) return;
                    const path = [];
                    while (el.nodeType === Node.ELEMENT_NODE) {
                        let selector = el.nodeName.toLowerCase();
                        if (el.id) {
                            selector += '#' + el.id;
                            path.unshift(selector);
                            break; 
                        } else {
                            let sib = el, nth = 1;
                            while (sib = sib.previousElementSibling) {
                                if (sib.nodeName.toLowerCase() == selector) nth++;
                            }
                            if (nth != 1) selector += ":nth-of-type("+nth+")";
                        }
                        path.unshift(selector);
                        el = el.parentNode;
                    }
                    return path.join(" > ");
                };

                const getComputedLabel = (el) => {
                    if (el.getAttribute('aria-label')) return el.getAttribute('aria-label');
                    if (el.getAttribute('aria-labelledby')) {
                        const labelEl = document.getElementById(el.getAttribute('aria-labelledby'));
                        if (labelEl) return labelEl.innerText;
                    }
                    if (el.id) {
                        const label = document.querySelector(`label[for="${el.id}"]`);
                        if (label) return label.innerText;
                    }
                    if (el.placeholder) return el.placeholder;
                    if (el.innerText && el.innerText.trim().length > 0) return el.innerText;
                    if (el.tagName === 'INPUT' && el.type === 'submit') return el.value;
                    return ""; 
                };

                const elements = document.querySelectorAll(
                    'input, button, a, textarea, select, [role="button"], [role="link"], [role="checkbox"], [role="radio"]'
                );
                
                let extracted = [];
                let counter = 1;

                elements.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.width === 0 || rect.height === 0 || window.getComputedStyle(el).visibility === 'hidden') return;

                    extracted.push({
                        id: counter.toString(),
                        // MATCHING PYTHON KEY: 'tag_name'
                        tag_name: el.tagName.toLowerCase(), 
                        selector: getCssPath(el),
                        text: getComputedLabel(el).trim(),
                        // MATCHING PYTHON KEY: 'attributes'
                        attributes: {
                            type: el.type || '',
                            role: el.getAttribute('role') || el.tagName.toLowerCase(),
                            placeholder: el.placeholder || '',
                            name: el.name || ''
                        },
                        // MATCHING PYTHON KEY: 'states'
                        states: {
                            required: el.required || false,
                            checked: el.checked || false,
                            disabled: el.disabled || false
                        }
                    });
                    counter++;
                });
                return extracted;
            }
            """
            
            raw_elements = page.evaluate(dom_script)
            
            self.element_store.clear()
            yaml_snapshot = []

            for item in raw_elements:
                el = Element(
                    element_id=item['id'],
                    tag_name=item['tag_name'], 
                    selector=item['selector'],
                    attributes=item['attributes'],
                    text=item['text'],
                    states=item['states']
                )
                self.element_store.add(el)

                yaml_snapshot.append({
                    "id": el.id,
                    "tag": el.tag_name,
                    "text": el.text[:50], 
                    "type": el.attributes.get('type'), 
                    "selector": el.selector
                })

            with open("snapshot.yaml", "w", encoding="utf-8") as f:
                yaml.dump(yaml_snapshot, f, sort_keys=False)

            return yaml.dump(yaml_snapshot, sort_keys=False)

        except Exception as e:
            return f"Error taking snapshot: {str(e)}"