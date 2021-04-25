from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup

TOKEN = "1601660987:AAH8--Glix9nt_3um_icg8mhR-epK6xe1yQ"

reply_keyboard = [['/infoⓘ', '/site🌐', '/help❔']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def help(update, context):
    update.message.reply_text(
        '''В этой статье приведены инструкции по устранению проблем с пользованием нашим сайтом.

🆘Здесь будет список основных проблем ии их решений.🆘
☰ ☰ ☰ ☰ ☰ ☰ 
☰ ☰ ☰ ☰ ☰ ☰ 
☰ ☰ ☰ ☰ ☰ ☰ 
☰ ☰ ☰ ☰ ☰ ☰ 
☰ ☰ ☰ ☰ ☰ ☰ 
☰ ☰ ☰ ☰ ☰ ☰ 
☰ ☰ ☰ ☰ ☰ ☰ 

✅Лайфхак✅
Чтобы не было никаких вылетов или багов, просто не торопитесь🗿
Наши сервера могут не успеть за вами. Давайте панорамам полностью прогружаться🙏

Если же возникли вопросы, пишите на почту ✉''',
        reply_markup=markup)


def start(update, context):
    update.message.reply_text(
        """Привет👋!
Я - Explorer Bot🤖""",
        reply_markup=markup)


def site(update, context):
    update.message.reply_text(
        "Сайт: https://188.68.221.19",
        reply_markup=markup)


def info(update, context):
    update.message.reply_text(
        '''Petersburg Explorer - это новая игра о Санкт-Петербурге.
Вы погружаетесь в северную столицу России благодаря
панорам Яндекс карт.
                
В процессе игры вы будете гулять по городу. Вам нужно 
будет дойти до определённого места. Чем ближе вы придёте
к месту назначения, тем больше очков вы получите! Так что 
вперёд гулять по нашему любимому городу! 😉 
''',
        reply_markup=markup)


def start_tgbot():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    start_tgbot()
