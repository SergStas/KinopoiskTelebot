import sqlite3 as sq
from sqlite3 import Error

from models.dataclasses.Person import Person
from models.dataclasses.Relation import Relation
from models.dataclasses.User import User


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
        print(query)
    return cursor.fetchall()

def user_querry(query):
    connection.row_factory = lambda cursor, row: User(row[0], row[1], row[2], row[3], row[4])
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
    connection.row_factory = lambda cursor, row: row
    return cursor.fetchall()

def person_querry(query):
    connection.row_factory = lambda cursor, row: Person(row[0], row[1], row[2])
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
    connection.row_factory = lambda cursor, row: row
    return cursor.fetchall()

tables = ['genre', 'person', 'params', 'colleague', 'params_genre', 'user_type', 'user', 'req', 'fav']


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