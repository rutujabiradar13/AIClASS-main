import streamlit as st
from scr.database.db import create_subject


@st.dialog('create new subject')
def create_subject_dialog(teacher_id):
    st.write("Enter the deatil of your sub")
    sub_id = st.text_input("subject Code", placeholder='cs101')
    sub_name = st.text_input("subject_name", placeholder="introduction to computer science")
    sub_section = st.text_input("section", placeholder="A")

    if st.button("create subject now", type="primary", width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("Subject Ceated Sucessfully !")
                st.rerun()
            except Exception as e:
                st.error(f"Error{str(e)}")
        else:
            st.warning("Please fill all the fied")



