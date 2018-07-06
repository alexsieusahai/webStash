import multiprocessing as mp

try:
    from webStash import WebStash
    from config import Config
except (SystemError, ImportError):
    from .webStash import WebStash
    from .config import Config

class WebTrove:
    def __init__(self, num_workers):
        self.pool = mp.Pool(num_workers)
        self.config = Config()
        self.cacher = Cacher()

    def get_batch_html(self, url_list):
        results = [self.pool.apply_async(WebStash().get_web_data, args=(url,)) for url in url_list]
        outputs = [p.get() for p in results]
        return outputs

if __name__ == '__main__':
    webTrove = WebTrove(2)
    print(webTrove.get_batch_html(['https://www.google.com', 'https://news.ycombinator.com/news']))
