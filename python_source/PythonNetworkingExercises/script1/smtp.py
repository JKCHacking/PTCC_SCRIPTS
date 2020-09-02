import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

mail_domain = 'smtp.gmail.com'
from_email = 'joshnee.kim.cunanan@gmail.com'
to_email = 'joshnee.kim.cunanan@gmail.com'
smtp_port = 465

server = smtplib.SMTP_SSL(mail_domain, smtp_port)
server.ehlo()

with open('password.txt', 'r') as f:
    password = f.read()

server.login(from_email, password)

msg = MIMEMultipart()
msg['From'] = 'UnknownBot'
msg['To'] = to_email
msg['Subject'] = 'Test'

with open('message.txt', 'r') as f:
    message = f.read()
msg.attach(MIMEText(message, 'plain'))

filename = 'colorful_skull_background.jpg'
attachment = open(filename, 'rb')

pl = MIMEBase('application', 'octet-stream')
pl.set_payload(attachment.read())

encoders.encode_base64(pl)
pl.add_header('Content-Disposition', f'attachment; filename={filename}')
msg.attach(pl)

text = msg.as_string()
server.sendmail(from_email, to_email, text)
server.quit()
