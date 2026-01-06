from Navigation.Browser.manager import BrowserManager

class NavigationTools:
    def __init__(self, session: BrowserManager):
        self.session = session

    
    def open_page(self, url: str):
        """
        Opens the specified URL in the browser.
        """

        try:
            self.session.start()
            page = self.session.get_page()

            if not url.startswith("http"):
                url = "https://" + url

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )
            return {"status": "ok"}

        except Exception as e:
            return {"status": "error", "reason": str(e)}
        
    def close_browser(self):
        """
        Closes the browser session.
        """
        self.session.close()
        
