from src.base.browser import Browser


class BasePage(object):
    def __init__(self):
        self.browser = Browser
        self.page_elements = ['el1','el2','el3']