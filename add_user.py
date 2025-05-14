from utils import hash_password, get_connection


def add_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        sql = "INSERT INTO USERS (USERNAME, PASSWORD) VALUES (%s, %s)"
        cursor.execute(sql, (username, hashed))
        conn.commit()
        print(f"Käyttäjä '{username}' lisätty onnistuneesti.")
    except Exception as e:
        print("Virhe lisättäessä käyttäjää:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Esimerkkikäyttö
    username = input("Anna käyttäjätunnus: ")
    password = input("Anna salasana: ")
    add_user(username, password)
