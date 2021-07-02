import sqlite3 as sq
from sqlite3 import Error


def create_connection(pathDB):  # pathDB - text
    connection = None
    try:
        connection = sq.connect(pathDB)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection("kinopoiskDB.db")


def start_bd():
    with connection as conn:
        cur = conn.cursor()
        sql_code = open('db/sqlCode.sql', 'r').read()
        cur.executescript(sql_code)
        conn.commit()


def execute_query(query):
    #connection.row_factory = lambda cursor, row: row[0]
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
        print(query)

def execute_query_to_return(query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
    return cursor.fetchall()


tables = ['genre', 'position', 'person', 'film', 'genre_film', 'person_film', 'person_position_film', 'colleague']


def show_all_tables_values():
    cursor = connection.cursor()
    for table in tables:
        print(table)
        for row in cursor.execute('SELECT * FROM "{0}"'.format(table)):
            print(row)


def delete_all_tables_values():
    cursor = connection.cursor()
    for table in tables:
        for row in cursor.execute('DELETE FROM "{0}"'.format(table)):
            pass