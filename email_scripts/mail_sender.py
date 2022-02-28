from __future__ import print_function
import os
from pprint import pprint

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def send_email(email, verification_code):
    api_key = os.getenv("SEND_IN_BLUE_KEY")
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "Регистрация в Petersburg Explorer"

    html_content = f"<html><body><h1>" \
                   "Здравствуйте, кто-то пытается зарегистрироваться в Petersburg Explorer, используя данный email-адрес." \
                   f"Если это вы, используйте следующий код для подтверждения регистрации: {verification_code}" \
                   "</h1></body></html>"

    sender = {"name": "Petersburg Explorer", "email": "petersburg-explorer-game@yandex.ru"}
    to = [{"email": email}]
    reply_to = {"email": "petersburg-explorer-game@yandex.ru", "name": "Petersburg Explorer"}
    headers = {"Some-Custom-Name": "unique-id-1234"}

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, headers=headers,
                                                   html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
        return True
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return False