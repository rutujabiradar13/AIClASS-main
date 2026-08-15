import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style ="background:linear-gradient(135deg, #FFFFFF 0%, #F3E8FF 100%);border: 1px solid #D8B4FE; border-left: 7px solid #8B5CF6; padding:25px; border-radius:20px ;margin-bottom: 20px; box-shadow: 0 6px 20px rgba(124, 58, 237, 0.15);">
        <h3 style="margin: 0 0 12px 0; color: #4C1D95;  font-size: 1.4rem; font-weight: 700;">{name}</h3>
        <p style ="background: #EDE9FE; color:#6D28D9; margin:10px 0; padding: 6px 12px; border-radius: 10px; font-size: 0.9rem; font-weight: 600;">Code <span style="background :#EDE9FE; color: #6D28D9; padding:2px 8px; border_radius:10px; font-size: 0.9rem; font-weight: 600;">:{code} | Section : {section}</p>

        """

    if stats: 
        html +="""
        <div style=" diaplay: flex; gap:8px; flex-wrap:wrap; margin-top: 16px;">
        """

        for  label, value in stats:
            html += f'<div style="background:#FFFFFF; color: #5B21B6; padding:8px 14px; border-radius:12px; font-size: 0.9rem;border: 1px solid #DDD6FE; box-shadow: 0 2px 6px rgba(124, 58, 237, 0.08); ">{value}<b>{label}</b></div>'

        html +="</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()

        


