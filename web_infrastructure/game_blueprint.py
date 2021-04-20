from flask import Blueprint, render_template, redirect, session, request

from score_scripts.get_panoramas_data import get_panoramas_data
from score_scripts.parsers import parse_coordinates
from score_scripts.parsers import parse_destination_coordinates
from score_scripts.score_count import count_score

blueprint = Blueprint(__name__, 'game_blueprint', template_folder='templates')

ROUND = 1


@blueprint.route("/")
def index():
    session['Round'] = 1
    session['Score'] = 0
    session['Current Destination Coordinates'] = -1
    session['Current Coordinates'] = -1

    return render_template('start.html')


@blueprint.route("/game/", methods=['POST', 'GET'])
def game_screen():
    global ROUND
    if request.method == 'GET':
        panoramas_dict, ind1, ind2 = get_panoramas_data(ROUND)

        current_start_coords = (panoramas_dict[list(panoramas_dict.keys())[ind1]][0],
                                panoramas_dict[list(panoramas_dict.keys())[ind1]][1])

        session['Current Destination Coordinates'] = [panoramas_dict[list(panoramas_dict.keys())[ind2]][0],
                                                      panoramas_dict[list(panoramas_dict.keys())[ind2]][1]]

        session.modified = True
        return render_template('panorama.html',
                               destination=list(panoramas_dict.keys())[ind2],
                               x=current_start_coords[0],
                               y=current_start_coords[1],
                               round=ROUND, score=session['Score'])

    elif request.method == 'POST':
        response = request.get_data().decode()[1:-1].replace('"x":', ""). \
            replace(',"y"', '').replace(".", "").split(":")

        ROUND += 1

        session['Score'] += count_score(parse_coordinates(response),
                                        parse_coordinates(parse_destination_coordinates(
                                            session['Current Destination Coordinates'])))

        if ROUND == 5:
            return render_template('endgame.html', score=session['Score'])

        return redirect('/game/')
