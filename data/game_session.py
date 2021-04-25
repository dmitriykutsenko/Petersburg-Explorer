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

    completed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    destinationCoordinatesList = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    finishCoordinatesList = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date = sqlalchemy.Column(sqlalchemy.Date, nullable=True, default=datetime.datetime.now)
    totalScore = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    round = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    firstRoundScore = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    secondRoundScore = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    thirdRoundScore = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    fourthRoundScore = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    user = orm.relation('User')

    def __init__(self):
        self.round = 1
        self.totalScore = 0
        self.finishCoordinatesList = ""
        self.destinationCoordinatesList = ""

    def setRoundScore(self, roundNumber, score):
        if roundNumber == 1:
            self.firstRoundScore = score
        if roundNumber == 2:
            self.secondRoundScore = score
        if roundNumber == 3:
            self.thirdRoundScore = score
        if roundNumber == 4:
            self.fourthRoundScore = score

    def setRound(self, round):
        self.round = round

    def setScore(self, score):
        self.totalScore = score

    def setDestinationCoordinates(self, coordinates):
        self.destinationCoordinatesList = coordinates

    def setFinishCoordinates(self, coordinates):
        self.finishCoordinatesList = coordinates
