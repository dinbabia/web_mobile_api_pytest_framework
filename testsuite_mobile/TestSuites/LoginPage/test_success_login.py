
import pytest
from smart_assertions import soft_assert, verify_expectations

from SingleAction.LoginPage import LoginPageActions


@pytest.mark.run(order=2)
def test_success_login(tap_get_started_button):
    mobile_driver = tap_get_started_button.driver

    login_page_actions = LoginPageActions(mobile_driver)

    login_page_actions.enter_email("email@")
    login_page_actions.enter_password("password")
    login_page_actions.tap_login_button()

    expected_error_message = "Insert Message Here"
    actual_error_msg = "Get success message using Appium"
    soft_assert(expected_error_message == actual_error_msg,
                "[FAIL] '{var1}' != '{var2}'".format(var1=expected_error_message, var2=actual_error_msg))
    verify_expectations()
