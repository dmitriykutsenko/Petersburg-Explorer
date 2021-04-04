from flask import Flask, render_template, redirect, make_response, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from werkzeug.exceptions import abort
from data.cluster import Cluster
from data.panorama import Panorama
from data.user import User
import random

from data import db_session

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


def main():
    db_session.global_init('db/Petersburg.db')
    app.run(port=8000)


if __name__ == '__main__':
    main()
