import smtplib
from email.mime.text import MIMEText
from email.header import Header
import decorators

decorators.basicConfig(level=decorators.INFO,
                       filename='/home/hack/log/smtp.log',
                       filemode='a')
coding = 'utf-8'

sender = 'chyson@aliyun.com'
receivers = ['chyson@aliyun.com']

review_link = ''
mail_msg = '<p><a href="{}">Knowledge Review Link</a></p>'.format(review_link)

message = MIMEText(mail_msg, 'html', coding)

message['From'] = Header("Hack Chyson", coding)
message['To'] = Header("Hack Chyson", coding)

subject = 'Knowledge Review'
message['Subject'] = Header(subject, coding)

try:
    smtp_obj = smtplib.SMTP('localhost')
    smtp_obj.sendmail(sender, receivers, message.as_string())
    decorators.info('Email Sent Successfully.')
except smtplib.SMTPException as e:
    decorators.error('Email Sent Failed.')
