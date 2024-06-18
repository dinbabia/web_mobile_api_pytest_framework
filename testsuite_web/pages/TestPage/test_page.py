from pages.TestPage import test_page_locators as tpl
from pages.base_page import BasePage


class TestPageActions(BasePage):

    def click_submit_button(self):
        self.click(tpl.submit_button)

    def enter_email(self, mobile_number):
        self.enter_text(tpl.email_field, text=mobile_number)

    def enter_password(self, mobile_number):
        self.enter_text(tpl.password_field, text=mobile_number)
