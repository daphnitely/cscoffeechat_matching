import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
# TODO: replace with the official cs coffee chat email and update API key
from_email = "example@gmail.com"
to_email = "example@gmail.com"
subject = "Sending with SendGrid is Fun"
content = "<strong>and easy to do anywhere, even with Python</strong>"
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)