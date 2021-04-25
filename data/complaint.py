import sqlalchemy

from data.db_session import SqlAlchemyBase


class Complaint(SqlAlchemyBase):
    __tablename__ = 'complaints'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f"Панорама {self.name}: {self.x}, {self.y}"