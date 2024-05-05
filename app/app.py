import streamlit as st

from menu import menu

st.session_state['app_group'] = ''
menu()

st.header("Entry title")

