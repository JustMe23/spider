import urllib2
import re
import itertools
import urlparse
import robotparser

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
        html = download(url)
        if html is None:
            # receive an error trying to download this webpage
            num_errors += 1
            if num_errors == max_errors:
                ## reached maximum number of consecutive errors so exit
                break
            else:
                # success - can scrape the result
                # ...
                num_errors = 0

def link_crawler(seed_url, link_regex):
    ''' Crawl from the given seed URL following links matched by link_regex'''
    rp = robotparser.RobotFileParser()
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        rp.set_url(url+'/robots.txt')
        rp.read()
        user_agent = 'GoodCrawler'
        # check url passes robts.txt restrictions
        if rp.can_fetch(user_agent, url):
            html = download(url)
            # filter for links matching our regular expressin
            for link in get_links(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
                 # check if have already seen this link
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
        else:
            print('Blocked by robots.txt:', url)

def get_links(html):
    '''Return a list of links from html'''
    # A regular exprssion to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)
