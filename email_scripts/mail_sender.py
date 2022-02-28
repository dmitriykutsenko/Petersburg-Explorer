from __future__ import print_function
import os
from pprint import pprint

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def send_email(email, verification_code):
    api_key = os.getenv("SEND_IN_BLUE_KEY")
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))
    subject = "Регистрация в Petersburg Explorer"

    html_content = f'''<!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Document</title>
        </head>

        <body
            style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;background-color: #d8dada;font-size: 19px;max-width: 800px;margin: 0 auto;padding: 3%;">
            <div id="wrapper" style="background-color: #fff;padding: 0 20px;">
                <header style="width: 98%;">
                    <div id="logo" style="text-align: center;">
                        <img src="https://raw.githubusercontent.com/dmtrkv/Petersburg-Explorer/b7f6a90a2bf55dfca60c5fb15358474219042329/static/img/logo.png"
                            alt="Petersburg-Explorer" width="80px" height="80px">
                    </div>
                </header>
                <div id="code-label" style="margin: 3%;text-align: center;font-size: 1.5rem;color: #333;">
                    Ваш код подтверждения регистрации аккаунта <br />
                </div>
                <div class="one-col"
                    style="border: 1px solid rgba(0, 0, 0, 0.158);border-radius: 5px;text-align: center;color: #333;padding: 3%;">
                    Продолжите регистрацию, введя код подтверждения снизу: <br />
                    <div id="code"
                        style="background-color: #d6ebff;display: inline-block;font-size: 1.6rem;font-weight: 700; margin: 2%;">
                        {verification_code}
                    </div>
                </div>
                <br />
                <div id="notes" style="color: #333;font-size: 1rem;">
                    <b>Примечание:</b> Это приглашение предназначено для {email}. Если вы не ожидали этого
                    приглашения, вы можете проигнорировать это письмо.
                </div>
            </div>
        </body>

        </html>'''

    sender = {"name": "Petersburg Explorer",
              "email": "petersburg-explorer-game@yandex.ru"}
    to = [{"email": email}]
    reply_to = {"email": "petersburg-explorer-game@yandex.ru",
                "name": "Petersburg Explorer"}
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
