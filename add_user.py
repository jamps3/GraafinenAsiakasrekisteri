import pymysql
import bcrypt

user = "admin"
password = "salasana123"
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

connection = pymysql.connect(
    host="your-db-hostname",
    user="your-db-user",
    password="your-db-password",
    database="Asiakastilaus",
)
cursor = connection.cursor()
cursor.execute(
    "INSERT INTO KAYTTAJA (TUNNUS, SALASANA_HASH) VALUES (%s, %s)",
    (user, password_hash),
)
connection.commit()
cursor.close()
connection.close()
print("Käyttäjä lisätty.")
