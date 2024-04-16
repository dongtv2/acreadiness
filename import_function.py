import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime
import sqlite3
from sqlite3 import Error
from function import *
import streamlit as st

def display_flightplan_by_date():
    # Create a connection to the SQLite database
    conn = create_connection_com_fpl()

    # Get all unique dates from the 'com flightplan' table
    df_dates = pd.read_sql_query("SELECT DISTINCT DATE FROM comflightplan", conn)

    # Close the connection
    conn.close()

    # Create a select box with the unique dates
    selected_date = st.selectbox("Select a date to view database", df_dates['DATE'])

    # When a date is selected, display the flight plan for that date
    if selected_date is not None:
        # Create a connection to the SQLite database
        conn = create_connection_com_fpl()

        # Get the flight plan for the selected date
        df_flightplan = pd.read_sql_query(f"SELECT * FROM comflightplan WHERE DATE = '{selected_date}'", conn)

        # Close the connection
        conn.close()

        # Display the flight plan
        st.dataframe(df_flightplan)

def fetch_data_by_ns(key):

    # Create a connection to the SQLite database
    conn = create_connection_com_fpl()

    # Get all unique dates from the 'flightplan' table
    df_dates = pd.read_sql_query("SELECT DISTINCT DATE FROM comflightplan", conn)

    # Close the connection
    conn.close()

    # Create a select box with the unique dates
    selected_date = st.selectbox("Select a date", df_dates['DATE'], key=key)

    # When a date is selected, fetch the data for that date
    if selected_date is not None:
        # Create a connection to the SQLite database
        conn = create_connection_com_fpl()

        # Get the data for the selected date
        df_data = pd.read_sql_query(f"SELECT * FROM comflightplan WHERE DATE = '{selected_date}'", conn)

        # Close the connection
        conn.close()

        # Return the data
        return df_data
    
def fetch_data_by_pf(key):

    # Create a connection to the SQLite database
    conn = create_connection_com_fpl()

    # Get all unique dates from the 'flightplan' table
    df_dates = pd.read_sql_query("SELECT DISTINCT DATE FROM comflightplan", conn)

    # Close the connection
    conn.close()

    # Create a select box with the unique dates
    selected_date = st.selectbox("Select a date", df_dates['DATE'], key=key)

    # When a date is selected, fetch the data for that date
    if selected_date is not None:
        # Create a connection to the SQLite database
        conn = create_connection_com_fpl()

        # Get the data for the selected date
        df_data = pd.read_sql_query(f"SELECT * FROM comflightplan WHERE DATE = '{selected_date}'", conn)

        # Close the connection
        conn.close()

        # Return the data
        return df_data
