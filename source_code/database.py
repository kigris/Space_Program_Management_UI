import sqlite3
import os
from datetime import datetime

DATA_PATH = 'db/'
DB_FILENAME = 'spaceship_manager'


def check_database():
    # Se comprueba si existe el directorio, si no se crea
    os.makedirs(DATA_PATH, exist_ok=True)
    # Se comprueba si existe la base de datos, si no se crea
    con = sqlite3.connect(DATA_PATH + DB_FILENAME + '.db')
    cur = con.cursor()

    # Creación tabla Usuario
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
                user text NOT NULL, 
                password text NOT NULL
                )''')

    # Creación tabla cohetes
    cur.execute('''CREATE TABLE IF NOT EXISTS rockets
                (id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                name text NOT NULL, 
                maxWeight real NOT NULL
                )''')

    # Creación tabla estado
    cur.execute('''CREATE TABLE IF NOT EXISTS status (
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    description text NOT NULL
                )''')

    # Se insertan los diferentes estados
    cur.execute(
        "INSERT INTO status (description) VALUES ('CREATED'), ('IN TRANSIT'), ('DELIVERED'), ('FAILED'), ('ASSIGNED')")

    # Creación tabla lanzamientos
    cur.execute('''CREATE TABLE IF NOT EXISTS launches (
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    rocketId int NOT NULL,
                    desc_id text NOT NULL,
                    days int NOT NULL,
                    description text NOT NULL,
                    status int NOT NULL,
                    startDate text NOT NULL,
                    finalDate text,
                    FOREIGN KEY(rocketId) REFERENCES rockets(id)
                )''')

    # Creación tabla peticiones
    cur.execute('''CREATE TABLE IF NOT EXISTS petitions (
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,                    
                    desc_id text NOT NULL,
                    description text NOT NULL,
                    weight real NOT NULL,
                    days int NOT NULL, 
                    launchId int,
                    status int,
                    startDate text NOT NULL,
                    finalDate text,
                    FOREIGN KEY(launchId) REFERENCES launches(id)
                )''')

    # Creación tabla configuración
    cur.execute('''CREATE TABLE IF NOT EXISTS configuration(
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    description text NOT NULL,
                    value text NOT NULL
                    )''')

    # Se inserta el administrador
    cur.execute(
        "INSERT INTO users (user, password) VALUES  ('Admin','julian345')")
    # Se intenta obtener la fecha del sistema
    hasDate = cur.execute(
        "select value from configuration where description = 'systemDate'").fetchone()
    if not hasDate:  # si no existe
        # Se obtiene la fecha de hoy
        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            f"INSERT INTO configuration (value,description) VALUES (date('{today}'), 'systemDate')")

    con.commit()  # Se guardan todos los cambios
    con.close()  # Se cierra la conexión


def populate_db():
    con = sqlite3.connect(DATA_PATH + DB_FILENAME + '.db')
    cur = con.cursor()
    # Inserción cohetes
    cur.execute(
        "INSERT INTO rockets (name, maxWeight) VALUES ('Phoros','770'), ('Pastru','230')")
    # Se obtiene la fecha del sistema
    dateSystem = cur.execute(
        "select value from configuration where description = 'systemDate'").fetchone()[0]
    # Inserción peticiones
    cur.execute(
        f"INSERT INTO petitions (desc_id, description, weight, days, startDate) VALUES  ('P5PurAir', '5 purificadores de aire', 43, 14, date('{dateSystem}'))")
    cur.execute(
        f"INSERT INTO petitions (desc_id, description, weight, days, startDate) VALUES  ('P4O2', '4 tanques de oxígeno', 130.5, 32, date('{dateSystem}'))")
    cur.execute(
        f"INSERT INTO petitions (desc_id, description, weight, days, startDate) VALUES  ('P7A', '7 cajas de amoníaco', 45, 10, date('{dateSystem}'))")
    cur.execute(
        f"INSERT INTO petitions (desc_id, description, weight, days, startDate) VALUES  ('P2ExCO', '2 extractores de monóxido de carbono', 692.4, 40, date('{dateSystem}'))")

    # Inserción lanzamientos
    cur.execute(
        f"INSERT INTO launches (rocketId, desc_id, days, description, status, startDate) VALUES (1,'Apollo23', 35, 'Lanzamiento con escalera en ISS hacia la Luna', 1, date('{dateSystem}'))")
    cur.execute(
        f"INSERT INTO launches (rocketId, desc_id, days, description, status, startDate) VALUES (2,'Sartud2', 12, 'Viaje turístico hacia ISS', 1, date('{dateSystem}'))")

    # Se guardan cambios
    con.commit()
    con.close()
