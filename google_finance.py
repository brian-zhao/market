from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import demjson
import urllib2
from urllib2 import Request, urlopen

from urllib3 import PoolManager
from urllib3.contrib.appengine import AppEngineManager, is_appengine_sandbox


class GoogleFinance(object):
  def __init__(self):
    pass

  def build_news_url(self, code):
    return ('http://finance.google.com/finance/company_news?output=json&q=ASX:' +
            code + '&start=0&num=1000')

  def build_company_url(self, code):
    return ('http://finance.google.com/finance?output=json&q=ASX:' + code)

  def get_news(self, code):
    """Get the ASX code related new from Google news API.

    Returns:
      A list of news dictionary, list of dict keys:
        - usg: n/a.
        - sru: Search Result url.
        - tt: Time stamp.
        - d: How old the news.
        - t: Title.
        - s: Source.
        - sp: First paragraph.
        - u: Source url.
    """

    url = self.build_news_url(code)
    req = Request(url)
    resp = urlopen(req)
    content_json = demjson.decode(resp.read())

    article_json = []
    news_json = content_json['clusters']
    for cluster in news_json:
        for article in cluster:
            if article == 'a':
                article_json.extend(cluster[article])

    return article_json

  def get_g_fin_details(self, code):
    url = self.build_company_url(code)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    content_json = demjson.decode(response.read()[3:])

    # if is_appengine_sandbox():
    #   # AppEngineManager uses AppEngine's URLFetch API behind the scenes
    #   http = AppEngineManager()
    # else:
    #   # PoolManager uses a socket-level API behind the scenes
    #   http = PoolManager()
    # page = http.request('GET', url, preload_content=False)
    # logging.info(page.read())
    # content_json = demjson.decode(page.read()[3:])
    return content_json
