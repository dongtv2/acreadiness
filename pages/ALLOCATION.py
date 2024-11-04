import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error

# Function to create a connection to the database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('moc.db')
    except Error as e:
        st.error(f"Error: {e}")
    return conn

# Function to create tables if they don't exist
def create_tables(conn):
    try:
        c = conn.cursor()
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
        c.execute(sql_allocation)
        conn.commit()
    except Error as e:
        st.error(f"Error: {e}")

# Function to insert a new allocation
def insert_allocation(conn, date, rev):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO allocation (date, rev) VALUES (?, ?)", (date, rev))
        conn.commit()
        return c.lastrowid
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to fetch joined data from ac_list and ac_status
def fetch_joined_data(conn):
    try:
        c = conn.cursor()
        query = '''
        SELECT ac_list.acreg, COALESCE(ac_status.station, 'Unknown') AS station, COALESCE(ac_status.status, 'OPS') AS status
        FROM ac_list
        LEFT JOIN ac_status ON ac_list.acreg = ac_status.acreg
        '''
        c.execute(query)
        rows = c.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to fetch distinct allocations
def fetch_allocations(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT DISTINCT date, rev FROM allocation")
        rows = c.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to insert data into allocation table
def insert_allocation_data(conn, date, rev, acreg, status, station):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO allocation (date, rev, acreg, status, station) VALUES (?, ?, ?, ?, ?)", (date, rev, acreg, status, station))
        conn.commit()
    except Error as e:
        st.error(f"Error: {e}")

def app():
    st.title('Allocation Management')

    conn = create_connection()
    if conn is not None:
        create_tables(conn)

        tab1, tab2 = st.tabs(["Create Allocation", "Copy Data"])

        with tab1:
            st.header("Create Allocation")
            date = st.date_input("Date")
            rev = st.text_input("Rev")
            if st.button("Create Allocation"):
                allocateno_i = insert_allocation(conn, date, rev)
                if allocateno_i:
                    st.success(f"Allocation created with Date: {date} and Rev: {rev}")
            st.table(fetch_allocations(conn))

        with tab2:
            st.header("Copy Data to Allocation")
            allocations = fetch_allocations(conn)
            if allocations:
                allocation_options = [f"{date} - {rev}" for date, rev in allocations]
                selected_allocation = st.selectbox("Select Allocation", allocation_options)
                if selected_allocation:
                    date, rev = selected_allocation.split(" - ")
                    joined_data = fetch_joined_data(conn)
                    if joined_data:
                        df = pd.DataFrame(joined_data, columns=["acreg", "station", "status"])
                        st.dataframe(df)
                        if st.button("Copy All Data"):
                            for index, row in df.iterrows():
                                insert_allocation_data(conn, date, rev, row["acreg"], row["status"], row["station"])
                            st.success(f"All data copied to allocation with Date: {date} and Rev: {rev}")

        conn.close()

if __name__ == "__main__":
    app()