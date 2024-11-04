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

# Function to fetch all records from station
def fetch_station(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT stationno_i, station, mainbase, remark FROM station")
        rows = c.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to insert a new record into station
def insert_station(conn, station, mainbase, remark):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO station (station, mainbase, remark) VALUES (?, ?, ?)", (station, mainbase, remark))
        conn.commit()
    except Error as e:
        st.error(f"Error: {e}")

# Function to update a record in station
def update_station(conn, stationno_i, station, mainbase, remark):
    try:
        c = conn.cursor()
        c.execute("UPDATE station SET station = ?, mainbase = ?, remark = ? WHERE stationno_i = ?", (station, mainbase, remark, stationno_i))
        conn.commit()
    except Error as e:
        st.error(f"Error: {e}")

# Function to delete a record from station
def delete_station(conn, stationno_i):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM station WHERE stationno_i = ?", (stationno_i,))
        conn.commit()
    except Error as e:
        st.error(f"Error: {e}")

def app():
    st.title('STATION LIST')

    conn = create_connection()
    if conn is not None:
        rows = fetch_station(conn)
        df = pd.DataFrame(rows, columns=["stationno_i", "station", "mainbase", "remark"])
        df["mainbase"] = df["mainbase"].astype(bool)  # Ensure mainbase is boolean
    
        edited_df = st.data_editor(df, 
                                   column_config={
                                       "mainbase": st.column_config.CheckboxColumn(
                                           "Main Base",
                                           help="Select if this is a main base",
                                           default=False,
                                       )
                                   },
                                   num_rows="dynamic")

        if st.button("Save Changes"):
            for index, row in edited_df.iterrows():
                if pd.isna(row["stationno_i"]):  # New record
                    insert_station(conn, row["station"], row["mainbase"], row["remark"])
                else:  # Existing record
                    update_station(conn, row["stationno_i"], row["station"], row["mainbase"], row["remark"])

            st.success("Changes saved successfully!")

        if st.button("Delete Selected"):
            selected_rows = edited_df[edited_df["selected"] == True]
            for index, row in selected_rows.iterrows():
                delete_station(conn, row["stationno_i"])

            st.success("Selected records deleted successfully!")

        conn.close()

if __name__ == "__main__":
    app()