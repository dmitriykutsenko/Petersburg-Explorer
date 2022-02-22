import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import Updater

reply_keyboard = [['/infoⓘ', '/site🌐'], ['/help❔', '/commands📖']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def help(update, context):
    update.message.reply_text(
        '''В этой статье приведены инструкции по устранению проблем с пользованием нашим сайтом.

✅Лайфхак✅
Чтобы не было никаких вылетов или багов, просто не торопитесь🗿
Наши сервера могут не успеть за вами. Давайте панорамам полностью прогружаться🙏

Если же возникли вопросы, пишите на почту ✉ или в нашу группу вконтакте''',
        reply_markup=markup)


def start(update, context):
    update.message.reply_text(
        """Привет👋!
Я - Explorer Bot🤖""",
        reply_markup=markup)


def site(update, context):
    update.message.reply_text(
        "Сайт: http://petersburg-explorer.ru",
        reply_markup=markup)


def info(update, context):
    update.message.reply_text(
        '''Petersburg Explorer - это новая игра о Санкт-Петербурге.
Вы погружаетесь в архитектуру и стиль северной столицы России благодаря
панорамам Яндекс.Карт.

В процессе игры вы будете гулять по городу. Вам нужно 
будет дойти до определённого места. Чем ближе вы придёте
к месту назначения, тем больше очков вы получите! Так что 
вперёд гулять по нашему любимому городу! 😉 
''',
        reply_markup=markup)


def vk(update, context):
    update.message.reply_text(
        "VK: https://vk.com/petersburgexplorer",
        reply_markup=markup)


def github(update, context):
    update.message.reply_text(
        "Github: https://github.com/dmtrkv/Petersburg_Explorer",
        reply_markup=markup)


def commands(update, context):
    update.message.reply_text(
        """📖Список команд:📖
/help - проблемы и их решения
/info - общая информация о проекте 
/vk - группа вк с ботом
/github - гитхаб проекта
/site - наш сайт""",
        reply_markup=markup)


def start_tgbot():
    load_dotenv(dotenv_path='data/.env')
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("vk", vk))
    dp.add_handler(CommandHandler("github", github))
    dp.add_handler(CommandHandler("commands", commands))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    start_tgbot()