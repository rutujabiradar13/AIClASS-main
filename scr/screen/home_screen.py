import streamlit as st
from scr.components.header import header_home

from scr.ui.base_layout import style_base_layout
from scr.ui.base_layout import style_background_home

def home_screen():

    style_base_layout()
    style_background_home()
    header_home()
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I am Teacher")
        st.image("https://cdn-icons-png.flaticon.com/512/1995/1995574.png", width=200)
        if st.button( "teacher portal" , type='primary', icon=':material/arrow_outward:', icon_position="right"):
            st.session_state["login_type"]="teacher"
            st.rerun()

    with col2:
        st.header("I am Student")
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=200)
        if st.button("student portal", type='primary', icon=':material/arrow_outward:', icon_position="right"):
            st.session_state["login_type"]="student"

            st.rerun()


    