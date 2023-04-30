import datetime

import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class GameSession(SqlAlchemyBase):
    __tablename__ = 'game_sessions'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    destination_coordinates_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    finish_coordinates_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date = sqlalchemy.Column(sqlalchemy.Date, nullable=True, default=datetime.datetime.now)
    total_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    round = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    first_round_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    second_round_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    third_round_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    fourth_round_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __init__(self):
        self.round = 1
        self.total_score = 0
        self.finish_coordinates_list = ""
        self.destination_coordinates_list = ""

    def set_round_score(self, round_number, score):
        if round_number == 1:
            self.first_round_score = score
        if round_number == 2:
            self.second_round_score = score
        if round_number == 3:
            self.third_round_score = score
        if round_number == 4:
            self.fourth_round_score = score

    def set_round(self, round):
        self.round = round

    def set_score(self, score):
        self.total_score = score

    def set_destination_coordinates(self, coordinates):
        self.destination_coordinates_list = coordinates

    def set_finish_coordinates(self, coordinates):
        self.finish_coordinates_list = coordinates

    def set_user_id(self, id):
        self.user_id = id
