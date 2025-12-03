from playwright.sync_api import sync_playwright
from urllib.parse import quote

class BrowserRunner:
    def __init__(self):
        self._play = sync_playwright().start()
        self.browser = self._play.chromium.launch(headless=False, args=["--start-maximized"])
        self.page = self.browser.new_page(no_viewport=True)

    def _title_to_href(self, title: str) -> str:
        slug = title.replace(" ", "_")
        # Percent-encode for URL (ü → %C3%BC, ' → %27)
        encoded_slug = quote(slug, safe='()_')
        return f"/wiki/{encoded_slug}"

    def _expand_collapsible_sections(self):
            """
            Click all 'show' buttons in collapsible sections (navboxes, etc.)
            so that hidden links become visible.
            """
            self.page.evaluate(
                """
                () => {
                    document
                    .querySelectorAll('.mw-collapsible-toggle .mw-collapsible-text')
                    .forEach(el => {
                        if (el.textContent.trim().toLowerCase() === 'show') {
                            el.click();
                        }
                    });
                }
                """
            )

    def open_page(self, title: str):
        url = "https://en.wikipedia.org" + self._title_to_href(title)
        self.page.goto(url)

    def click_link_to(self, target_title: str):
        """
        On the current page, scroll. show red box around target_title link and then click it.
        """
        self._expand_collapsible_sections()

        href = self._title_to_href(target_title)

        locator = self.page.locator(f'a[href="{href}"]')    # Searces for <a href='{href}'>


        if locator.count() == 0:
            # Fallback: try by visible text i.e. <a href='{href}'>target_title</a>
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

        # Try a normal Playwright click first: (checks visibility/stability i.e. if link is visible in current viewport (no scrolling needed))
        try:
            link.click()
        except TimeoutError as e:
            print(
                f"[BROWSER] Normal click timed out for '{target_title}' ({e}). "
                "Falling back to JS click."
            )
            # Force click via JS: (bypasses visibility/stability checks)
            if element_handle:
                self.page.evaluate("el => el.click()", element_handle)
            else:
                # last-resort fallback: just open via URL
                self.open_page(target_title)
        except Exception as e:
            print(
                f"[BROWSER] Click failed for '{target_title}' ({e}). "
                "Falling back to direct navigation."
            )
            self.open_page(target_title)

    def close(self):
        self.browser.close()
        self._play.stop()
