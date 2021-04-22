import sqlalchemy

from data.db_session import SqlAlchemyBase


class GameSession(SqlAlchemyBase):
    __tablename__ = 'game_sessions'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)

    finalScore = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

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
