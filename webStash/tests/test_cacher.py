import pytest


import os
import shutil

try:
    from cacher import Cacher
    from exceptions import (SerializerImplementationError, CacheMapError)
except (SystemError, ImportError):
    from .cacher import Cacher
    from .exceptions import (SerializerImplementationError, CacheMapError)

from .urlopen_mockup import urlopen

@pytest.fixture()
def setup():
    try:
        shutil.rmtree('webstashcache')
    except FileNotFoundError:
        pass

    try:
        os.remove('cacheMap.pkl')
    except FileNotFoundError:
        pass
    cacher = Cacher()
    link = 'https://news.ycombinator.com/news'
    return (cacher, link)

def test_cacher_creates_dir():
    os.chdir('tests')
    setup()
    assert os.path.isdir('webstashcache')

def test_cacher_set_get_del():
    (cacher, link) = setup()
    html = urlopen(link)
    cacher[link] = html
    assert link in cacher.cacheMap
    del cacher[link]
    assert link not in cacher.cacheMap

def test_cacher_exceptions():
    (cacher, link) = setup()
    cacher.config.serializer = 'notASerializer'
    try:
        cacher._Cacher__load('something')
    except Exception as e:
        assert isinstance(e, SerializerImplementationError)
    try:
        cacher._Cacher__dump(1, 'something')
    except Exception as e:
        assert isinstance(e, SerializerImplementationError)

def test_teardown():
    setup()
