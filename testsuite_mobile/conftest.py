import pytest
import subprocess
import shutil
import time
import os

from appium import webdriver
from abc import ABC, abstractmethod


def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Appium Server Starting in: {time_format}\n", end='\r')
        time.sleep(1)
        seconds -= 1


@pytest.fixture(scope="session")
def mobile_driver_session(appium_server_session, set_device_capabilities):
    mobile_driver = MobileDriver(capabilities=set_device_capabilities, host_address="http://127.0.0.1", port="4723")
    mobile_driver.build_driver()

    yield mobile_driver

    mobile_driver.quit_driver()


@pytest.fixture(scope="session")
def appium_server_session():
    SystemCheckAppium.has_the_library_name_installed(library_name='appium')
    appium_server = AppiumServer(port="4723")
    appium_server.start_server_in_new_terminal()
    yield
    appium_server.close_the_terminal_gracefully()


class SystemCheck(ABC):

    @staticmethod
    @abstractmethod
    def has_the_library_name_installed(library_name: str):
        pass


class SystemCheckAppium(SystemCheck):

    @staticmethod
    def has_the_library_name_installed(library_name: str):
        if shutil.which(library_name) is None:
            pytest.exit(f"Error: '{library_name}' is not installed or available in the system.", returncode=1)


class AppiumServer:
    def __init__(self, port) -> None:
        self._port = port
        self._start_appium_countdown_secs = 5

    def start_server_in_new_terminal(self):
        # This works for macOS only since we need both iOS and android to test.
        subprocess.Popen(['osascript', '-e', f'''
            tell application "Terminal"
                set serverWindow to do script "appium --allow-cors -p {self._port}"
                set custom title of serverWindow to "appium_server"
            end tell
        '''])
        countdown(self._start_appium_countdown_secs)

    def close_the_terminal_gracefully(self):
        process = self._grep_appium_process()
        for pid in process.stdout.splitlines():
            try:
                os.kill(int(pid), 15)  # 15-SIGTERM the process. Exit gracefully and clean up resources before exit.
                subprocess.Popen(['osascript', '-e', 'tell app "Terminal" to close (every window whose name contains "appium")'])
            except Exception as e:
                print(f"Failed to terminate Appium server process with PID {pid}: {e}")

    def _grep_appium_process(self):
        return subprocess.run(['pgrep', '-f', f'appium --allow-cors -p {self._port}'], capture_output=True, text=True)


@pytest.fixture(scope="session")
def set_device_capabilities(request):
    device_type = request.config.getoption("--device-type")
    device_name = request.config.getoption("--device-name")
    return select_device_capability_choice(device_type=device_type, device_name=device_name)


def select_device_capability_choice(device_type, device_name):
    if device_type == 'android':
        return AndroidDeviceCapabilities(device_name=device_name)
    elif device_type == 'ios':
        return IOSDeviceCapabilities(device_name=device_name)
    else:
        raise RuntimeError(f"'{device_type}' given is not found.")


def pytest_addoption(parser):
    parser.addoption("--device-type", action="store", default="android", help="Type of Device :[android, ios]")
    parser.addoption("--device-name", action="store", default="emulator-xxxx", help="Default Device Name should be running.")


class DeviceCapabilities:
    def __init__(self, device_name: str) -> None:
        setattr(self, "appium:appPackage", "insert app package here")
        setattr(self, "appium:appWaitActivity", "insert main activity here")
        setattr(self, "appium:deviceName", device_name)

    def __call__(self):
        return self.__dict__


class AndroidDeviceCapabilities(DeviceCapabilities):
    def __init__(self, device_name: str) -> None:
        super().__init__(device_name)
        setattr(self, "platformName", "Android")
        setattr(self, "appium:automationName", "UIAutomator2")
        setattr(self, "platformVersion", "12")
        setattr(self, "appium:app", os.path.join(os.getcwd(), '..', '_apk', 'insert name here.apk'))
        setattr(self, "unicodeKeyboard", False)
        setattr(self, "resetKeyboard", False)


class IOSDeviceCapabilities(DeviceCapabilities):
    def __init__(self, device_name: str) -> None:
        super().__init__(device_name)
        setattr(self, "platformName", "IOS")
        setattr(self, "appium:automationName", "XCUITest")
        setattr(self, "appium:app", "//Insert Name Project.app")
        setattr(self, "unicodeKeyboard", False)
        setattr(self, "resetKeyboard", False)


class MobileDriver:
    def __init__(self, capabilities, host_address: str, port: str) -> None:
        self.capabilities = capabilities
        self._host_address = host_address
        self._port = port

    def get_mobile_driver_address(self):
        return f"{self._host_address}:{self._port}"

    def build_driver(self):
        self.driver = webdriver.Remote(f"{self._host_address}:{self._port}", self.capabilities())

    def quit_driver(self):
        self.driver.quit()
