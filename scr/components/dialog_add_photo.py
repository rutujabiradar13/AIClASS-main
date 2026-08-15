import streamlit as st
from scr.database.db import enroll_student_to_subject
from scr.database.config import supabase
from PIL import Image


import time


@st.dialog('Capture or upload photo')
def add_photo_dialog():
    st.write('Add classroom photo to scan for attendance ')

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1, t2 = st.columns(2)
    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'

    with t2:
            type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
            if st.button('upload photo', type=type_upload, width='stretch'):
                st.session_state.photo_tab = 'upload'
       
    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('take photo', key='dialog_cam')

        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo)) 
            st.toast('photo Captured')
            st.rerun()

    if st.session_state.photo_tab == 'upload':
            uploaded_photo = st.file_uploader('Choose image  files', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key='dialog_upload')
    
            if uploaded_photo:
                for f in uploaded_photo:
                    st.session_state.attendance_images.append(Image.open(f)) 

                    st.toast('Photo uploaded sucessfully')
                    st.rerun()

    st.divider()
    if st.button('Done', type="primary", width="stretch"):
        st.rerun()
    
        
    

        