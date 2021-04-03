from flask import Flask, render_template, redirect, make_response, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from werkzeug.exceptions import abort
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def panorama():
    return render_template('panorama.html')


if __name__ == '__main__':
    app.run()