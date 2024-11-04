import streamlit as st
import sqlite3
import pandas as pd

st.title("Input AC Available")
st.write("Please input the available aircrafts for the day")

# Create a text input box for each field
date = st.date_input("Date:")
a320 = st.number_input("A320:", value=int())
a321_ceo = st.number_input("A321-CEO:",value=int())
a321_neo = st.number_input("A321-NEO:",value=int())
a321_act = st.number_input("A321-ACT:",value=int())
a330 = st.number_input("A330:",value=int())
remark = st.text_area("Remark:")

# Connect to the SQLite database
conn = sqlite3.connect('ac_available.db')
c = conn.cursor()

# When the 'Submit' button is pressed, insert the input data into the database
if st.button('Submit'):
    c.execute("INSERT INTO ac_available (DATE, A320, A321_CEO, A321_NEO, A321_ACT, A330, REMARK) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (date, a320, a321_ceo, a321_neo, a321_act, a330, remark))
    conn.commit()
    st.success("Data inserted into ac_available.db")

# When the 'Update' button is pressed, update the record with the input data
if st.button('Update'):
    c.execute("UPDATE ac_available SET A320 = ?, A321_CEO = ?, A321_NEO = ?, A321_ACT = ?, A330 = ?, REMARK = ? WHERE DATE = ?",
              (a320, a321_ceo, a321_neo, a321_act, a330, remark, date))
    conn.commit()
    st.success("Data updated in ac_available.db")

# When the 'Delete' button is pressed, delete the record with the input date
if st.button('Delete'):
    c.execute("DELETE FROM ac_available WHERE DATE = ?", (date,))
    conn.commit()
    st.success("Data deleted from ac_available.db")

# Read the data from the ac_available table into a DataFrame
df = pd.read_sql_query("SELECT * FROM ac_available", conn)

# Display the DataFrame in Streamlit
st.dataframe(df)