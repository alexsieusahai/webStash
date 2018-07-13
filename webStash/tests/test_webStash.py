from webStash import WebStash
from webData import WebData

def test_get_web_data():
    stash = WebStash(getterType='chromedriver')
    url = 'https://news.ycombinator.com/news'
    wd = stash.get_web_data(url)
    assert isinstance(wd, WebData)
    assert url in stash.cacher.cacheMap
    stash.clean()
