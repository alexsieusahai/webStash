try:
    from cacher import Cacher
    from config import Config
    from getter import Getter
    from webData import WebData
    from webStash import WebStash
    from webMine import WebMine
except (SystemError, ImportError):
    from .cacher import Cacher
    from .config import Config
    from .getter import Getter
    from .webData import WebData
    from .webStash import WebStash
    from .webMine import WebMine
