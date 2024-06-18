"""
Base Mobile Actions that will be inherited in all TestActions.
"""


from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from abc import ABC, abstractmethod

from my_utils.custom_logger import SingletonLogger


cl = SingletonLogger.get_logger()


class NavigationHandler(ABC):
    @abstractmethod
    def go_to_page(self, page: str):
        pass


class AppiumNavigationHandler(NavigationHandler):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_page(self, page):
        cl.info(f"go_to_page | {page}")
        self.driver.get(page)


class GestureHandler(ABC):
    @abstractmethod
    def swipe_left_to_right(self):
        pass

    @abstractmethod
    def swipe_right_to_left(self):
        pass

    @abstractmethod
    def swipe_top_to_bottom(self):
        pass

    @abstractmethod
    def swipe_bottom_to_up(self):
        pass


class AppiumGestureHandler(GestureHandler):

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self._driver_size = driver.get_window_size()
        self._driver_height = self._driver_size['height']
        self._driver_width = self._driver_size['width']
        self._action = TouchAction(self.driver)

    def _swipe(self, start_point: tuple, end_point: tuple, duration=None):

        self._action.press(x=start_point[0], y=start_point[1]).wait(ms=duration).move_to(x=end_point[0], y=end_point[1]).release().perform()

    def swipe_right_to_left(self):
        start_x = self._driver_width*8/9
        start_y = self._driver_height/2
        end_x = self._driver_width/9
        end_y = self._driver_height/2
        self._swipe(start_point=(start_x, start_y), end_point=(end_x, end_y), duration=500)

    def swipe_left_to_right(self):
        start_x = self._driver_width/9
        start_y = self._driver_height/2
        end_x = self._driver_width*8/9
        end_y = self._driver_height/2
        self._swipe(start_point=(start_x, start_y), end_point=(end_x, end_y), duration=500)

    def swipe_top_to_bottom(self):
        start_x = self._driver_width/2
        start_y = self._driver_height * 2 / 9
        end_x = self._driver_width/2
        end_y = self._driver_height * 8 / 9
        self._swipe(start_point=(start_x, start_y), end_point=(end_x, end_y), duration=500)

    def swipe_bottom_to_up(self):
        start_x = self._driver_width/2
        start_y = self._driver_height * 8 / 9
        end_x = self._driver_width/2
        end_y = self._driver_height / 9
        self._swipe(start_point=(start_x, start_y), end_point=(end_x, end_y), duration=500)


class InteractionHandler(ABC):
    @abstractmethod
    def click(self, locator: tuple):
        pass

    @abstractmethod
    def input_text(self, locator: tuple, text: str):
        pass

    @abstractmethod
    def get_element(self, locator: tuple):
        pass

    @abstractmethod
    def get_elements(self, locator: tuple):
        pass

    @abstractmethod
    def get_element_text(self, locator: tuple):
        pass

    @abstractmethod
    def get_elements_text(self, locator: tuple):
        pass

    @abstractmethod
    def get_element_attribute(self, locator: tuple, attribute: str):
        pass

    @abstractmethod
    def set_default_wait_time(self, wait_time: int):
        pass


class AppiumInteractionHandler(InteractionHandler):
    def __init__(self, driver: WebDriver, default_wait_time=30):
        self.driver = driver
        self.deviceName = driver.capabilities.get("deviceName", "NO DEVICE NAME")
        self.platformName = driver.capabilities.get("platformName", "NO PLATFORM NAME")
        self.default_wait_time = default_wait_time

    def clear_field(self, locator):
        cl.info(f"{self.deviceName} | Clear Field | locator: {locator}")
        WebDriverWait(self.driver, self.default_wait_time).until(EC.element_to_be_clickable(locator)).clear()

    def click(self, locator):
        cl.info(f"{self.deviceName} | click | locator: {locator}")
        WebDriverWait(self.driver, self.default_wait_time).until(EC.element_to_be_clickable(locator)).click()

    def input_text(self, locator, text):
        cl.info(f"{self.deviceName} | input_text | locator: {locator} | text: {text}")
        if self.platformName == "Android":
            self.click(locator=locator)
        WebDriverWait(self.driver, self.default_wait_time).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def _press_search(self):
        self.driver.implicitly_wait(3)
        if self.platformName == 'Android':
            self.driver.execute_script('mobile: performEditorAction', {'action': 'search'})
        elif self.platformName == "IOS":
            self.driver.hide_keyboard('Done')

    def get_element(self, locator):
        cl.info(f"{self.deviceName} | get_element | locator: {locator}")
        return WebDriverWait(self.driver, self.default_wait_time).until(EC.presence_of_element_located(locator))

    def get_elements(self, locator):
        cl.info(f"{self.deviceName} | get_elements | locator: {locator}")
        return WebDriverWait(self.driver, self.default_wait_time).until(EC.presence_of_all_elements_located(locator))

    def get_element_text(self, locator):
        cl.info(f"{self.deviceName} | get_element_text | locator: {locator}")
        return WebDriverWait(self.driver, self.default_wait_time).until(EC.visibility_of_element_located(locator)).text

    def get_elements_text(self, locator):
        cl.info(f"{self.deviceName} | get_elements_text | locator: {locator}")
        text_list = []
        elements = WebDriverWait(self.driver, self.default_wait_time).until(EC.visibility_of_element_located(locator))
        for element in elements:
            text_list.append(element.text)
        return text_list

    def get_element_attribute(self, locator, attribute):
        cl.info(f"{self.deviceName} | get_element_attribute | locator: {locator}")
        element = WebDriverWait(self.driver, self.default_wait_time).until(EC.visibility_of_element_located(locator))
        return element.get_attribute(attribute)

    def set_default_wait_time(self, wait_time):
        cl.info(f"{self.deviceName} | set_default_time | wait_time: {wait_time}")
        self.default_wait_time = wait_time


class WaitHandler(ABC):
    @abstractmethod
    def wait_for_element(self, locator: tuple):
        pass

    @abstractmethod
    def element_is_present(self, locator: tuple):
        pass

    @abstractmethod
    def set_default_timeout(self, timeout: int):
        pass


class AppiumWaitHandler(WaitHandler):
    def __init__(self, driver: WebDriver, default_timeout=30):
        self.driver = driver
        self.deviceName = driver.capabilities.get("deviceName", "NO DEVICE NAME")
        self.default_timeout = default_timeout

    def wait_to_be_invisible(self, locator):
        cl.info(f"{self.deviceName} | wait_to_be_invisible | locator: {locator}")
        WebDriverWait(self.driver, self.default_timeout).until(EC.invisibility_of_element_located(locator))

    def wait_for_element(self, locator):
        cl.info(f"{self.deviceName} | wait_for_element | locator: {locator}")
        WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located(locator))

    def element_is_present(self, locator):
        cl.info(f"{self.deviceName} | wait_for_element | locator: {locator}")
        try:
            WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            cl.info(f"{self.deviceName} | wait_for_element | NOT FOUND")
            return False

    def set_default_timeout(self, timeout):
        self.default_timeout = timeout
