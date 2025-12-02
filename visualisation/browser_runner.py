from playwright.sync_api import sync_playwright

class BrowserRunner:
    def __init__(self):
        self._play = sync_playwright().start()
        self.browser = self._play.chromium.launch(headless=False, args=["--start-maximized"])
        self.page = self.browser.new_page(no_viewport=True)

    def _title_to_href(self, title: str) -> str:
        slug = title.replace(" ", "_")
        return f"/wiki/{slug}"

    def open_page(self, title: str):
        url = "https://en.wikipedia.org" + self._title_to_href(title)
        self.page.goto(url)

    def click_link_to(self, target_title: str):
        """
        On the current page, scroll. show red box around target_title link and then click it.
        """
        href = self._title_to_href(target_title)

        locator = self.page.locator(f"a[href='{href}']") # Searces for <a href='{href}'>

        if locator.count() == 0:
            # Fallback: try by visible text i.e. <a>{target_title}</a>
            locator = self.page.locator("a", has_text=target_title)

        if locator.count() == 0:
            print(f"[BROWSER] Could not find link for '{target_title}', going directly.")
            self.open_page(target_title)
            return

        link = locator.first

        # Scroll into view
        link.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300)

        # Highlight with a red box using JS
        element_handle = link.element_handle()
        if element_handle:
            self.page.evaluate(
                """el => {
                    el.style.outline = '3px solid red';
                    el.style.outlineOffset = '2px';
                    el.style.transition = 'outline 0.2s ease-in-out';
                }""",
                element_handle,
            )

        # Pause so the red box is visible
        self.page.wait_for_timeout(800)

        link.click()

    def close(self):
        self.browser.close()
        self._play.stop()
