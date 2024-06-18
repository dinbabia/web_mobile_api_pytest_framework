"""
Base/Parent page that will be inherited by all pages. These are the main actions of a page.
"""

from my_utils.custom_logger import SingletonLogger

cl = SingletonLogger.get_logger()


class BasePage:

    def __init__(self, page):
        self.page = page

    def check(self, selector):
        """
        Toggle check an element specified by a selector.
        """
        cl.info(f"Toggle radio checkbox: '{selector}'")
        self.page.check(selector)

    def click(self, selector):
        """
        Clicks on an element specified by a selector.
        """
        cl.info(f"Click a button: '{selector}'")
        self.page.click(selector)

    def enter_text(self, selector, text):
        """
        Fills in a text field with the provided text.
        """
        cl.info(f"Enter Text on: '{selector}' | Text Value: '{text}'")
        self.page.fill(selector, text)

    def get_all_elements(self, selector):
        """
        Get all elements using a selector and return it as an element.
        """
        cl.info(f"Getting all the elements from: {selector}")
        return self.page.query_selector_all(selector)

    def get_attribute(self, selector, attribute):
        """
        Gets the value of an attribute of an element.
        """
        cl.info(f"Get attribute on: '{selector}' | Attribute: '{attribute}'")
        result = self.page.get_attribute(selector, attribute)
        cl.info(f"Result Attribute: '{result}'")
        return result

    def get_text(self, selector):
        """
        Retrieves the text content of an element.
        """
        cl.info(f"Get Text on: '{selector}'")
        result = self.page.inner_text(selector)
        cl.info(f"Result Text: '{result}'")
        return result

    def get_title(self):
        """
        Returns the title of the current page.
        """
        result = self.page.title()
        cl.info(f"Get Page Title: '{result}'")
        return result

    def get_url(self):
        """
        Returns the current URL of the page.
        """
        result = self.page.url
        cl.info(f"Get Page URL: '{result}'")
        return result

    def go_back(self):
        """
        Navigates to the previous page in history.
        """
        cl.info("Go Back Page")
        self.page.go_back()

    def go_forward(self):
        """
        Navigates to the next page in history.
        """
        cl.info("Go Forward Page")
        self.page.go_forward()

    def is_visible(self, selector):
        """
        Checks if an element is visible on the page.
        """
        cl.info(f"Check if elemen is visible: '{selector}'")
        result = self.page.is_visible(selector)
        cl.info(f"Result: '{result}'")
        return result

    def navigate(self, url, wait_condition: str = "load"):
        """
        Navigate to a site specified by a url.

         Params
        ----------
            wait_condition (str) ->  Default: load. | Option: 'domcontentloaded' | Check documentation for
                more options but discouraged.
        """
        cl.info(f"Navigate to: '{url}'")
        self.page.goto(url, wait_until=wait_condition)

    def pause_page(self):
        """
        Pause the current page.
        """
        cl.info("Page is paused...")
        self.page.pause()

    def refresh_page(self):
        """
        Reloads the current page.
        """
        cl.info("Page will refresh...")
        self.page.reload()

    def scroll_to_element(self, selector):
        """
        Scrolls the page to make an element visible.
        """
        cl.info(f"Scrolling to element: '{selector}'")
        self.page.eval_on_selector(selector, "element => element.scrollIntoView()")

    def take_screenshot(self, path):
        """
        Takes a screenshot of the current page state.
        """
        cl.info(f"Screenshot taken and saved to: {path}")
        self.page.screenshot(path=path)

    def wait_for_element(self, selector):
        """
        Waits for an element to be present on the page.
        """
        cl.info(f"Wait for element: '{selector}'")
        self.page.wait_for_selector(selector)

    def wait_for_page_load(self):
        """
        Waits for the page to reach the 'load' state.
        """
        cl.info("Wait for page to load.")
        self.page.wait_for_load_state("load")

    def wait_for_seconds(self, seconds):
        cl.info(f"Waiting for {seconds} seconds.")
        self.page.wait_for_timeout(seconds * 1000)
