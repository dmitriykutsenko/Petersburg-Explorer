import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email, subject, text):
    try:
        addr_from = os.getenv("FROM")
        password = os.getenv("PASSWORD")

        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = email
        msg['Subject'] = subject

        body = text
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL(os.getenv('HOST'), os.getenv('PORT'))
        server.login(addr_from, password)

        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print(e)
        return False
