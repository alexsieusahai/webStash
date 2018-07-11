import multiprocessing as mp
import time

from urllib.parse import urlparse

try:
    from webStash import WebStash
    from config import Config
except (SystemError, ImportError):
    from .webStash import WebStash
    from .config import Config

# maybe a streaming kind of interface is a good idea?
# look to see how people implement streammers, it's a good idea to copy the interface of the popular ones for usability anyways

class WebMine:
    def __init__(self, num_workers, waitTimeBeforeScraping=0):
        self.pool = mp.Pool(num_workers)
        self.config = Config()
        self.waitTimeBeforeScraping = waitTimeBeforeScraping
        self.visitedTimeDict = {}
        self.rateLimit = 1

    def get_batch_web_data(self, url_list):
        results = []
        i = 0
        while len(url_list) > 0:
            webStash = WebStash(getterType='chromedriver', waitTimeBeforeScraping = self.waitTimeBeforeScraping)
            url = url_list[i]
            netloc = urlparse(url).netloc
            # I don't want to be forced to spin up a new WebStash every time...
            # is there a way of having a pool of WebStash objects to work with?
            if netloc in self.visitedTimeDict:
                if url not in webStash.cacher.cacheMap:
                    if time.time() - self.visitedTimeDict[netloc] < self.rateLimit:
                        time.sleep(0.05)
                        continue

            result = self.pool.apply_async(webStash.get_web_data, args=(url,))  # abstracts away the waiting for workers to be ready and everything...
            # maybe look at how apply_async method works under the hood for a better idea of how to design a similar abstraction?
            self.visitedTimeDict[netloc] = time.time()
            results.append(result)
            del url_list[i]
            if len(url_list) == 0:
                break
            i = (i + 1) % len(url_list)
            # maybe move the above into the get_function, and replace get_batch_web_data with get_all?

        outputs = [p.get() for p in results]  # handles zombie processes and et cetera
        return outputs


if __name__ == '__main__':
    webMine = WebMine(2, waitTimeBeforeScraping=2)

    WebStash().clean()

    startTime = time.time()
    url_list = ['https://news.ycombinator.com/news', 'https://news.ycombinator.com/']
    webMine.get_batch_web_data(url_list)
    endTime = time.time()
    assert endTime - startTime > webMine.rateLimit

    # now that those links are hashed...

    startTime = time.time()
    webMine.get_batch_web_data(url_list)
    endTime = time.time()
    assert endTime - startTime < 0.01
