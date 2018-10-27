import urllib2
import re
import itertools

def download(url, user_agent='wswp', num_retries=2):
    print 'Downloading: ', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers = headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, user_agent, xnum_retries-1)
    return html

def crawl_sitemap(url):
    # downlaod the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each links
    for link in links:
        html = download(link)
        # scrape html here
        pass
    
def iterdown():
    # maximum number of consecutive download errors allowed
    max_errors = 5
    # current number of consecutive download
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/~%d' % page
        html download(url)