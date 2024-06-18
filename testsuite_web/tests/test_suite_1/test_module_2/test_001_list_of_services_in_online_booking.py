
import pytest
from pages.TestPage.test_page import TestPageActions


class TestSample002:

    @pytest.fixture(scope="class")
    def page(self, browser_context):
        # Create a new page for each test class
        page = browser_context.new_page()
        yield page
        page.close()

    def test_001_test_page_002(self, page):
        test_page_action = TestPageActions(page)
        test_page_action.enter_email("Email Here")
        test_page_action.enter_password("Password Here")
        test_page_action.click_submit_button()
        # Insert More Steps and Assertions Here
