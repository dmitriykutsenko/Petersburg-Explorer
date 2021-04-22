import sqlalchemy

from data.db_session import SqlAlchemyBase


class GameSession(SqlAlchemyBase):
    __tablename__ = 'game_sessions'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    round = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    completed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    destination_coordinates = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)

    totalScore = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    firstRound = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    secondRound = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    thirdRound = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    fourthRound = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def setFirstRoundScore(self, score):
        self.firstRound = score

    def setSecondRoundScore(self, score):
        self.secondRound = score

    def setThirdRoundScore(self, score):
        self.thirdRound = score

    def setFourthRoundScore(self, score):
        self.fourthRound = score

    def setRound(self, round):
        self.round = round

    def setScore(self, score):
        self.totalScore = score

    def setDestinationCoordinates(self, coordinates):
        self.destination_coordinates = coordinates
