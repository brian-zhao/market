from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import demjson
from urllib2 import Request, urlopen


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
    req = Request(url)
    resp = urlopen(req)
    content_json = demjson.decode(resp.read()[3:])

    return content_json
