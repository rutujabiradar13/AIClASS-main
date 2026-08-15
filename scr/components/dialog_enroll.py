import streamlit as st
from scr.database.db import enroll_student_to_subject
from scr.database.config import supabase
import time


@st.dialog('enroll in subject')
def enroll_dialog():
    st.write('enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary',width='stretch'):
        if join_code:
            res = supabase.table('subjects').select('subject_id, name , subject_code').eq('subject_code', join_code).execute()
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                check = supabase.table('student_subject').select('*').eq('subject_id', subject[ 'subject_id']).eq('student_id', student_id).execute()
                if check.data:
                    st.warning('You are already enrolledin this program')
                else:
                    enroll_student_to_subject(student_id, subject[ 'subject_id'])
                    st.success("Succesfully enrolled !")
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning('please Enter a subject code')
   