import random
from data import db_session
from data.cluster import Cluster
from data.panorama import Panorama


def get_panoramas_data(cluster_id):
    db_sess = db_session.create_session()
    cluster = db_sess.query(Cluster).filter(Cluster.id == cluster_id).first()

    panoramas = [int(elem) for elem in cluster.panoramas.split()]

    panoramas_dict = {}

    for panorama_id in panoramas:
        for panorama_from_db in db_sess.query(Panorama).filter(Panorama.id == panorama_id):
            panoramas_dict[panorama_from_db.name] = [panorama_from_db.x, panorama_from_db.y]

    i1, i2 = random.sample(range(len(panoramas_dict.keys())), 2)

    return panoramas_dict, i1, i2
