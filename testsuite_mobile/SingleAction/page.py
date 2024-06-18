from core.MobileActions import AppiumInteractionHandler, AppiumNavigationHandler, AppiumGestureHandler, AppiumWaitHandler


class Page:
    def __init__(self, driver) -> None:
        self.interaction = AppiumInteractionHandler(driver)
        self.navigation = AppiumNavigationHandler(driver)
        self.gesture = AppiumGestureHandler(driver)
        self.wait = AppiumWaitHandler(driver)
