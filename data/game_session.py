import sqlalchemy

from data.db_session import SqlAlchemyBase


class GameSession(SqlAlchemyBase):
    __tablename__ = 'game_sessions'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
