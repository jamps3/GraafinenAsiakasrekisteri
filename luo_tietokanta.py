from utils import get_connection

# Alustetaan yhteys ilman tietokantaa, koska tietokantaa ei ehkä vielä ole olemassa
conn = get_connection()
with conn.cursor() as cursor:
    cursor.execute("DROP DATABASE IF EXISTS Asiakastilaus;")
    cursor.execute(
        "CREATE DATABASE Asiakastilaus CHARACTER SET utf8mb4 COLLATE utf8mb4_swedish_ci;"
    )
conn.close()

# Yhdistetään uudelleen, nyt uuteen tietokantaan
conn = get_connection(database="Asiakastilaus")
with conn.cursor() as cursor:
    # USERS-taulu ja admin-käyttäjä salasanalla admin
    cursor.execute(
        """
        CREATE TABLE USERS (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            USERNAME VARCHAR(50) NOT NULL UNIQUE,
            PASSWORD_HASH CHAR(64) NOT NULL
        );
    """
    )
    cursor.execute(
        """
        INSERT INTO USERS (USERNAME, PASSWORD_HASH)
        VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');
    """
    )

    # ASIAKAS-taulu
    cursor.execute(
        """
        CREATE TABLE ASIAKAS (
            ASIAKASNUMERO INT AUTO_INCREMENT PRIMARY KEY,
            ETUNIMI VARCHAR(50) NOT NULL,
            SUKUNIMI VARCHAR(50) NOT NULL,
            YRITYS VARCHAR(100)
        );
    """
    )

    # Esimerkkiasiakkaat
    customers = [
        ("Matti", "Meikäläinen", "Esimerkki Oy"),
        ("Maija", "Mallikas", "Malliyritys Oy"),
        ("Kalle", "Kustaa", "Kustaa Ky"),
        ("Liisa", "Lempiäinen", "Liisan Leipä"),
        ("Pekka", "Pouta", "Sääpalvelu Oy"),
        ("Sari", "Sateenkaari", "Luontopalvelut Oy"),
        ("Ville", "Vainio", "Vainion Vihannes"),
        ("Anna", "Aurinkoinen", "Aurinko Energia Oy"),
        ("Jari", "Jokinen", "Jokinen & Co"),
        ("Elina", "Ekström", "Ekström Solutions"),
    ]

    cursor.executemany(
        "INSERT INTO ASIAKAS (ETUNIMI, SUKUNIMI, YRITYS) VALUES (%s, %s, %s);",
        customers,
    )

conn.commit()
conn.close()

print("Tietokanta 'Asiakastilaus' ja taulut luotu onnistuneesti.")
