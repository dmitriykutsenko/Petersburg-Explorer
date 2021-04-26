import logging
import random

from flask import Blueprint, render_template, redirect, request, session
from flask_login import login_required, current_user

from data import db_session
from data.game_session import GameSession
from score_scripts.get_panoramas_data import get_panoramas_data
from score_scripts.parsers import parse_coordinates
from score_scripts.parsers import parse_destination_coordinates
from score_scripts.parsers import toIntParser
from score_scripts.score_count import count_score

blueprint = Blueprint(__name__, 'game_blueprint', template_folder='templates')
logging.basicConfig(level=logging.INFO, filename='logs.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@blueprint.route("/")
def index():
    try:
        db_sess = db_session.create_session()

        gameSession = GameSession()

        db_sess.add(gameSession)
        db_sess.commit()

        db_sess = db_session.create_session()
        gameSession = db_sess.query(GameSession).all()[-1]
        session['sessionId'] = gameSession.id
        logging.info("Started a new gamesession (id = {})".format(str(session['sessionId'])))

        return render_template('start.html')

    except Exception:
        return render_template('error.html')


@blueprint.route("/game/", methods=['POST', 'GET', 'PUT'])
@login_required
def game_screen():
    if request.method == 'GET':
        try:
            db_sess = db_session.create_session()
            gameSession = db_sess.query(GameSession).filter(GameSession.id == session['sessionId']).first()

            currentRound = gameSession.round
            if str(currentRound) == '5':
                logging.info("Redicrected gamesession (id = {}) to finish screen".format(str(session['sessionId'])))
                return redirect('/finish_game/')

            if int(currentRound) > 5:
                logging.fatal("Gamesession's round number became more than 5")
                return render_template('error.html')

            cluster_id = random.randint(1, 7)

            panoramas_dict, ind1, ind2 = get_panoramas_data(str(cluster_id))

            start_coordinates = (panoramas_dict[list(panoramas_dict.keys())[ind1]][0],
                                 panoramas_dict[list(panoramas_dict.keys())[ind1]][1])

            db_dest_coordinates = gameSession.destinationCoordinatesList.split(";")

            dest_coordinates = " ".join(
                parse_coordinates(
                    parse_destination_coordinates(
                        [str(panoramas_dict[list(panoramas_dict.keys())[ind2]][0]),

                         str(panoramas_dict[list(panoramas_dict.keys())[ind2]][1])]
                    )
                )
            )

            db_dest_coordinates.append(dest_coordinates)

            gameSession.setDestinationCoordinates(";".join(db_dest_coordinates))

            db_sess.commit()

            logging.info("New destination coordinates were put correctly")

            return render_template('panorama.html',
                                   destination=list(panoramas_dict.keys())[ind2],
                                   x=start_coordinates[0],
                                   y=start_coordinates[1],
                                   round=currentRound)

        except Exception:
            logging.fatal('Error occured in GET handler')
            return render_template('error.html')

    elif request.method == 'PUT':
        try:
            response = request.get_data().decode()[1:-1].replace('"x":', ""). \
                replace(',"y"', '').replace(".", "").split(":")
            db_sess = db_session.create_session()
            gameSession = db_sess.query(GameSession).filter(GameSession.id == session['sessionId']).first()

            db_finish_coordinates = gameSession.finishCoordinatesList.split(";")
            db_finish_coordinates.append(
                " ".join(
                    parse_coordinates(response)
                )
            )

            gameSession.setFinishCoordinates(";".join(db_finish_coordinates))
            db_sess.commit()
            logging.info("New finish coordinates were put correctly")
            return 'caught coordinates'

        except Exception:
            logging.fatal('Error occured in PUT handler')
            return render_template('error.html')

    elif request.method == "POST":
        try:
            db_sess = db_session.create_session()
            gameSession = db_sess.query(GameSession).filter(GameSession.id == session['sessionId']).first()

            currentRound = gameSession.round
            currentRound += 1
            gameSession.setRound(currentRound)

            logging.info("Gamession's (id = {}) round updated to {}".format(str(session['sessionId']),
                                                                            str(currentRound)))

            db_sess.commit()

            return redirect('/game/')

        except Exception:
            logging.fatal('Error occured in POST handler')
            return render_template('error.html')


@blueprint.route('/finish_game/')
@login_required
def finish():
    try:
        db_sess = db_session.create_session()
        db_sess.expire_on_commit = False
        gameSession = db_sess.query(GameSession).filter(GameSession.id == session['sessionId']).first()

        totalScore = 0

        finishCoordinates = gameSession.finishCoordinatesList.split(";")
        destinationCoordinates = gameSession.destinationCoordinatesList.split(";")

        for i in range(1, 5):
            thisFinishCoordinates = finishCoordinates[i]
            thisDestinationCoordinates = destinationCoordinates[i]

            plusScore = count_score(toIntParser(thisFinishCoordinates.split()),
                                    toIntParser(thisDestinationCoordinates.split()))
            gameSession.setRoundScore(i, plusScore)
            totalScore += plusScore

        game_session = GameSession()

        game_session.totalScore = totalScore
        game_session.firstRoundScore = gameSession.firstRoundScore
        game_session.secondRoundScore = gameSession.secondRoundScore
        game_session.thirdRoundScore = gameSession.thirdRoundScore
        game_session.fourthRoundScore = gameSession.fourthRoundScore

        current_user.game_sessions.append(game_session)
        db_sess.merge(current_user)

        db_sess.commit()

        logging.info("Gamession (id = {}) finished correctly".format(str(session['sessionId'])))

        return render_template('endgame.html', score=totalScore)

    except Exception:
        logging.fatal('Error occured during counting total score in gamesession (id = {})'
                      .format(str(session['sessionId'])))
        return render_template('error.html')


@blueprint.route('/info/')
def info():
    return render_template('info.html')
