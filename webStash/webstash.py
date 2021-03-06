import os

from urllib.request import urlopen

try:
    from config import Config
    from cacher import Cacher
    from webData import WebData
    from getter import Getter
    from exceptions import GetterImplementationError
except (SystemError, ImportError):
    from .config import Config
    from .cacher import Cacher
    from .webData import WebData
    from .getter import Getter
    from .exceptions import GetterImplementationError

class WebStash:
    def __init__(self, getterType='urlopen', waitTimeBeforeScraping=0):
        self.cacher = Cacher()
        self.config = Config()
        self.getter = Getter(getterType, waitTimeBeforeScraping=waitTimeBeforeScraping)

    def get_web_data(self, url):
        try:
            return self.cacher[url]
        except KeyError:
            self.config.debugPrint('Getting webData...')
            filename= self.cacher.getFilename(url)
            html = self.getter.get_html(url)
            screenshotLocation = self.getter.get_screenshot(url, filename+'.png')
            webData = WebData(
                    filename,
                    url,
                    html,
                    screenshotLocation=screenshotLocation
                    )
            self.cacher[url] = webData
            return self.cacher[url]

    def delete(url):
        del self.cacher[url]

    def clean(self):
        self.cacher.clean()

