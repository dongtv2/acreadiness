#Create SQLITE for user input database including the following tables:
# DATE = datetime , A320, A321-CEO,A321-NEO, A321-ACT, A330 = int , REMARK = text

import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('ac_available.db') # creates a SQLite database named 'user_input.db'
        return conn
    except Error as e:
        print(e)

def create_table(conn):
    try:
        sql = '''CREATE TABLE ac_available (
                    DATE datetime,
                    A320 int,
                    A321_CEO int,
                    A321_NEO int,
                    A321_ACT int,
                    A330 int,
                    REMARK text
                );'''
        conn.execute(sql)
    except Error as e:
        print(e)

def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()