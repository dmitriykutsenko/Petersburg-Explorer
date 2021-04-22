from flask import Blueprint, render_template, redirect, request

from data import db_session
from data.game_session import GameSession
from score_scripts.get_panoramas_data import get_panoramas_data
from score_scripts.parsers import parse_coordinates

blueprint = Blueprint(__name__, 'game_blueprint', template_folder='templates')


@blueprint.route("/")
def index():
    db_sess = db_session.create_session()

    gameSession = GameSession()
    gameSession.setRound(1)
    gameSession.setScore(0)

    db_sess.add(gameSession)
    db_sess.commit()

    return render_template('start.html')


@blueprint.route("/game/", methods=['POST', 'GET', 'PUT'])
def game_screen():
    if request.method == 'GET':
        db_sess = db_session.create_session()
        gameSession = db_sess.query(GameSession).all()[-1]

        currentRound = gameSession.round

        panoramas_dict, ind1, ind2 = get_panoramas_data(currentRound)

        current_start_coords = (panoramas_dict[list(panoramas_dict.keys())[ind1]][0],
                                panoramas_dict[list(panoramas_dict.keys())[ind1]][1])

        dest_coordinates = parse_coordinates([str(panoramas_dict[list(panoramas_dict.keys())[ind2]][0]).replace(".", ""),
                            str(panoramas_dict[list(panoramas_dict.keys())[ind2]][1]).replace(".", "")])

        score = gameSession.totalScore

        db_sess.commit()

        print(dest_coordinates)

        return render_template('panorama.html',
                               destination=list(panoramas_dict.keys())[ind2],
                               x=current_start_coords[0],
                               y=current_start_coords[1],
                               round=currentRound,
                               xCount=dest_coordinates[0],
                               yCount=dest_coordinates[1])

    elif request.method == "POST":
        db_sess = db_session.create_session()
        gameSession = db_sess.query(GameSession).all()[-1]

        currentRound = gameSession.round
        currentRound += 1
        gameSession.setRound(currentRound)

        print("ROUND UPDATED:", currentRound)

        db_sess.commit()

        if str(currentRound) == "5":
            print("GAME FINISHED")
            return redirect('/finish_game/')
        else:
            return redirect('/game/')


@blueprint.route('/finish_game/')
def finish():
    db_sess = db_session.create_session()
    gameSession = db_sess.query(GameSession).all()[-1]

    return render_template('endgame.html', score=gameSession.totalScore)
