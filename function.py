import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime
import sqlite3
from sqlite3 import Error

import streamlit as st


# Define the global variable
mainbase = ['SGN', 'HAN', 'DAD', 'CXR', 'HPH','VII','PQC','VCA']


def create_connection_com_fpl():
    conn = None;
    try:
        conn = sqlite3.connect('comflightplan.db') # creates a SQLite database named 'flightplan.db'
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn




def assign_actype(ac):
    if 'A321' in ac and 'NEO' in ac and 'ACT' in ac:
        return 'A321-NEO-ACT'
    elif 'A321' in ac and 'NEO' in ac:
        return 'A321-NEO'
    elif 'NEO' in ac and 'A321' not in ac:
        return 'A321-NEO'
    elif 'A321' in ac:
        return 'A321-CEO'
    elif 'A320' in ac:
        return 'A320'
    elif 'A330' in ac:
        return 'A330'
    else:
        return ac

def process_flightplan(filepath, df_date):
    # Load data
    df = pd.read_excel(filepath)
    if df is None:
        return None

    # Preprocess data
    df.rename(columns={'BASE IN': 'BASE_IN', 'BASE OUT': 'BASE_OUT', 'FLT N0': 'FLT_NO', 'Unnamed: 17': 'MORE_INFOR'}, inplace=True)
    total_row_index = df.loc[df['BASE_IN'] == 'OUT'].index[0]
    df = df.loc[:total_row_index]
    df.drop(df.index[-1], inplace=True)

    new_df = df[['AC', 'BASE_IN', 'BASE_OUT', 'STD', 'ARR', 'ROUTE', 'FLT_NO', 'STD.1', 'STA', 'BLOCK','FREQ', 'FROM', 'TO','MORE_INFOR']].copy()
    new_df.dropna(subset=['AC'], inplace=True)

    # Process 'AC' column
    conditions = [
        new_df['MORE_INFOR'].str.contains('NEO|FREEBIRD|ACT', case=False, na=False),
        (new_df['AC'] == 'A321') & new_df['MORE_INFOR'].isna(),
        new_df['AC'] != 'A330',
        ~new_df['AC'].str.contains('A321|A330|NEO|FREEBIRD|ACT', case=False, na=False)
    ]
    values = [
        new_df['AC'].astype(str) + '-' + new_df['MORE_INFOR'].astype(str),
        new_df['AC'].astype(str) + '-CEO',
        new_df['AC'].astype(str),
        new_df['AC'].astype(str) + '-A320'
    ]
    new_df['AC'] = np.select(conditions, values, default=new_df['AC'])

    # Assign 'ACTYPE' based on 'AC'
    new_df['ACTYPE'] = new_df['AC'].apply(assign_actype)

    # Rename and reset columns
    new_df.rename(columns={'STD': 'DEP', 'STD.1': 'STD'}, inplace=True)
    new_df.reset_index(drop=True, inplace=True)
    new_df.drop(columns=['MORE_INFOR'], inplace=True)

    # Determine 'SECTOR'
    start_index = 0
    sector_counter = 1
    for i in range(len(new_df)):
        if new_df.loc[i, 'BASE_IN'] in mainbase and pd.isna(new_df.loc[i, 'BASE_OUT']):
            if i != 0:
                new_df.loc[start_index:i, 'SECTOR'] = f'Sector {sector_counter}'
                sector_counter += 1
            start_index = i
        elif pd.isna(new_df.loc[i, 'BASE_IN']) and new_df.loc[i, 'BASE_OUT'] in mainbase:
            new_df.loc[start_index:i+1, 'SECTOR'] = f'Sector {sector_counter}'
            start_index = i + 1
        elif new_df.loc[i, 'BASE_IN'] == new_df.loc[i, 'BASE_OUT']:
            new_df.loc[start_index:i, 'SECTOR'] = f'Sector {sector_counter}'
            sector_counter += 1
            start_index = i
    if pd.isna(new_df.loc[len(new_df)-1, 'SECTOR']):
        new_df.loc[start_index:, 'SECTOR'] = f'Sector {sector_counter}'

    # Add 'DATE' column and fill with df_date
    new_df['DATE'] = df_date

    # Define new column order
    cols = ['DATE', 'SECTOR', 'AC','ACTYPE', 'BASE_IN', 'BASE_OUT', 'DEP', 'ARR', 'ROUTE', 'FLT_NO', 'STD', 'STA', 'BLOCK', 'FREQ', 'FROM', 'TO']

    # Reorder the columns
    new_df = new_df[cols]

    # Convert 'STD' and 'STA' to datetime.time objects and then to minutes
    for col in ['STD', 'STA', 'BLOCK']:
        new_df[col] = new_df[col].apply(lambda t: t.hour * 60 + t.minute)

    # Connect to SQLite database
    conn = create_connection_com_fpl()
    if conn is not None:
        # Read the existing data from the database
        df_db = pd.read_sql_query("SELECT * FROM comflightplan", conn)

        # Check if the new data already exists in the database
        if not df_db.equals(new_df):
            # If the new data does not exist in the database, append it
            new_df.to_sql('comflightplan', conn, if_exists='append', index=False)
        else:
            print("The data already exists in the database. Skipping import.")

    return new_df


### Tính tổng số lượng OUT - IN các station -> cần lưu dữ liệu vào 1 bảng để phân tích

def calculate_out_in(df, columns):
    """
    This function calculates and creates a DataFrame based on the provided columns.
    """
    counts = {}
    for column in columns:
        if column not in df.columns:
            print(f"The DataFrame does not have the '{column}' column.")
            return None
        counts[column] = df[column].value_counts()

    # Create DataFrame from results
    result_df = pd.DataFrame({
        'STATION': counts[columns[0]].index,
        'BASE_OUT': counts[columns[0]].values,
        'BASE_IN': counts[columns[1]].reindex(counts[columns[0]].index, fill_value=0).values
    })

    return result_df


def calculate_flights(df):
    if df is None:
        print("DataFrame is None")
        
        return
    
    # Filter rows where 'AC' does not contain 'FREEBIRD'
    df_without_freebird = df[~df['AC'].str.contains('-FREEBIRD')]

    # Filter rows where 'AC' contains 'FREEBIRD'
    df_wetlease = df[df['AC'].str.contains('FREEBIRD')]

    # Calculate total number of flights without FREEBIRD
    total_without_freebird = df_without_freebird.shape[0]

    # Calculate total number of flights with FREEBIRD
    total_wetlease = len(df_wetlease)
    st.write("Total number of flights:", df.shape[0])
    st.write("Total number of Vietjet flights:", total_without_freebird)
    st.write("Total number of Wetlease flights:", total_wetlease)

    return total_without_freebird, total_wetlease


def plot_count_base_in_out(df_ns, df_pf):

    # Define labels
    labels = df_ns.index

    # Define data
    df_ns_out = df_ns['OUT']
    df_ns_in = df_ns['IN']
    df_pf_out = df_pf['OUT']
    df_pf_in = df_pf['IN']

    # Define bar width
    bar_width = 0.35

    # Define bar positions
    r1 = np.arange(len(labels))
    r2 = [x + bar_width for x in r1]

    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Plot data for nightstop
    plt.barh(r1, df_ns_out, color='b', height=bar_width, edgecolor='grey', alpha=0.5, label='BASE OUT -NIGHTSTOP')
    plt.barh(r1, df_ns_in, left=df_ns_out, color='r', height=bar_width, edgecolor='grey', alpha=0.5, label='BASE IN - NIGHTSTOP')

    # Plot data for preflight
    plt.barh(r2, df_pf_out, color='b', height=bar_width, edgecolor='grey', label='BASE OUT - PREFLIGHT')
    plt.barh(r2, df_pf_in, left=df_pf_out, color='r', height=bar_width, edgecolor='grey', label='BASE IN -PREFLIGHT')

    # Add labels and title
    plt.ylabel('STATION')
    plt.xlabel('Total Time')
    plt.title('Total BASE OUT and BASE IN Time by Station')

    # Add yticks on the middle of the group bars
    plt.yticks([r + bar_width / 2 for r in range(len(df_ns_out))], labels)

    # Add a legend
    plt.legend()

    # Add total number on top of each bar
    for i in range(len(df_ns_out)):
        plt.text(x=df_ns_out[i], y=r1[i], s=df_ns_out[i], size=10, color='b')
        plt.text(x=df_ns_in[i], y=r1[i], s=df_ns_in[i], size=10, color='r')

    for i in range(len(df_pf_out)):
        plt.text(x=df_pf_out[i], y=r2[i], s=df_pf_out[i], size=10, color='b')
        plt.text(x=df_pf_in[i], y=r2[i], s=df_pf_in[i], size=10, color='r')

    # Show the plot
    plt.show()
