import sqlalchemy

from data.db_session import SqlAlchemyBase


class Panorama(SqlAlchemyBase):
    __tablename__ = 'panoramas'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    x = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    y = sqlalchemy.Column(sqlalchemy.Float, nullable=True)