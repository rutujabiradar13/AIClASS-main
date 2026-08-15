import streamlit as st

from scr.screen.home_screen import home_screen
from scr.screen.student_screen import student_screen
from scr.screen.teacher_screen import teacher_screen

def main():
    st.set_page_config(
        page_title ="AICLASS Making Attendance Faster Using AI",
        page_icon ="https://img.icons8.com/?size=100&id=MsERXXVyVEs9&format=png&color=000000"
     )

    if "login_type" not in st.session_state:
        st.session_state['login_type']= None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        
        case 'student':
            student_screen()

        case None:
            home_screen()

    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != "student":
            st.session_state.login_type = "student"
            st.rerun()

        if st.session_state.get('is_logged_in') and st.session_state.get('user_role')=='student':
            pass
           

main()