import sqlite3
from sqlite3 import Error

def create_table_with_cols(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS comflightplan (
                    ID integer PRIMARY KEY,
                    DATE datetime,
                    SECTOR text,
                    AC text,
                    ACTYPE text,
                    BASE_IN text,
                    BASE_OUT text,
                    DEP text,
                    ARR text,
                    ROUTE text,
                    FLT_NO text,
                    STD integer,
                    STA integer,
                    BLOCK integer,
                    FREQ text,
                    "FROM" integer,
                    "TO" integer
                );'''
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def create_connection_com_fpl():
    conn = None;
    try:
        conn = sqlite3.connect('comflightplan.db') # creates a SQLite database named 'comflightplan.db'
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def main():
    # create a database connection
    conn = create_connection_com_fpl()

    # create tables
    if conn is not None:
        create_table_with_cols(conn)  # Corrected function name
    else:
        print("Error! cannot create the database connection.")

    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()