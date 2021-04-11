import vk
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

TOKEN = '9a91352c9040eb78f534e8b0d69cb6c3409aabc434dce6e3fe4283c8f5ff08b7c364c766e22fc0fd157b8'

def send_messages(chat_id, text):
    random_id = random.randint(0, 1000000)
    vk.method('messages.send', {'chat_id': chat_id, 'message': text, 'random_id': random_id})


def bot():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, 203903199)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.type.to_me:
                msg = event.text
                bad_words = ['говно', 'какашка', 'пока']
                chat_id = event.chat_id
                send_messages(chat_id, "Спасибо, что написали нам. Мы обязательно ответим")
                if msg in bad_words:
                    send_messages(chat_id, 'Говорите добрые слова!')
                else:
                    send_messages(chat_id, msg)


if __name__ == '__main__':
    bot()