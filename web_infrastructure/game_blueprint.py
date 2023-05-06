import logging
import random

from flask import Blueprint, render_template, redirect, request, session
from flask_login import login_required, current_user

from data import db_session
from data.game_session import GameSession
from score_scripts.get_panoramas_data import get_panoramas_data
from score_scripts.parsers import parse_coordinates
from score_scripts.parsers import parse_destination_coordinates
from score_scripts.parsers import to_int_parser
from score_scripts.score_count import count_score

blueprint = Blueprint('game_blueprint', __name__, template_folder='templates')


# logging.basicConfig(level=logging.INFO, filename='gamesession.log',
#                     format='%(asctime)s %(levelname)s %(name)s %(message)s')

@blueprint.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html'), 500


@blueprint.route("/")
def index():
    db_sess = db_session.create_session()

    game_session = GameSession()

    db_sess.add(game_session)
    db_sess.commit()

    db_sess = db_session.create_session()
    game_session = db_sess.query(GameSession).all()[-1]
    session['sessionId'] = game_session.id
    logging.info("STARTED A NEW GAMESESSION (id = {})".format(str(session['sessionId'])))

    return render_template('start.html')


@blueprint.route("/game/", methods=['POST', 'GET', 'PUT'])
@login_required
def game_screen():
    if request.method == 'GET':
        db_sess = db_session.create_session()
        game_session = db_sess.query(GameSession).filter(GameSession.id == session['sessionId']).first()

        current_round = game_session.round
        if str(current_round) == '5':
            logging.info("REDIRECTED GAMESESSION (id = {}) TO FINISH SCREEN".format(str(session['sessionId'])))
            return redirect('/finish_game/')

        if int(current_round) > 5:
            logging.fatal("GAMESESSION's ROUND NUMBER BECAME MORE THAN 5")
            return render_template('error.html')

        cluster_id = random.randint(1, 7)

        panoramas_dict, ind1, ind2 = get_panoramas_data(str(cluster_id))

        start_coordinates = (panoramas_dict[list(panoramas_dict.keys())[ind1]][0],
                             panoramas_dict[list(panoramas_dict.keys())[ind1]][1])

        db_dest_coordinates = game_session.destination_coordinates_list.split(";")

        dest_coordinates = " ".join(
            parse_coordinates(
                parse_destination_coordinates(
                    [str(panoramas_dict[list(panoramas_dict.keys())[ind2]][0]),

                     str(panoramas_dict[list(panoramas_dict.keys())[ind2]][1])]
                )
            )
        )

        db_dest_coordinates.append(dest_coordinates)

        game_session.set_destination_coordinates(";".join(db_dest_coordinates))

        db_sess.commit()

        logging.info("NEW DESTINATION COORDINATES WERE PUT CORRECTLY: {} {}".format(db_dest_coordinates[0],
                                                                                    db_dest_coordinates[1]))

        return render_template('panorama.html',
                               destination=list(panoramas_dict.keys())[ind2],
                               x=start_coordinates[0],
                               y=start_coordinates[1],
                               round=current_round)

    elif request.method == 'PUT':
        response = request.get_data().decode()[1:-1].replace('"x":', ""). \
            replace(',"y"', '').replace(".", "").split(":")
        db_sess = db_session.create_session()
        game_session = db_sess.query(GameSession).filter(GameSession.id == session['sessionId']).first()

        db_finish_coordinates = game_session.finish_coordinates_list.split(";")
        db_finish_coordinates.append(
            " ".join(
                parse_coordinates(response)
            )
        )

        game_session.set_finish_coordinates(";".join(db_finish_coordinates))
        db_sess.commit()
        logging.info("NEW DESTINATION COORDINATES WERE PUT CORRECTLY: {} {}".format(db_finish_coordinates[0],
                                                                                    db_finish_coordinates[1]))
        return 'caught coordinates'

    elif request.method == "POST":
        db_sess = db_session.create_session()
        game_session = db_sess.query(GameSession).filter(GameSession.id == session['sessionId']).first()

        current_round = game_session.round
        current_round += 1
        game_session.set_round(current_round)

        logging.info("GAMESESSIONS'S (id = {}) ROUND UPDATED TO {}".format(str(session['sessionId']),
                                                                           str(current_round)))

        db_sess.commit()

        return redirect('/game/')


@blueprint.route('/finish_game/')
@login_required
def finish():
    db_sess = db_session.create_session()
    db_sess.expire_on_commit = False
    game_session = db_sess.query(GameSession).filter(GameSession.id == session['sessionId']).first()

    total_score = 0

    finish_coordinates = game_session.finish_coordinates_list.split(";")
    destination_coordinates = game_session.destination_coordinates_list.split(";")

    for i in range(1, 5):
        this_finish_coordinates = finish_coordinates[i]
        this_destination_coordinates = destination_coordinates[i]

        plus_score = count_score(to_int_parser(this_finish_coordinates.split()),
                                 to_int_parser(this_destination_coordinates.split()))
        game_session.set_round_score(i, plus_score)
        total_score += plus_score

    game_session.set_user_id(current_user.id)
    game_session.set_score(total_score)

    db_sess.commit()

    logging.info("GAMESESSION (id = {}) FINISHED CORRECTLY".format(str(session['sessionId'])))

    return render_template('endgame.html', score=total_score)


@blueprint.route('/info/')
def info():
    return render_template('info.html')
