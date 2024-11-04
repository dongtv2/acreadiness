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

# Function to fetch all records from ac_status
def fetch_ac_status(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT ac_statusno_i, acreg, status, station, remark FROM ac_status")
        rows = c.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to fetch all records from ac_list
def fetch_ac_list(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT acreg FROM ac_list")
        rows = c.fetchall()
        return [row[0] for row in rows]
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to fetch all records from station
def fetch_station_list(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT station FROM station")
        rows = c.fetchall()
        return [row[0] for row in rows]
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to insert a new record into ac_status
def insert_ac_status(conn, acreg, status, station, remark):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO ac_status (acreg, status, station, remark) VALUES (?, ?, ?, ?)", (acreg, status, station, remark))
        conn.commit()
        st.info(f"Inserted new record: {acreg}, {status}, {station}, {remark}")
    except Error as e:
        st.error(f"Error: {e}")

# Function to update a record in ac_status
def update_ac_status(conn, ac_statusno_i, acreg, status, station, remark):
    try:
        c = conn.cursor()
        c.execute("UPDATE ac_status SET acreg = ?, status = ?, station = ?, remark = ? WHERE ac_statusno_i = ?", (acreg, status, station, remark, ac_statusno_i))
        conn.commit()
        st.info(f"Updated record {ac_statusno_i}: {acreg}, {status}, {station}, {remark}")
    except Error as e:
        st.error(f"Error: {e}")

# Function to delete a record from ac_status
def delete_ac_status(conn, ac_statusno_i):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM ac_status WHERE ac_statusno_i = ?", (ac_statusno_i,))
        conn.commit()
        st.info(f"Deleted record {ac_statusno_i}")
    except Error as e:
        st.error(f"Error: {e}")

def app():
    st.title('AC STATUS LIST')

    conn = create_connection()
    if conn is not None:
        ac_list = fetch_ac_list(conn)
        station_list = fetch_station_list(conn)
        rows = fetch_ac_status(conn)
        df = pd.DataFrame(rows, columns=["ac_statusno_i", "acreg", "status", "station", "remark"])

        edited_df = st.data_editor(df, 
                                   column_config={
                                       "acreg": st.column_config.SelectboxColumn(
                                           "AC Reg",
                                           options=ac_list,
                                           help="Select the aircraft registration"
                                       ),
                                       "station": st.column_config.SelectboxColumn(
                                           "Station",
                                           options=station_list,
                                           help="Select the station"
                                       )
                                   },
                                   num_rows="dynamic")

        if st.button("Save Changes"):
            for index, row in edited_df.iterrows():
                if pd.isna(row["ac_statusno_i"]):  # New record
                    insert_ac_status(conn, row["acreg"], row["status"], row["station"], row["remark"])
                else:  # Existing record
                    update_ac_status(conn, row["ac_statusno_i"], row["acreg"], row["status"], row["station"], row["remark"])

            st.success("Changes saved successfully!")

        if st.button("Delete Selected"):
            selected_rows = edited_df[edited_df["selected"] == True]
            for index, row in selected_rows.iterrows():
                delete_ac_status(conn, row["ac_statusno_i"])

            st.success("Selected records deleted successfully!")

        conn.close()

if __name__ == "__main__":
    app()