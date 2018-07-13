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


