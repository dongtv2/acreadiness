import sqlite3
from sqlite3 import Error

def create_table_with_cols(conn):
    try:
        sql_ac_list = '''CREATE TABLE IF NOT EXISTS ac_list (
                    ac_regno_i integer PRIMARY KEY,
                    acreg text,
                    actype text
                );'''
        sql_ac_status = '''CREATE TABLE IF NOT EXISTS ac_status (
                    ac_statusno_i integer PRIMARY KEY,
                    acreg text,
                    status text,
                    station text,
                    remark text,
                    FOREIGN KEY (acreg) REFERENCES ac_list(acreg)
                );'''
        sql_allocation = '''CREATE TABLE IF NOT EXISTS allocation (
                    allocateno_i integer PRIMARY KEY,
                    date datetime,
                    rev text,
                    acreg text,
                    status text,
                    station text,
                    sta time,
                    std time,
                    grd_time time,
                    daily boolean,
                    FOREIGN KEY (station) REFERENCES station(station)
                );'''
        sql_station = '''CREATE TABLE IF NOT EXISTS station (
                    stationno_i integer PRIMARY KEY,
                    station text,
                    mainbase boolean,
                    remark text
                );'''

        c = conn.cursor()
        c.execute(sql_ac_list)
        c.execute(sql_ac_status)
        c.execute(sql_allocation)
        c.execute(sql_station)
    except Error as e:
        print(e)

def insert_ac_list(conn, aclist):
    try:
        sql_insert = '''INSERT INTO ac_list(acreg) VALUES(?)'''
        c = conn.cursor()
        c.executemany(sql_insert, [(ac,) for ac in aclist])
        conn.commit()
    except Error as e:
        print(e)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('moc.db') # creates a SQLite database named 'moc.db'
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def main():
    aclist = ['A521', 'A522', 'A523', 'A524', 'A525','A526', 'A527', 'A528', 'A529', 'A530', 'A531', 'A532', 'A533', 'A534', 'A535','A536','A538', 'A539', 'A540', 'A542', 'A544', 'A600', 'A607', 'A629', 'A630', 'A631', 'A632', 'A633', 'A634', 'A635', 'A636', 'A637', 'A639', 'A640', 'A641', 'A642', 'A643', 'A644', 'A645', 'A646', 'A647', 'A648', 'A649', 'A650', 'A651', 'A652', 'A653', 'A654', 'A655', 'A656', 'A657', 'A658', 'A661', 'A662', 'A663', 'A666', 'A667', 'A668', 'A669', 'A670', 'A671', 'A672', 'A673', 'A674', 'A675', 'A676', 'A677', 'A683', 'A684', 'A685', 'A687', 'A689', 'A690', 'A691', 'A693', 'A694', 'A697', 'A698', 'A699', 'A810', 'A811', 'A812', 'A814', 'A815', 'A816', 'A817']
    conn = create_connection()
    if conn is not None:
        create_table_with_cols(conn)
        insert_ac_list(conn, aclist)
        conn.close()

if __name__ == '__main__':
    main()