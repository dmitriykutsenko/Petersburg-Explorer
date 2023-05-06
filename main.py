from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from waitress import serve

import os
from data import db_session
from data.user import User
from forms.search import SearchForm
from web_infrastructure import users_blueprint, game_blueprint


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'petersburg_explorer_secret_key'
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    @app.context_processor
    def base():
        form = SearchForm()
        return dict(form=form)

    app.register_blueprint(users_blueprint.blueprint)
    app.register_blueprint(game_blueprint.blueprint)

    load_dotenv(dotenv_path='data/.env')
    db_session.global_init('db/Petersburg.db')

    return app


if __name__ == '__main__':
    app = create_app()
    serve(app, host='0.0.0.0', port=5000)
