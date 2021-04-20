import os

from flask import Flask
from flask_login import LoginManager
from data import db_session
from data.user import User
from dotenv import load_dotenv
from web_infrastructure import users_blueprint, game_blueprint

load_dotenv(dotenv_path='email_scripts/.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'petersburg_explorer_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


app.register_blueprint(users_blueprint.blueprint)
app.register_blueprint(game_blueprint.blueprint)


def main():
    db_session.global_init('db/Petersburg.db')
    app.run('127.0.0.1', port=8080)



if __name__ == '__main__':
    main()
