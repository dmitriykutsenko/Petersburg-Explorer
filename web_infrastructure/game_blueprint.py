from flask import Blueprint, render_template, redirect, request
from flask_login import login_required

from data import db_session
from data.game_session import GameSession
from score_scripts.get_panoramas_data import get_panoramas_data
from score_scripts.parsers import parse_coordinates
from score_scripts.parsers import parse_destination_coordinates
from score_scripts.parsers import toIntParser
from score_scripts.score_count import count_score

blueprint = Blueprint(__name__, 'game_blueprint', template_folder='templates')


@blueprint.route("/")
def index():
    db_sess = db_session.create_session()

    gameSession = GameSession()
    gameSession.setRound(1)
    gameSession.setScore(0)
    gameSession.setDestinationCoordinates("")
    gameSession.setFinishCoordinates("")

    db_sess.add(gameSession)
    db_sess.commit()

    return render_template('start.html')


@blueprint.route("/game/", methods=['POST', 'GET', 'PUT'])
@login_required
def game_screen():
    if request.method == 'GET':
        db_sess = db_session.create_session()
        gameSession = db_sess.query(GameSession).all()[-1]

        currentRound = gameSession.round

        panoramas_dict, ind1, ind2 = get_panoramas_data(currentRound)

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

        return render_template('panorama.html',
                               destination=list(panoramas_dict.keys())[ind2],
                               x=start_coordinates[0],
                               y=start_coordinates[1],
                               round=currentRound)

    elif request.method == 'PUT':
        response = request.get_data().decode()[1:-1].replace('"x":', ""). \
            replace(',"y"', '').replace(".", "").split(":")
        db_sess = db_session.create_session()
        gameSession = db_sess.query(GameSession).all()[-1]

        db_finish_coordinates = gameSession.finishCoordinatesList.split(";")
        db_finish_coordinates.append(
            " ".join(
                parse_coordinates(response)
            )
        )

        gameSession.setFinishCoordinates(";".join(db_finish_coordinates))
        db_sess.commit()
        return 'caught coordinates'

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
@login_required
def finish():
    db_sess = db_session.create_session()
    gameSession = db_sess.query(GameSession).all()[-1]

    totalScore = 0

    finishCoordinates = gameSession.finishCoordinatesList.split(";")
    destinationCoordinates = gameSession.destinationCoordinatesList.split(";")

    for i in range(1, 5):
        thisFinishCoordinates = finishCoordinates[i]
        thisDestinationCoordinates = destinationCoordinates[i]

        print(thisFinishCoordinates, thisDestinationCoordinates)

        plusScore = count_score(toIntParser(thisFinishCoordinates.split()),
                                toIntParser(thisDestinationCoordinates.split()))
        gameSession.setRoundScore(i, plusScore)
        totalScore += plusScore

    db_sess.commit()

    return render_template('endgame.html', score=totalScore)
