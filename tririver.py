import datetime
import jinja2
import os
import webapp2
import models

from google.appengine.api import users


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
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }
    self.response.out.write(template.render(context))


class RenderServicePage(webapp2.RequestHandler):
  def get(self):
    template = template_env.get_template('service.html')
    self.response.out.write(template.render({}))


class RenderLogisticsPage(webapp2.RequestHandler):
  def get(self):
    template = template_env.get_template('logistics.html')
    self.response.out.write(template.render({}))


class RenderAboutPage(webapp2.RequestHandler):
  def get(self):
    template = template_env.get_template('about-us.html')
    self.response.out.write(template.render({}))


class RenderShopPage(webapp2.RequestHandler):
  def get(self):
    template = template_env.get_template('shop.html')
    self.response.out.write(template.render({}))


application = webapp2.WSGIApplication(
    [('/', MainPage),
     ('/about', RenderAboutPage),
     ('/service', RenderServicePage),
     ('/logistics', RenderLogisticsPage),
     ('/shop', RenderShopPage)], 
    debug=True)
