import streamlit as st
from function import *
from import_function import *
import streamlit_shadcn_ui as ui
from streamlit_elements import elements, mui, html
import sqlite3
import streamlit_shadcn_ui as ui
import matplotlib.pyplot as plt
import plotly.graph_objects as go
st.set_page_config(page_title="Schedule Check App", page_icon=":shark:", layout="wide")

st.set_option('deprecation.showPyplotGlobalUse', False)

def app():
    df_ns = None  # Initialize df_ns
    df_pf = None  # Initialize df_pf
    input_date = None  # Initialize input_date
    df_ns_vj_nf = None  # Initialize df_ns_vj_nf

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
            df_ns = fetch_data_by_ns('ns_date') # Lọc, lưu dữ liệu từ database theo ngày vào biến df_ns

            if df_ns is not None:
                
                df_ns_out_in = calculate_out_in(df_ns, ['BASE_OUT', 'BASE_IN'])
                st.table(df_ns_out_in)
            else:
                st.write("The selected data does not have the required columns.")
            with st.expander("Show all data"):
                calculate_flights(df_ns)
                
            df_ns_vj = df_ns[~df_ns['AC'].str.contains('-FREEBIRD')]

            df_ns_vj_nf = df_ns_vj[~df_ns_vj['BASE_IN'].isin(mainbase)] # Df những chuyến night stop tại mainbase và không có chuyến bay đêm
            
            # Những chuyến NS tại SGN
            df_ns_vj_nf_sgn = df_ns_vj_nf[df_ns_vj_nf['BASE_OUT'] == 'SGN']
            # Những chuyến NS tại HAN
            df_ns_vj_nf_han = df_ns_vj_nf[df_ns_vj_nf['BASE_OUT'] == 'HAN']
            # Những chuyến NS tại DAD 
            df_ns_vj_nf_dad = df_ns_vj_nf[df_ns_vj_nf['BASE_OUT'] == 'DAD']
            # Những chuyến NS tại CXR
            df_ns_vj_nf_cxr = df_ns_vj_nf[df_ns_vj_nf['BASE_OUT'] == 'CXR']


            df_ns_vj_actype_counts = df_ns_vj['ACTYPE'].value_counts()

            # Plot actype_counts in Streamlit
            st.bar_chart(df_ns_vj_actype_counts, use_container_width=True)
            st.dataframe(df_ns_vj_nf)
        with col2:
            st.write("Select Preflight Date")
           
            df_pf = fetch_data_by_pf('pf_date')

            if df_pf is not None:
                df_pf_out_in = calculate_out_in(df_pf, ['BASE_OUT', 'BASE_IN'])
                st.table(df_pf_out_in)
            else:
                st.write("The selected data does not have the required columns.")
            
            with st.expander("Show all data"):
                calculate_flights(df_pf)


            df_pf_vj = df_pf[~df_pf['AC'].str.contains('-FREEBIRD')]
            # st.table(actype_pf_count)
            df_pf_vj_actype_counts = df_pf_vj['ACTYPE'].value_counts()
            # Plot actype_counts in Streamlit
            st.bar_chart(df_pf_vj_actype_counts)




## TAB 03 
        with tab3:
            st.write("OMC Overview")
            df_sorted = df_ns_vj_nf_sgn.sort_values('STA')

            st.table(df_sorted)
            st.write("Total AC:", df_ns_vj_nf_sgn.shape[0])
            count_unique_actypes(df_ns_vj_nf_sgn)
            count_inout_= calculate_out_in(df_ns_vj, ['BASE_OUT', 'BASE_IN'])
            st.dataframe(count_inout_)

if __name__ == "__main__":
    app()