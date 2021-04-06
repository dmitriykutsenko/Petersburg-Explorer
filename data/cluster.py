import sqlalchemy

from data.db_session import SqlAlchemyBase


class Cluster(SqlAlchemyBase):
    __tablename__ = 'clusters'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    panoramas = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def addPanorama(self, id):
        panoramas_list = self.panoramas.split()
        panoramas_list.append(id)
        self.panoramas = " ".join(panoramas_list)
