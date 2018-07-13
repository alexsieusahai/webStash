from getter import Getter

def test_getterTypes():
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

def test_getter_wait_before_scraping():
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
