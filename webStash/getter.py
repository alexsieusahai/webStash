from urllib.request import urlopen
from selenium import webdriver

import time

try:
    from exceptions import GetterImplementationError
except (SystemError, ImportError):
    from .exceptions import GetterImplementationError

class Getter:
    def __init__(self, getterType, waitTimeBeforeScraping=0):
        assert isinstance(getterType, str)
        self.getterType = getterType
        self.can_screenshot = False
        self.workers = []
        self.waitTimeBeforeScraping = waitTimeBeforeScraping

        if getterType == 'chromedriver':
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            self.driver = webdriver.Chrome(chrome_options=options)
        if getterType in ['chromedriver']:
            self.can_screenshot = True

    def get_html(self, url):
        if self.getterType == 'urlopen':
            return str(urlopen(url).read())
        if self.getterType == 'chromedriver':
            self.driver.get(url)
            time.sleep(self.waitTimeBeforeScraping)
            return self.driver.page_source

        else:
            raise GetterImplementationError(getterType + ' is not a supported getter type')

    def get_screenshot(self, url, filename):
        if self.can_screenshot:
            if self.getterType == 'chromedriver':
                self.driver.save_screenshot(filename)
                return filename
        else:
            return None


if __name__ == "__main__":

    getter0 = Getter('urlopen')
    html0 = getter0.get_html('https://news.ycombinator.com/news')
    assert isinstance(html0, str)

    getter1 = Getter('chromedriver')
    html1 = getter1.get_html('https://news.ycombinator.com/news')
    assert isinstance(html1, str)

    try:
        errorgetter = Getter('this is not a getter type')
    except GetterImplementationError as e:
        assert str(e) == 'this is not a getter type is not a supported getter type'
