from flask import Flask, render_template, redirect, make_response, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from werkzeug.exceptions import abort
from data.cluster import Cluster
from data.panorama import Panorama
from data.user import User

from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'petersburg_explorer_secret_key'


@app.route("/", methods=['POST', 'GET'])
def panorama():
    if request.method == 'GET':
        db_sess = db_session.create_session()
        clusters = db_sess.query(Cluster)

        for cluster in clusters:
            panoramas = cluster.panoramas.split()

        panoramas = [int(elem) for elem in panoramas]

        panoramas_dict = {}

        for panorama_from_db in db_sess.query(Panorama):
            panoramas_dict[panorama_from_db.name] = [panorama_from_db.x, panorama_from_db.y]

        print(panoramas_dict)
        print('here')

        # вызов js функции для перемещения панорамы в нужную точку
        return render_template('panorama.html')

    elif request.method == 'POST':
        # вызов js функции получения координат
        # переключение на следющую панораму при помощи js функции

        return render_template('panorama.html')


def main():
    db_session.global_init('db/explorer.db')
    app.run(port=8000)


if __name__ == '__main__':
    main()
