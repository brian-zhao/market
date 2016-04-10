import logging
import webapp2
import models

from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


class LogSenderHandler(InboundMailHandler):
  def receive(self, mail_message):
    logging.info("Received a message from: " + mail_message.sender)
    plaintext_bodies = mail_message.bodies('text/plain')
    html_bodies = mail_message.bodies('text/html')
    decoded_html = ''
    for content_type, body in html_bodies:
        decoded_html = body.decode()

    models.InboundEmail(
        mail_from=mail_message.sender,
        mail_to=mail_message.to,
        mail_subject=mail_message.subject,
        mail_message=decoded_html).put()

app = webapp2.WSGIApplication(
  [('/_ah/mail/.+', LogSenderHandler)], debug=True)
