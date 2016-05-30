from google.appengine.api import users
from google.appengine.ext import ndb


class UserPrefs(ndb.Model):
  user = ndb.UserProperty(auto_current_user_add=True)
