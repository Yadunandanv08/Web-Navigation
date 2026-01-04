from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional


class BrowserManager:

    def __init__(self, headless: bool = False):
        self.headless = headless

        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def start(self):
       
        if self.playwright is not None:
            return  

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 800},
            ignore_https_errors=True
        )

        self.page = self.context.new_page()

    def get_page(self) -> Page:
        
        if self.page is None:
            raise RuntimeError("BrowserManager not started. Call start() first.")
        return self.page

    def close(self):
        
        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
