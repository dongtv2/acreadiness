import streamlit as st
from function import *
from import_function import *
import streamlit_shadcn_ui as ui
from streamlit_elements import elements, mui, html
import sqlite3

st.set_page_config(page_title="Schedule Check App", page_icon=":shark:", layout="wide")

st.set_option('deprecation.showPyplotGlobalUse', False)

def app():
    df_ns = None  # Initialize df_ns
    df_pf = None  # Initialize df_pf
    input_date = None  # Initialize input_date

    st.title('Homepage')
    st.header('Welcome to MOC.AR!')
    st.write('Schedule Check App.')

    tab1, tab2, tab3 = st.tabs(["IMPORT", "COMMERCIAL OVERVIEW", "OMC OVERVIEW"])

    with tab1:
        st.expander("Import commercial flightplan", expanded=True)


        df_date = st.date_input("Select a date", value=None)
        if df_date is not None:
            st.write("Selected date:", df_date.strftime("%m.%d.%Y"))

            uploaded_file = st.file_uploader("Upload Nightstop XLSX file", type='xlsx')
            if uploaded_file is not None:
                df_com = process_flightplan(uploaded_file,df_date)
                st.dataframe(df_com)

        display_flightplan_by_date()

    with tab2:
        col1,col2 = st.columns(2)

        with col1:
            
            st.write("Select Nightstop Date")
            df_ns = fetch_data_by_ns('ns_date')

            if df_ns is not None:
                
                df_ns_out_in = calculate_out_in(df_ns, ['BASE_OUT', 'BASE_IN'])
                st.table(df_ns_out_in)
            else:
                st.write("The selected data does not have the required columns.")
            calculate_flights(df_ns)
        with col2:
            st.write("Select Preflight Date")
           
            df_pf = fetch_data_by_pf('pf_date')

            if df_pf is not None:
                df_pf_out_in = calculate_out_in(df_pf, ['BASE_OUT', 'BASE_IN'])
                st.table(df_pf_out_in)
            else:
                st.write("The selected data does not have the required columns.")

    with tab3:
        st.write("OMC Overview")

if __name__ == "__main__":
    app()