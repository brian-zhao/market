from google.appengine.api import users
from google.appengine.ext import ndb


class UserPrefs(ndb.Model):
  user = ndb.UserProperty(auto_current_user_add=True)


class InboundEmail(ndb.Model):
  mail_from = ndb.StringProperty()
  mail_to = ndb.StringProperty()
  mail_subject = ndb.StringProperty()
  mail_message = ndb.TextProperty()