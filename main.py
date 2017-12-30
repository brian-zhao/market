from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import datetime
import jinja2
import json
import models
import os
import urllib
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users
from google_finance import GoogleFinance


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


class MainPage(webapp2.RequestHandler):
  def get(self):
    current_time = datetime.datetime.now()
    user = users.get_current_user()
    if user:
      models.UserPrefs(id=user.user_id()).put()
    login_url = users.create_login_url(self.request.path)
    logout_url = users.create_logout_url(self.request.path)

    template = template_env.get_template('index.html')
    shares = models.shares.query().order(
        -models.shares.annual_dividend_yield).fetch()
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
        'shares': shares,
    }
    self.response.out.write(template.render(context))


# data = models.Prices.query(models.Prices.code =='CBA').fetch()
class RenderPricePage(webapp2.RequestHandler):
  def get(self, code_name):
    current_time = datetime.datetime.now()
    user = users.get_current_user()
    if user:
      models.UserPrefs(id=user.user_id()).put()
    login_url = users.create_login_url(self.request.path)
    logout_url = users.create_logout_url(self.request.path)

    template = template_env.get_template('prices.html')
    share = models.shares.query(
        models.shares.code == code_name).get()
    prices = models.Prices.query(
        models.Prices.code == code_name).order(
            -models.Prices.close_date).fetch()
    g_fin = GoogleFinance()
    news = g_fin.get_news(code_name)
    g_detail = g_fin.get_g_fin_details(code_name)

    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
        'code_name': code_name,
        'prices': prices,
        'share': share,
        'news': news,
        'gd': g_detail[0],
        # 'g_financial': g_detail['financials'][0]
    }
    self.response.out.write(template.render(context))


class RenderServicePage(webapp2.RequestHandler):
  def get(self):
    template = template_env.get_template('service.html')
    self.response.out.write(template.render({}))


class RenderAboutPage(webapp2.RequestHandler):
  def get(self):
    template = template_env.get_template('about-us.html')
    self.response.out.write(template.render({}))


class RenderTechPage(webapp2.RequestHandler):
  def get(self):
    template = template_env.get_template('tech.html')
    self.response.out.write(template.render({}))


class SinglePriceSyncHnadler(webapp2.RequestHandler):
  def get(self, code_name):
    price_syncer = SinglePriceSyncer('asx_price_sync', code_name)
    price_syncer.Run()
    self.response.out.write('ASX price sync id: bla')


class SinglePriceSyncer(object):
  def __init__(self, task_name, code_name):
    self._task_name = task_name
    self.code_name = code_name

  def Run(self):
    url = ('http://data.asx.com.au/data/1/share/%s/prices?' +
           'interval=daily&count=600') % self.code_name
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    entities = []
    for d in data['data']:
      p = models.Prices(
          code=d['code'],
          close_date=datetime.datetime.strptime(
              d['close_date'], '%Y-%m-%dT%H:%M:%S+%f'),
          close_price=d['close_price'],
          change_price=d['change_price'],
          volume=d['volume'],
          day_high_price=d['day_high_price'],
          day_low_price=d['day_low_price'],
          change_in_percent=d['change_in_percent'])
      entities.append(p)
    ndb.put_multi(entities)


class AddCompanyHander(webapp2.RequestHandler):
  def get(self):
    template = template_env.get_template('job_done.html')

    companies = []
    with open('ASXListedCompanies.csv', 'rb') as csvfile:
      code_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
      for row in code_reader:
        data = models.Company(
            compnay_name=row[0],
            asx_code=row[1],
            industry_group_name=row[2])
        companies.append(data)
    ndb.put_multi(companies)
    self.response.out.write(template.render({'job_name': 'add_company'}))


application = webapp2.WSGIApplication(
    [('/', MainPage),
     ('/about', RenderAboutPage),
     ('/service', RenderServicePage),
     ('/tech', RenderTechPage),
     (r'/price/(\w+)', RenderPricePage),
     (r'/single_price_sync/(\w+)', SinglePriceSyncHnadler),
     ('/bz/add_company', AddCompanyHander)],
    debug=True)
