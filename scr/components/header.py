import streamlit as st

def header_home():
   
    logo_url = "https://img.icons8.com/?size=100&id=MsERXXVyVEs9&format=png&color=000000"

    st.markdown(f""" 
        <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; margin-bottom: 30px;">
        <img src="{logo_url}" style="height: 150px; margin-right: 15px;" />

        <h1 style="text-align: center; color: #E0E3FF; margin: 0;">
        AI <br/> CLASS
        </h1>
        </div>
    
                """, unsafe_allow_html=True)

def header_dashboard():
    
    logo_url = "https://img.icons8.com/?size=100&id=MsERXXVyVEs9&format=png&color=000000"

    st.markdown(f""" 
        <div style="display: flex; flex-direction: row; align-items: center; justify-content: center; margin-bottom: 30px;">
        <img src="{logo_url}" style="height: 100px; margin-right: 15px;" />

        <h1 style="text-align: center; color: #E0E3FF; margin: 0;">
        AI <br/> CLASS
        </h1>
        </div>
    
                """, unsafe_allow_html=True)