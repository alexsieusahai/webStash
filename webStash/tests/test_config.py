import pytest

try:
    from config import (Config, ProxyData)
except (SystemError, ImportError):
    from .config import (Config, ProxyData)

def test_setGetterType():
    cfg = Config()
    cfg.setGetterType('chromedriver')
    assert cfg.getterType == 'chromedriver'

def test_getFreeProxies():
    cfg = Config()
    cfg.getFreeProxies()
    assert len(cfg.proxyList) > 0
