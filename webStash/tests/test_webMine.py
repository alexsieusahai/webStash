from webStash import WebStash
from webMine import WebMine

import time

def test_concurrency():
    webMine = WebMine(2, waitTimeBeforeScraping=2)

    WebStash().clean()

    startTime = time.time()
    url_list = ['https://news.ycombinator.com/news', 'https://news.ycombinator.com/']
    webMine.get_batch_web_data(url_list)
    endTime = time.time()
    assert endTime - startTime > webMine.rateLimit

    startTime = time.time()
    webMine.get_batch_web_data(url_list)
    endTime = time.time()
    assert endTime - startTime < 0.01
