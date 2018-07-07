# webStash

# Use Case
This package is intended as a tool to help the scraping process by caching the html and other stuff such as screenshots, if available.

# Installation
This package is available on `pypi`. So, to install,
```bash
sudo pip3 install webStash
```

# Examples
This is probably the most general use case:
```python
from bs4 import BeautifulSoup
import webStash

stash = webStash.WebStash()
web_data = stash.get_web_data('https://news.ycombinator.com')
html = web_data.html
```
If you do this, consequent calls of `stash.get_web_data('https://news.ycombinator.com')` will grab the stashed `WebData` object. The next most common thing would be deleting `https://news.ycombinator.com` from the cache. This is how you would do this:
```python
import webStash

stash = webStash.WebStash()
stash.delete('https://news.ycombinator.com')
```
