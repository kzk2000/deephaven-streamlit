import os

import streamlit as st


def menu_regular(suffix=None):
    print("***")

    kk = os.listdir()
    print(kk)

    st.sidebar.page_link("pages/regular_1_Plotting_Demo.py", label="Plotting Demo", icon='📈')
    st.sidebar.page_link("pages/regular_2_Mapping_Demo.py", label="Mapping Demo", icon="🌍")
    st.sidebar.page_link("pages/regular_3_DataFrame_Demo.py", label="DataFrame Demo", icon="📊")


def menu_deephaven():
    st.sidebar.page_link("pages/deephaven_1_Math_Plot_Demo.py", label='Math Plot Demo', icon="📐")
    st.sidebar.page_link("pages/deephaven_2_Stock_UI_Dashboard.py", label='Stock UI Dashboard', icon="📈")


def menu(suffix=None):
    st.sidebar.page_link("app.py", label="**Home**", icon="🏠")
    st.sidebar.page_link("pages/appgroup_1_regular.py", label="Regular Apps")
    st.sidebar.page_link("pages/appgroup_2_deephaven.py", label="Deephaven Apps")
    st.sidebar.divider()
    st.sidebar.header(st.session_state['app_group'])
    if st.session_state['app_group'] == 'Regular Apps':
        menu_regular(suffix)

    if st.session_state['app_group'] == 'Deephaven Apps':
        menu_deephaven()

    st.sidebar.divider()
