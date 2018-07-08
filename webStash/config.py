from bs4 import BeautifulSoup

from selenium import webdriver

class ProxyData:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
    #def set_preference(self, 

class Config:
    def __init__(self):
        self.serializer = 'pickle'
        self.getterType = None
        self.proxyList = []

    def setGetterType(self, getterType):
        self.getterType = getterType

    def getFreeProxies(self):
        self.proxyList = []
        freeProxyLink = 'https://free-proxy-list.net/'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(freeProxyLink)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        for tr in soup.select('tr.odd') + soup.select('tr.even'):
            tds = tr.select('td')
            ip_address = tds[0].get_text()
            port = tds[1].get_text()
            aproxy = ProxyData(ip_address, port)
            self.proxyList.append(aproxy)

if __name__ == '__main__':
    cfg = Config()
    cfg.getFreeProxies()
    assert isinstance(cfg.proxyList, list)
    aproxy = cfg.proxyList[0]
    assert isinstance(aproxy, ProxyData)
