#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import Story
from django.utils import timezone
#https://docs.djangoproject.com/en/2.0/topics/email/#django.core.mail.backends.smtp.EmailBackend
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_mail(html, destination):
   #gmail_pwd =  ''
# me == my email address
# you == recipient's email address
   #me = "colouredsweat@gmail.com"
  

   #smtpserver = smtplib.SMTP("smtp.gmail.com",587)
   #smtpserver.ehlo()
   #smtpserver.starttls()
   #smtpserver.ehlo
   #smtpserver.login(me, gmail_pwd)
   #header = 'To:' + destination.email + '\n' + 'From: ' + me + '\n' + 'Subject:Coloured Sweat \n'
   #print header

# Create message container - the correct MIME type is multipart/alternative.
   subject, from_email, to = 'Coloured Sweat', 'colouredsweat@gmail.com', destination.email
   html_content = render_to_string('/home/formigol/public_html/static/templates/contacts/email_send.html', {'contact': 'hiii'}) # ...
   text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
   msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
   msg.attach_alternative(html_content, "text/html")
   msg.send()
   
   #msg = MIMEMultipart('alternative')
   #msg['Subject'] = "Coloured Sweat"
   #msg['From'] = me
   #msg['To'] = destination.email

# Create the body of the message (a plain-text and an HTML version).
   #text = 'hey'

# Record the MIME types of both parts - text/plain and text/html.
   #part1 = MIMEText(text, 'plain')
   #part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
   #msg.attach(part1)
   #msg.attach(part2)

   #smtpserver.sendmail(me, destination.email,  msg.as_string())
   #print 'done!'
   #smtpserver.close()

# Save in the database the basic info about the sended mail
   story_record = Story(contact=destination, date_of_dispatch =timezone.now(),
			via_email_contact = True)
   story_record.save()


# Send the message via local SMTP server.
#s = smtplib.SMTP('localhost')
#sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
#s.sendmail(me, you, msg.as_string())
#s.quit()
