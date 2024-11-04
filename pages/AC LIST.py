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

# Function to fetch all records from ac_list
def fetch_ac_list(conn):
    try:
        c = conn.cursor()
        c.execute("SELECT acreg, actype FROM ac_list")
        rows = c.fetchall()
        return rows
    except Error as e:
        st.error(f"Error: {e}")
        return []

# Function to insert a new record into ac_list
def insert_ac_list(conn, acreg, actype):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO ac_list (acreg, actype) VALUES (?, ?)", (acreg, actype))
        conn.commit()
    except Error as e:
        st.error(f"Error: {e}")

# Function to update a record in ac_list
def update_ac_list(conn, old_acreg, new_acreg, actype):
    try:
        c = conn.cursor()
        c.execute("UPDATE ac_list SET acreg = ?, actype = ? WHERE acreg = ?", (new_acreg, actype, old_acreg))
        conn.commit()
    except Error as e:
        st.error(f"Error: {e}")

# Function to delete a record from ac_list
def delete_ac_list(conn, acreg):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM ac_list WHERE acreg = ?", (acreg,))
        conn.commit()
    except Error as e:
        st.error(f"Error: {e}")

def app():
    st.title('AIRCRAFT LIST')

    conn = create_connection()
    if conn is not None:
        rows = fetch_ac_list(conn)
        df = pd.DataFrame(rows, columns=["acreg", "actype"])

        edited_df = st.data_editor(df,use_container_width = True, num_rows="dynamic")

        if st.button("Save Changes"):
            for index, row in edited_df.iterrows():
                if row["acreg"] not in df["acreg"].values:  # New record
                    insert_ac_list(conn, row["acreg"], row["actype"])
                else:  # Existing record
                    old_row = df.loc[df["acreg"] == row["acreg"]].iloc[0]
                    update_ac_list(conn, old_row["acreg"], row["acreg"], row["actype"])

            st.success("Changes saved successfully!")

        if st.button("Delete Selected"):
            selected_rows = edited_df[edited_df["selected"] == True]
            for index, row in selected_rows.iterrows():
                delete_ac_list(conn, row["acreg"])

            st.success("Selected records deleted successfully!")

        conn.close()

if __name__ == "__main__":
    app()