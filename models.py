from utils import get_connection, hash_password


def get_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT PASSWORD_HASH FROM USERS WHERE USERNAME = %s", (username,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result and result[0] == hash_password(password):
            return True
    except Exception as e:
        print("Virhe käyttäjän tarkistuksessa:", e)
    return False
