import streamlit as st
from streamlit_option_menu import option_menu

# 1. as sidebar menu
with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Settings'],
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    selected
#
# # 2. horizontal menu
selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
    icons=['house', 'cloud-upload', "list-task", 'gear'],
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected2 == "Home":
    col1, col2,_ = st.columns([1, 1, 4])

    with col1:
        st.write('col1')
        st.selectbox("Main Menu", ["Home", 'Settings'])

    with col2:
        st.write('col2')
        st.date_input("date")


# # 3. CSS style definitions
# selected3 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                         icons=['house', 'cloud-upload', "list-task", 'gear'],
#                         menu_icon="cast", default_index=0, orientation="horizontal",
#                         styles={
#                             "container": {"padding": "0!important", "background-color": "#fafafa"},
#                             "icon": {"color": "orange", "font-size": "25px"},
#                             "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
#                             "nav-link-selected": {"background-color": "green"},
#                         }
#                         )
#


# Define the pages and their file paths
pages = {'Home':'pages/regular_1_Plotting_Demo.py',
         'Continent Data':'pages/regular_2_Mapping_Demo.py',
         }
st.write("ttt")
# Create a list of the page names
page_list = list(pages.keys())

def nav(current_page=page_list[0]):
    with st.sidebar:
        p = option_menu("Page Menu", page_list,
            default_index=page_list.index(current_page),
            orientation="vertical")

        if current_page != p:
            st.switch_page(pages[p])