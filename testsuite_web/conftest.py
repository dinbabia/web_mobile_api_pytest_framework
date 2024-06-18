"""
Setup for Mobile-Web Test Suite.
"""

import pytest
from tkinter import Tk
from playwright.sync_api import sync_playwright


root = Tk()


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": root.winfo_screenwidth(),
            "height": root.winfo_screenheight()
        }
    }


@pytest.fixture(scope="function")
def browser(browser):
    """
    Browser scope of Playwright. To add a new page, use the following code below.
    Use this fixture if you want to create new tabs in the same browser.

     Use Example
    ----------
    >>> from pages.sample_page import SamplePage
    >>> def test_browser_fixture(browser):
    >>>     context = browser.new_context()
    >>>     page1 = SamplePage(context.new_page())
    >>>     page1.navigate('https://google.com')
    >>>     page2 = SamplePage(context.new_page())
    >>>     page2.navigate('https://facebook.com')
    """
    yield browser


@pytest.fixture(scope="function")
def page(browser):
    """
    Direct page scope of Playwright. We need to

     Use Example
    ---------
    >>> from pages.sample_page import SamplePage
    >>> def test_page_fixture(page):
    >>>     samplePage = SamplePage(page)
    >>>     samplePage.navigate('https://facebook.com')
    """
    with browser.new_page() as page:
        yield page


@pytest.fixture(scope="class")
def browser_context():
    with sync_playwright() as p:
        # browser = p.chromium.launch()
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        context.add_cookies([
            {"name": "test_cookie",
             "value": "1234",
             "domain": "test.test",
             "path": "/"}
        ])

        yield context
        context.close()
        browser.close()
