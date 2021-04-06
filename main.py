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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'petersburg_explorer_secret_key'

def get_panoramas_data():
    db_sess = db_session.create_session()
    clusters = db_sess.query(Cluster)

    for cluster in clusters:
        panoramas = cluster.panoramas.split()

    panoramas = [int(elem) for elem in panoramas]

    panoramas_dict = {}

    for panorama_from_db in db_sess.query(Panorama):
        panoramas_dict[panorama_from_db.name] = [panorama_from_db.x, panorama_from_db.y]

    print(panoramas_dict)

    i1, i2 = random.sample(range(len(panoramas_dict.keys())), 2)
    print(i1, i2)
    return panoramas_dict, i1, i2

@app.route("/", methods=['POST', 'GET'])
def game_screen():
    if request.method == 'GET':
        panoramas_dict, ind1, ind2 = get_panoramas_data()

        print(list(panoramas_dict.keys()))

        return render_template('panorama.html', destination=list(panoramas_dict.keys())[ind2],
                               x=panoramas_dict[list(panoramas_dict.keys())[ind1]][0],
                               y=panoramas_dict[list(panoramas_dict.keys())[ind1]][1])

    elif request.method == 'POST':
        # вызов js функции получения координат
        # переключение на следющую панораму при помощи js функции
        panoramas_dict, ind1, ind2 = get_panoramas_data()
        return render_template('panorama.html', destination=list(panoramas_dict.keys())[ind2],
                               x=panoramas_dict[list(panoramas_dict.keys())[ind1]][0],
                               y=panoramas_dict[list(panoramas_dict.keys())[ind1]][1])

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)



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
            return redirect("/panorama")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
