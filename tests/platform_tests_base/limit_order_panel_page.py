from tests.platform_tests_base.base_page import BasePage
from tests.platform_tests_base.locators import limit_order_panel_locators


class LimitOrderPanelPage(BasePage):
    
    def __init__(self):
        super(LimitOrderPanelPage, self).__init__()
        self.locators = limit_order_panel_locators
