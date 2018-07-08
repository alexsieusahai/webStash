import pickle as pkl
import os
import shutil
import hashlib
import codecs

try:
    from config import Config
except (SystemError, ImportError):
    from .config import Config

try:
    from exceptions import SerializerImplementationError, CacheMapError
except (SystemError, ImportError):
    from .exceptions import SerializerImplementationError, CacheMapError

genNotSupportedStr = lambda astr: astr + ' is not currently supported!'

class Cacher:
    def __init__(self):
        self.config = Config()
        try:
            self.cacheMap = pkl.load(open('cacheMap.pkl', 'rb'))
        except FileNotFoundError:
            self.cacheMap = {}

        if not os.path.isdir(os.getcwd()+'/webstashcache'):
            print('making cache dir...')
            os.mkdir('webstashcache')

    def __getitem__(self, key):
        return self.__load(self.cacheMap[key])

    def __setitem__(self, key, value):
        filename = self.getFilename(key)
        self.cacheMap[key] = filename
        pkl.dump(self.cacheMap, open('cacheMap.pkl', 'wb'))
        self.__dump(value, filename)

    def __delitem__(self, key):
        filename = self.cacheMap[key]
        del self.cacheMap[key]
        pkl.dump(self.cacheMap, open('cacheMap.pkl', 'wb'))
        os.remove(os.getcwd()+'/'+filename)

    def __load(self, filename):
        if self.config.serializer == 'pickle':
            return pkl.load(open(filename, 'rb'))
        else:
            raise SerializerImplementationError(genNotSupportedStr(self.config.serializer))

    def __dump(self, obj, filename):
        if self.config.serializer == 'pickle':
            print('dumping', filename)
            pkl.dump(obj, open(filename, 'wb'))
        else:
            raise SerializerImplementationError(genNotSupportedStr(self.config.serializer))

    def clean(self):
        print('cleaning...')
        try:
            shutil.rmtree('webstashcache')
        except FileNotFoundError:
            print('no webstashcache to remove; doing nothing...')
        try:
            os.remove('cacheMap.pkl')
        except FileNotFoundError:
            print('no cacheMap to remove; doing nothing...')

    def getFilename(self, filename):
        m = hashlib.md5()
        encodedFilename = codecs.encode(filename)
        m.update(encodedFilename)
        return 'webstashcache/'+m.hexdigest()


if __name__ == "__main__":
    import os
    from urllib.request import urlopen

    # core functionality testing
    cacher = Cacher()
    link = 'https://news.ycombinator.com/news'
    html = urlopen(link).read()
    cacher[link] = html
    assert len(cacher.cacheMap) == 1
    test = cacher[link]
    assert test == html
    del cacher[link]
    assert len(cacher.cacheMap) == 0
    cacher.clean()

    # testing getFilename
    assert cacher.getFilename('somefile') == cacher.getFilename('somefile')

    # making sure that my exceptions are being handled properly
    cacher.config.serializer = 'notASerializer'
    try:
        cacher._Cacher__load('something')
    except Exception as e:
        print(type(e))
    try:
        cacher._Cacher__dump(1, 'something')
    except Exception as e:
        print(type(e))
