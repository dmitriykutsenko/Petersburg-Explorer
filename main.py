from flask import Flask, render_template, redirect, make_response, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from werkzeug.exceptions import abort

from data.cluster import Cluster
from data.panorama import Panorama
from data.user import User
import random
from forms.register import RegisterForm
from forms.login import LoginForm

from data import db_session
from data.user import User

import vk
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'petersburg_explorer_secret_key'

ROUND = 1


def get_panoramas_data(cluster_id):
    db_sess = db_session.create_session()
    cluster = db_sess.query(Cluster).filter(Cluster.id == cluster_id).first()

    panoramas = [int(elem) for elem in cluster.panoramas.split()]

    print(panoramas)

    panoramas_dict = {}

    for panorama_id in panoramas:
        for panorama_from_db in db_sess.query(Panorama).filter(Panorama.id == panorama_id):
            print(panorama_from_db)
            panoramas_dict[panorama_from_db.name] = [panorama_from_db.x, panorama_from_db.y]

    print(panoramas_dict)

    i1, i2 = random.sample(range(len(panoramas_dict.keys())), 2)

    print(i1, i2)

    return panoramas_dict, i1, i2


@app.route("/game", methods=['POST', 'GET'])
def game_screen():
    global ROUND
    if request.method == 'GET':
        panoramas_dict, ind1, ind2 = get_panoramas_data(ROUND)

        return render_template('panorama.html',
                               destination=list(panoramas_dict.keys())[ind2],
                               x=panoramas_dict[list(panoramas_dict.keys())[ind1]][0],
                               y=panoramas_dict[list(panoramas_dict.keys())[ind1]][1],
                               round=ROUND)

    elif request.method == 'POST':
        ROUND += 1

        return redirect('/game')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template('start.html')


def main():
    db_session.global_init('db/Petersburg.db')
    app.run(port=8000)

    
@app.route("/signup", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            return redirect("/game")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

def send_messages(chat_id, text):
    random_id = random.randint(0, 1000000)
    vk.method('messages.send', {'chat_id': chat_id, 'message': text, 'random_id': random_id})

def bot():
    vk_session = vk_api.VkApi(
        token='9a91352c9040eb78f534e8b0d69cb6c3409aabc434dce6e3fe4283c8f5ff08b7c364c766e22fc0fd157b8')

    longpoll = VkBotLongPoll(vk_session, 203903199)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Спасибо, что написали нам. Мы обязательно ответим",
                             random_id=random.randint(0, 2 ** 64))
            msg = event.text
            bad_words = ['говно', 'какашка', 'пока']
            chat_id = event.chat_id
            if msg in bad_words:
                send_messages(chat_id, 'Говорите добрые слова!')
            else:
                send_messages(chat_id, msg)


if __name__ == '__main__':
    main()
    bot()
