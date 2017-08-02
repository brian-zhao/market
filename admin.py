from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import webapp2
import urllib
import json
import thread
import models
from google.appengine.api import taskqueue

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


class AsxCodeSyncHandler(webapp2.RequestHandler):
  def get(self):
    taskqueue.add(
        queue_name='CodeSync',
        url='/admin/run_code_sync',
        method='GET')
    self.response.out.write('Code Sync: Queued')


class RunCoeeSyncHnadler(webapp2.RequestHandler):
  def get(self):
    code_syncer = CodeSyncer('asx_code_sync')
    tid = thread.start_new_thread(code_syncer.Run, [])
    self.response.out.write('ASX code sync id: %s' % tid)


class CodeSyncer(object):
  def __init__(self, task_name):
    self._task_name = task_name

  def Run(self):
    for code in ASX_200:
      url = "http://data.asx.com.au/data/1/share/%s/" % code
      response = urllib.urlopen(url)
      data = json.loads(response.read())
      print(code)
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
     ('/admin/run_code_sync', RunCoeeSyncHnadler)],
    debug=True)
