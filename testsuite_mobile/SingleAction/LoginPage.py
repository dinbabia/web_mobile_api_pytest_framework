
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from SingleAction.page import Page


class LoginPageVerifications(Page):

    def __init__(self, driver) -> None:
        super().__init__(driver)
        self.driver = driver
        self.platformName = driver.capabilities.get("platformName", None)

    def has_email_field(self):
        locator = {
            "Android": (AppiumBy.XPATH, "//"),
            "IOS": (AppiumBy.CLASS_NAME, "Insert class name here")
        }
        return self.wait.element_is_present(locator=locator[self.platformName])


class LoginPageActions(Page):

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.driver = driver
        self.platformName = driver.capabilities.get("platformName", None)

    def enter_email(self, email):
        locator = {
            "Android": (AppiumBy.XPATH, "// insert xpath here"),
            "IOS": (AppiumBy.CLASS_NAME, "insert class name here")
        }
        self.interaction.input_text(locator=locator[self.platformName], text=email)

    def enter_password(self, password):
        locator = {
            "Android": (AppiumBy.XPATH, "// insert xpath here"),
            "IOS": (AppiumBy.CLASS_NAME, "insert class name here")
        }
        self.interaction.input_text(locator=locator[self.platformName], text=password)

    def tap_login_button(self):
        locator = {
            "Android": (AppiumBy.XPATH, "// insert xpath here"),
            "IOS": (AppiumBy.XPATH, "// insert xpath here")
        }
        self.interaction.click(locator=locator[self.platformName])
