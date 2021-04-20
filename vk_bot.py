import string

import vk
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

TOKEN = '9a91352c9040eb78f534e8b0d69cb6c3409aabc434dce6e3fe4283c8f5ff08b7c364c766e22fc0fd157b8'

bad_words = ['какашка', 'тупой', 'плохой', 'ужасный', 'нехороший', 'соси', 'салют', 'дибил']
hello_words = ['привет', 'хай', 'здарова']
bye_words = ['пока', 'до свидания']
yes_words = ['да', 'конечно', 'абсолютно', 'верно', 'точно']
no_words = ['нет']


def bot():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 203903199)

    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = vk.users.get(user_id=event.obj.message['from_id'], fields=["city"])
            first_name = response[0]["first_name"]
            if event.obj.message['text'].lower().rstrip(string.punctuation) in hello_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {first_name}!",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation) in bad_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Соблюдайте нормы речевого этикета!",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation) in yes_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Хорошо",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation) in bye_words:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Удачи!",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'].lower().rstrip(string.punctuation) == 'хочу играть':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Вам будут предложены фотографии мест Санкт-Петербурга. Вы готовы?",
                                 random_id=random.randint(0, 2 ** 64))
                if event.obj.message['text'].lower().rstrip(string.punctuation):
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Нет)",
                                     random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{event.obj.message['text'].capitalize()}? Если вы хотите сыграть в игру, то напишите 'Хочу играть' ",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    bot()