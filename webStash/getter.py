from urllib.request import urlopen
from selenium import webdriver

import time
import requests

try:
    from exceptions import GetterImplementationError
    from config import Config
except (SystemError, ImportError):
    from .exceptions import GetterImplementationError
    from .config import Config

class Getter:
    def __init__(self, getterType, waitTimeBeforeScraping=0):
        assert isinstance(getterType, str)
        self.getterType = getterType
        self.can_screenshot = False
        self.workers = []
        cfg = Config()
        self.waitTimeBeforeScraping = cfg.waitTimeBeforeScraping

        if getterType in ['chromedriver']:
            self.can_screenshot = True

    def get_html(self, url):
        if self.getterType == 'urlopen':
            req = urlopen(url)
            time.sleep(self.waitTimeBeforeScraping)
            return req.read()

        if self.getterType == 'chromedriver':
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            self.driver = webdriver.Chrome(chrome_options=options)
            self.driver.get(url)
            time.sleep(self.waitTimeBeforeScraping)
            return self.driver.page_source

        if self.getterType == 'requests':
            r = requests.get(url)
            time.sleep(self.waitTimeBeforeScraping)
            return r.content

        else:
            raise GetterImplementationError(getterType + ' is not a supported getter type')

    def get_screenshot(self, url, filename):
        return None
        if self.can_screenshot:
            if self.getterType == 'chromedriver':
                self.driver.save_screenshot(filename)
                return filename
        else:
            return None


if __name__ == "__main__":

    testurl = 'https://news.ycombinator.com/news'
    getter0 = Getter('urlopen')
    html0 = getter0.get_html(testurl)
    assert isinstance(html0, bytes)

    getter1 = Getter('chromedriver')
    html1 = getter1.get_html(testurl)
    assert isinstance(html1, str)

    getter2 = Getter('requests')
    html2 = getter2.get_html(testurl)
    assert isinstance(html2, bytes)

    import datetime
    waitTimeBeforeScraping = 1
    testSleep = Getter('urlopen', waitTimeBeforeScraping=waitTimeBeforeScraping)
    startTime = datetime.datetime.now()
    for i in range(3):
        testSleep.get_html('https://news.ycombinator.com/news')

    endTime = datetime.datetime.now()

    assert (endTime - startTime).seconds > 3 * waitTimeBeforeScraping


    try:
        errorgetter = Getter('this is not a getter type')
    except GetterImplementationError as e:
        assert str(e) == 'this is not a getter type is not a supported getter type'
