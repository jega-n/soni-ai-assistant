from playwright.sync_api import sync_playwright

from assistant.config.settings import PLAYWRIGHT_HEADLESS


class Browser:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def launch(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=PLAYWRIGHT_HEADLESS
        )

        self.page = self.browser.new_page()

        return self.page

    def close(self):
        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()