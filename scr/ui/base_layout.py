import streamlit as st


def style_background_home():
    st.markdown(
        """
        <style>
        .stApp {
            background: #E0B0FF;
        }

        .stApp div[data-testid="stColumn"] {
            background-color: #E0E3FF !important;
            padding: 1rem !important;
            border-radius: 1.5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
        .stApp {
            background: #E0B0FF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');

        #MainMenu {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            display: none;
        }

        footer {
            display: none;
        }

        .block-container {
            padding-top: 1rem;
        }

        h1 {
            font-family: 'Roboto', sans-serif !important;
            font-size: 2.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
        }

        h2 {
            font-family: 'Roboto', sans-serif !important;
            font-size: 2.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
        }

        h3,
        h4,
        p {
            font-family: 'Outfit', sans-serif;
        }

        button {
            border-radius: 1.5rem !important;
            background-color: #E0459E !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }

        button:hover,
        button[kind="secondary"]:hover {
            border-radius: 1.5rem !important;
            background-color: #E0459E !important;
            color: purple !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }

        button:active,
        button[kind="tertiary"]:active {
            border-radius: 1.5rem !important;
            background-color: #E0459E !important;
            color: black !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )