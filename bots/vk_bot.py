import datetime
import os
import random
import string

import vk_api
from dotenv import load_dotenv
from pyowm import OWM
from pyowm.utils.config import get_default_config
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

load_dotenv(dotenv_path='data/.env')
TOKEN = os.getenv('VK_TOKEN')
API = os.getenv('VK_API')

bad_words = ['какашка', 'тупой', 'плохой', 'ужасный', 'нехороший', 'соси', 'салют', 'дибил']
hello_words = ['привет', 'хай', 'здарова']
bye_words = ['пока', 'до свидания']
yes_words = ['да', 'конечно', 'абсолютно', 'верно', 'точно']
no_words = ['нет']
how_are_u_words = ['как дела', 'как жизнь', 'все хорошо']

now = datetime.datetime.now()

def bot():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    group_id = int(os.getenv("VK_GROUP_ID"))
    longpoll = VkBotLongPoll(vk_session, group_id)

    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = vk.users.get(user_id=event.obj.message['from_id'], fields=["city"])
            first_name = response[0]["first_name"]
            if event.obj.message['text'].lower().rstrip(string.punctuation).strip() == 'начать':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Команды нашего бота: \n"
                                         f"1. !сайт \n"
                                         f"2. !гитхаб\n"
                                         f"3. !информация\n"
                                         f"4. !время \n"
                                         f"5. !дата \n"
                                         f"6. !погода\n"
                                         f"7. !жалоба"
                                         f"Также вы можете немного поговорить с ним, используя обычные фразы.",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() == '!сайт':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"petersburg-explorer.ru \n",
                                 random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Если ВКонтакте не открывает ссылку, то просто вставьте ее в браузер",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() == '!гитхаб':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"https://github.com/dmtrkv/Petersburg_Explorer",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() == '!информация':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Petersburg Explorer - это новая игра о Санкт-Петербурге. Вы погружаетесь в северную столицу России благодаря панорамам Яндекс карт. \n \n"
                                         "В процессе игры вы будете гулять по городу. Вам нужно будет дойти до определённого места. "
                                         "Чем ближе вы придёте к месту назначения, тем больше очков вы получите! Так что вперёд гулять по нашему любимому городу!",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() == '!дата':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=now.strftime("%d-%m-%Y"),
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation) == '!время':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=now.strftime("%H:%M:%S"),
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation) == '!погода':
                config_dict = get_default_config()
                config_dict['language'] = 'ru'
                owm = OWM(API, config_dict)
                manager = owm.weather_manager()
                observation = manager.weather_at_place('Санкт-Петербург')
                pogoda = observation.weather
                temperature = pogoda.temperature('celsius')['temp']
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Сейчас в городе Санкт-Петербурге " + str(int(temperature)) + " °С",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() == '!жалоба':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"По этой ссылке вы можете оставить жалобу: https://vk.com/topic-203903199_47565813",
                                 random_id=random.randint(0, 2 ** 64))


            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in hello_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {first_name}!",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in bad_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Соблюдайте нормы речевого этикета!",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in yes_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Хорошо",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in bye_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Удачи!",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation).strip() in how_are_u_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"У меня все хорошо!",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Я не понимаю вас."
                                         f" Команды нашего бота: \n"
                                         f"1. !сайт \n"
                                         f"2. !гитхаб\n"
                                         f"3. !информация\n"
                                         f"4. !время \n"
                                         f"5. !дата \n"
                                         f"6. !погода\n"
                                         f"7. !жалоба",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    bot()
