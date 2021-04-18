import random

from flask import Flask, render_template, redirect, request, session
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.cluster import Cluster
from data.panorama import Panorama
from data.user import User

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.email_verification import EmailVerificationForm

from score_scripts.parsers import parse_coordinates
from score_scripts.parsers import parse_destination_coordinates
from score_scripts.score_count import count_score

from dotenv import load_dotenv

from email_scripts.mail_sender import send_email
from email_scripts.code_generator import generate_code

load_dotenv(dotenv_path='email_scripts/.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'petersburg_explorer_secret_key'


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

    return panoramas_dict, i1, i2


@app.route("/catch_coordinates", methods=['PUT'])
def catch_coordinates():
    if request.method == 'PUT':
        response = request.get_data().decode()[1:-1].replace('"x":', "").\
            replace(',"y"', '').replace(".", "").split(":")
        session['Current Coordinates'] = response
        return "caught coordinates"


@app.route("/game", methods=['POST', 'GET'])
def game_screen():
    if request.method == 'GET':
        panoramas_dict, ind1, ind2 = get_panoramas_data(session['Round'])

        current_start_coords = (panoramas_dict[list(panoramas_dict.keys())[ind1]][0],
                                panoramas_dict[list(panoramas_dict.keys())[ind1]][1])

        session['Current Destination Coordinates'] = [panoramas_dict[list(panoramas_dict.keys())[ind2]][0],
                                                      panoramas_dict[list(panoramas_dict.keys())[ind2]][1]]

        return render_template('panorama.html',
                               destination=list(panoramas_dict.keys())[ind2],
                               x=current_start_coords[0],
                               y=current_start_coords[1],
                               round=session['Round'], score=session['Score'])

    elif request.method == 'POST':
        session['Round'] += 1

        session['Score'] += count_score(parse_coordinates(session['Current Coordinates']),
                                        parse_coordinates(parse_destination_coordinates(
                                            session['Current Destination Coordinates'])))

        if session['Round'] == 5:
            return render_template('endgame.html', score=session['Score'])

        return redirect('/game')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    session['Round'] = 1
    session['Score'] = 0
    session['Current Destination Coordinates'] = 0
    session['Current Coordinates'] = 0

    return render_template('start.html')


def main():
    db_session.global_init('db/Petersburg.db')
    app.run(port=8000)


@app.route('/email_verification', methods=['GET', 'POST'])
def email_verification():
    form = EmailVerificationForm()
    if form.validate_on_submit():
        return redirect('/login')

    return render_template('email_verification.html', title='Подтверждение', form=form)


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
        verification_code = generate_code()

        email_text = "Кто-то пытается зарегистрироваться в игре Petersburg Explorer, исользуя данный email-адрес." \
                     "Если это вы, введите данный код в соответствующее поле: {}".format(verification_code)

        if send_email(form.email.data, 'Регистрация в Petersburg Explorer', email_text):
            return redirect('/email_verification')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

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
