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
        while True:
            try:
                self.cacheMap = pkl.load(open('cacheMap.pkl', 'rb'))
                break
            except FileNotFoundError:
                self.cacheMap = {}
                break
            except EOFError:  # bad hack, should use a lock object on cacheMap instead
                time.sleep(0.05)

        if not os.path.isdir(os.getcwd()+'/webstashcache'):
            self.config.debugPrint('making cache dir...')
            os.mkdir('webstashcache')

    def __getitem__(self, key):
        return self.__load(self.cacheMap[key])

    def __setitem__(self, key, value):
        filename = self.getFilename(key)
        self.cacheMap[key] = filename
        self.__dump(value, filename)
        pkl.dump(self.cacheMap, open('cacheMap.pkl', 'wb'))

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
            self.config.debugPrint('dumping', filename)
            pkl.dump(obj, open(filename, 'wb'))
        else:
            raise SerializerImplementationError(genNotSupportedStr(self.config.serializer))

    def clean(self):
        self.config.debugPrint('cleaning...')
        try:
            shutil.rmtree('webstashcache')
        except FileNotFoundError:
            self.config.debugPrint('no webstashcache to remove; doing nothing...')
        try:
            os.remove('cacheMap.pkl')
        except FileNotFoundError:
            self.config.debugPrint('no cacheMap to remove; doing nothing...')

    def getFilename(self, filename):
        m = hashlib.md5()
        encodedFilename = codecs.encode(filename)
        m.update(encodedFilename)
        return 'webstashcache/'+m.hexdigest()

