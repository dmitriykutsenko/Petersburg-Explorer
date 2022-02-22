import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email, subject, text, from_yandex=False, from_second=False):
    try:
        if from_yandex:
            addr_from = os.getenv('YANDEX_FROM')
            password = os.getenv('YANDEX_PASSWORD')
            host = os.getenv('YANDEX_HOST')

        elif from_second:
            addr_from = os.getenv("FROM2")
            password = os.getenv("PASSWORD2")
            host = os.getenv('HOST')

        else:
            addr_from = os.getenv("FROM")
            password = os.getenv("PASSWORD")
            host = os.getenv('HOST')

        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = email
        msg['Subject'] = subject

        body = text
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL(host, os.getenv('PORT'))
        server.login(addr_from, password)

        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print(e)
        return False
