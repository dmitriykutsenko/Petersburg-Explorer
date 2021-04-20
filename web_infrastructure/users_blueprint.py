from flask import Blueprint, render_template, redirect, session
from flask_login import login_user, logout_user, login_required


from data import db_session

from data.user import User

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.email_verification import EmailVerificationForm

from email_scripts.code_generator import generate_code
from email_scripts.mail_sender import send_email

blueprint = Blueprint(__name__, 'users_blueprint', template_folder='templates')


@blueprint.route("/signup", methods=['GET', 'POST'])
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
            session['Verification Code'] = verification_code
            session['User Email'] = form.email.data
            session['User Nickname'] = form.name.data
            session['User Password'] = form.password.data

            return redirect('/email_verification')

    return render_template('register.html', title='Регистрация', form=form)


@blueprint.route('/email_verification', methods=['GET', 'POST'])
def email_verification():
    form = EmailVerificationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if session['Verification Code'] == form.code.data:
            user = User(
                name=session['User Nickname'],
                email=session['User Email'],
            )
            user.set_password(session['User Password'])
            db_sess.add(user)
            db_sess.commit()

            return redirect('/login')

        else:
            return render_template('email_verification.html', title='Подтверждение', form=form,
                                   message='Неверный код подтверждения')

    return render_template('email_verification.html', title='Подтверждение', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
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


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
