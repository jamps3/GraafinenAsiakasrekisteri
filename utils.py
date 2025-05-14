import hashlib
import pymysql


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection(database="Asiakastilaus"):
    return pymysql.connect(
        host="asiakastilaus.c1i6yq20uz0z.eu-north-1.rds.amazonaws.com",
        user="admin",
        password="0yongZ8zJabN3LyBxRpc",
        database=database,
    )
