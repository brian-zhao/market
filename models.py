from google.appengine.ext import ndb


class UserPrefs(ndb.Model):
  user = ndb.UserProperty(auto_current_user_add=True)


class Company(ndb.Model):
  compnay_name = ndb.StringProperty(required=True)
  asx_code = ndb.StringProperty(required=True)
  industry_group_name = ndb.StringProperty()


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

  name_full = ndb.StringProperty()
  name_short = ndb.StringProperty()
  name_abbrev = ndb.StringProperty()
  principal_activities = ndb.StringProperty()
  industry_group_name = ndb.StringProperty()
  sector_name = ndb.StringProperty()
  listing_date = ndb.DateTimeProperty()
  delisting_date = ndb.DateTimeProperty()
  web_address = ndb.StringProperty()
  mailing_address = ndb.StringProperty()
  phone_number = ndb.StringProperty()
  fax_number = ndb.StringProperty()
  registry_name = ndb.StringProperty()
  registry_address = ndb.StringProperty()
  registry_phone_number = ndb.StringProperty()
  foreign_exempt = ndb.BooleanProperty()
  investor_relations_url = ndb.StringProperty()
  primary_share_code = ndb.StringProperty()
  recent_announcement = ndb.BooleanProperty()
  products = ndb.JsonProperty()

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


class Prices(ndb.Model):
  code = ndb.StringProperty(required=True)
  close_date = ndb.DateTimeProperty()
  close_price = ndb.FloatProperty()
  change_price = ndb.FloatProperty()
  volume = ndb.IntegerProperty()
  day_high_price = ndb.FloatProperty()
  day_low_price = ndb.FloatProperty()
  change_in_percent = ndb.StringProperty()

  @classmethod
  def get(cls, code):
    if code:
      return cls.query().order(cls.close_date).fetch()

  @classmethod
  def create(cls, **kwargs):
    price = Prices(**kwargs)
    price.put()
    return price
