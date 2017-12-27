from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import holidays
import json
import logging
import models
import urllib
import webapp2

from google.appengine.api import taskqueue
from google.appengine.ext import ndb

ASX_200 = ['A2M', 'AAC', 'AAD', 'ABC', 'ABP', 'ACX', 'AGL', 'AHG', 'AHY', 'ALL',
           'ALQ', 'ALU', 'AMC', 'AMP', 'ANN', 'ANZ', 'AOG', 'APA', 'API', 'APO',
           'ARB', 'AST', 'AWC', 'AZJ', 'BAP', 'BEN', 'BGA', 'BHP', 'BKL', 'BKW',
           'BLD', 'BOQ', 'BPT', 'BRG', 'BSL', 'BTT', 'BWP', 'BXB', 'CAR', 'CBA',
           'CCL', 'CCP', 'CGC', 'CGF', 'CHC', 'CIM', 'CMW', 'CNU', 'COH', 'CPU',
           'CQR', 'CSL', 'CSR', 'CTD', 'CTX', 'CWN', 'CWY', 'CYB', 'DLX', 'DMP',
           'DOW', 'DXS', 'ECX', 'EHE', 'EVN', 'FBU', 'FLT', 'FMG', 'FPH', 'FXJ',
           'FXL', 'GEM', 'GMA', 'GMG', 'GNC', 'GOZ', 'GPT', 'GTY', 'GUD', 'GWA',
           'GXL', 'GXY', 'JHG', 'HSO', 'HT1', 'HVN', 'IAG', 'IFL', 'IFN', 'IGO',
           'ILU', 'INM', 'IOF', 'IPH', 'IPL', 'IRE', 'ISD', 'IVC', 'JBH', 'JHC',
           'JHX', 'LLC', 'LNK', 'MFG', 'MGR', 'MIN', 'MMS', 'MND', 'MPL', 'MQA',
           'MQG', 'MTR', 'MTS', 'MYO', 'MYR', 'MYX', 'NAB', 'NAN', 'NCM', 'NEC',
           'NSR', 'NST', 'NUF', 'NVT', 'NWS', 'NXT', 'ORA', 'ORE', 'ORG', 'ORI',
           'OSH', 'OZL', 'PGH', 'PMV', 'PPT', 'PRY', 'PTM', 'QAN', 'QBE', 'QUB',
           'REA', 'REG', 'RFG', 'RHC', 'RIO', 'RMD', 'RRL', 'RSG', 'RWC', 'S32',
           'SAR', 'SBM', 'SCG', 'SCP', 'SDA', 'SDF', 'SEK', 'SFR', 'SGM', 'SGP',
           'SGR', 'SHL', 'SIG', 'SKC', 'SKI', 'SKT', 'SPK', 'SPO', 'SRX', 'STO',
           'STW', 'SUL', 'SUN', 'SVW', 'SWM', 'SXL', 'SYD', 'SYR', 'TAH', 'TCL',
           'TGR', 'TLS', 'TME', 'TNE', 'TPM', 'TTS', 'TWE', 'VCX', 'VOC', 'VRT',
           'VVR', 'WBC', 'WEB', 'WES', 'WFD', 'WHC', 'WOR', 'WOW', 'WPL', 'WSA']
AU_HOLIDAYS = holidays.AU(prov='NSW')


class AsxCodeSyncHandler(webapp2.RequestHandler):
  def get(self):
    taskqueue.add(
        queue_name='CodeSync',
        url='/admin/run_code_sync',
        method='GET')
    self.response.out.write('Code Sync: Queued')


class RunCodeSyncHnadler(webapp2.RequestHandler):
  def get(self):
    code_syncer = CodeSyncer('asx_code_sync')
    code_syncer.Run()
    self.response.out.write('ASX code sync id: bla')


class AsxPriceSyncHandler(webapp2.RequestHandler):
  def get(self):
    taskqueue.add(
        queue_name='PriceSync',
        url='/admin/run_price_sync',
        method='GET')
    self.response.out.write('Price Sync: Queued')


class RunPriceSyncHnadler(webapp2.RequestHandler):
  def get(self):
    price_syncer = PriceSyncer('asx_price_sync')
    price_syncer.Run()
    self.response.out.write('ASX price sync id: bla')


class AsxCompanySyncHandler(webapp2.RequestHandler):
  def get(self):
    taskqueue.add(
        queue_name='CompanySync',
        url='/admin/run_company_sync',
        method='GET')
    self.response.out.write('Company Sync: Queued')


class RunCompanySyncHandler(webapp2.RequestHandler):
  def get(self):
    company_syncer = CompanySyncer('asx_company_sync')
    company_syncer.Run()
    self.response.out.write('ASX company sync done.')


class CompanySyncer(object):
  def __init__(self, task_name):
    self._task_name = task_name

  def Run(self):
    for code in ASX_200:
      url = 'http://data.asx.com.au/data/1/company/%s' % code
      response = urllib.urlopen(url)
      data = json.loads(response.read())
      models.shares.create(
          code=data['code'],
          name_full=data['name_full'],
          name_short=data['name_short'],
          name_abbrev=data['name_abbrev'],
          principal_activities=data['principal_activities'],
          industry_group_name=data['industry_group_name'],
          sector_name=data['sector_name'],
          listing_date=(
              datetime.datetime.strptime(
                  data['listing_date'], '%Y-%m-%dT%H:%M:%S+%f')
              if data['listing_date'] else None),
          delisting_date=(
              datetime.datetime.strptime(
                  data['delisting_date'], '%Y-%m-%dT%H:%M:%S+%f')
              if data['delisting_date'] else None),
          web_address=data['web_address'],
          mailing_address=data.get('mailing_address', ''),
          phone_number=data.get('phone_number', ''),
          fax_number=data.get('fax_number', ''),
          registry_name=data.get('registry_name', ''),
          registry_address=data.get('registry_address', ''),
          registry_phone_number=data.get('registry_phone_number', ''),
          foreign_exempt=(
              bool(data['foreign_exempt'])
              if data['foreign_exempt'] else False),
          investor_relations_url=data['investor_relations_url'],
          primary_share_code=data['primary_share_code'],
          recent_announcement=(
              bool(data['recent_announcement'])
              if data['recent_announcement'] else False),
          products=data['products'])


class PriceSyncer(object):
  def __init__(self, task_name):
    self._task_name = task_name

  def Run(self):
    if datetime.datetime.today() in AU_HOLIDAYS:
      return

    for code in ASX_200:
      url = ('http://data.asx.com.au/data/1/share/%s/prices?' +
             'interval=daily&count=1') % code
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


class CodeSyncer(object):
  def __init__(self, task_name):
    self._task_name = task_name

  def Run(self):
    if datetime.datetime.today() in AU_HOLIDAYS:
      return

    for code in ASX_200:
      url = 'http://data.asx.com.au/data/1/share/%s/' % code
      response = urllib.urlopen(url)
      data = json.loads(response.read())
      logging.info('processing %s', code)
      models.shares.create(
        code=data['code'],
        desc_full=data['desc_full'],
        last_price=data['last_price'],
        open_price=data['open_price'],
        day_high_price=data['day_high_price'],
        day_low_price=data['day_low_price'],
        change_price=data['change_price'],
        change_in_percent=data['change_in_percent'],
        volume=data['volume'],
        bid_price=data['bid_price'],
        offer_price=data['offer_price'],
        previous_close_price=data['previous_close_price'],
        previous_day_percentage_change=data['previous_day_percentage_change'],
        year_high_price=data['year_high_price'],
        last_trade_date=datetime.datetime.strptime(
            data['last_trade_date'], '%Y-%m-%dT%H:%M:%S+%f'),
        year_high_date=datetime.datetime.strptime(
            data['year_high_date'], '%Y-%m-%dT%H:%M:%S+%f'),
        year_low_price=data['year_low_price'],
        year_low_date=datetime.datetime.strptime(
            data['year_low_date'], '%Y-%m-%dT%H:%M:%S+%f'),
        year_open_date=(
            datetime.datetime.strptime(
                data['year_open_date'], '%Y-%m-%dT%H:%M:%S+%f')
            if data['year_open_date'] else None),
        pe=data['pe'],
        eps=data['eps'],
        average_daily_volume=data['average_daily_volume'],
        annual_dividend_yield=data['annual_dividend_yield'],
        market_cap=data.get('market_cap', 0),
        number_of_shares=data.get('number_of_shares', 0),
        deprecated_market_cap=data.get('deprecated_market_cap', 0),
        deprecated_number_of_shares=data.get('deprecated_number_of_shares', 0),
        suspended=data['suspended'],
        status=data['status'])


application = webapp2.WSGIApplication(
    [('/admin/asx_code_sync', AsxCodeSyncHandler),
     ('/admin/run_code_sync', RunCodeSyncHnadler),
     ('/admin/asx_price_sync', AsxPriceSyncHandler),
     ('/admin/run_price_sync', RunPriceSyncHnadler),
     ('/admin/asx_company_sync', AsxCompanySyncHandler),
     ('/admin/run_company_sync', RunCompanySyncHandler)],
    debug=True)
