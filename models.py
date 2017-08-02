from google.appengine.ext import ndb


class UserPrefs(ndb.Model):
  user = ndb.UserProperty(auto_current_user_add=True)


class shares(ndb.Model):
  code = ndb.StringProperty(required=True)
  desc_full = ndb.StringProperty()
  last_price = ndb.FloatProperty()
  open_price = ndb.FloatProperty()
  day_high_price = ndb.FloatProperty()
  day_low_price = ndb.FloatProperty()
  change_price = ndb.FloatProperty()
  change_in_percent = ndb.StringProperty()
  volume = ndb.IntegerProperty()
  bid_price = ndb.FloatProperty()
  offer_price = ndb.FloatProperty()
  previous_close_price = ndb.FloatProperty()
  previous_day_percentage_change = ndb.StringProperty()
  year_high_price = ndb.FloatProperty()
  last_trade_date = ndb.DateTimeProperty()
  year_high_date = ndb.DateTimeProperty()
  year_low_price = ndb.FloatProperty()
  year_low_date = ndb.DateTimeProperty()
  year_open_date = ndb.DateTimeProperty()
  pe = ndb.FloatProperty()
  eps = ndb.FloatProperty()
  average_daily_volume = ndb.IntegerProperty()
  annual_dividend_yield = ndb.FloatProperty()
  market_cap = ndb.IntegerProperty()
  number_of_shares = ndb.IntegerProperty()
  deprecated_market_cap = ndb.IntegerProperty()
  deprecated_number_of_shares = ndb.IntegerProperty()
  suspended = ndb.BooleanProperty(default=False)
  status = ndb.JsonProperty()

  @classmethod
  def get(cls, code):
    if code:
      return cls.get_by_id(code)

  @classmethod
  def create(cls, **kwargs):
    share = cls.get(kwargs.get('code'))
    if share:
      share.populate(**kwargs)
    else:
      share = shares(id=kwargs.get('code'), **kwargs)
    share.put()
    return share
