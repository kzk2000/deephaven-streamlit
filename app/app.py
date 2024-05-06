import streamlit as st

from menu import menu
import logging

st.session_state['app_group'] = ''
menu()

st.header("Entry title")

