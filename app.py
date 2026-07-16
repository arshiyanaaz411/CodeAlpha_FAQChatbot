import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="StyleHub - Help Center", page_icon="🛍️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: linear-gradient(180deg, #fef4f0 0%, #ffffff 100%);
    }
    #MainMenu, footer, header {visibility: hidden;}
    
    .navbar {
        background: linear-gradient(90deg, #9F2B8F, #6C2BD9);
        padding: 18px 25px;
        border-radius: 0px 0px 20px 20px;
        margin: -80px -80px 20px -80px;
        box-shadow: 0 4px 15px rgba(108,43,217,0.3);
    }
    .navbar-title {
        color: white;
        font-size: 26px;
        font-weight: 800;
        margin: 0;
    }
    .navbar-sub {
        color: #f0d9ff;
        font-size: 13px;
        margin: 0;
    }
    
    .chip {
        display: inline-block;
        background: white;
        border: 1.5px solid #9F2B8F;
        color: #9F2B8F;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
        cursor: pointer;
    }
    
    .bot-row {
        display: flex;
        align-items: flex-start;
        margin: 12px 0px;
    }
    .bot-avatar {
        background: linear-gradient(135deg, #9F2B8F, #6C2BD9);
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        margin-right: 10px;
        flex-shrink: 0;
    }
    .bot-msg {
        background: white;
        border: 1px solid #f0e0ea;
        color: #333;
        padding: 14px 18px;
        border-radius: 4px 18px 18px 18px;
        max-width: 70%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        font-size: 14.5px;
        line-height: 1.5;
    }
    
    .user-row {
        display: flex;
        justify-content: flex-end;
        margin: 12px 0px;
    }
    .user-msg {
        background: linear-gradient(135deg, #9F2B8F, #6C2BD9);
        color: white;
        padding: 14px 18px;
        border-radius: 18px 4px 18px 18px;
        max-width: 70%;
        font-size: 14.5px;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(108,43,217,0.25);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #9F2B8F, #6C2BD9);
        color: white;
        border: none;
        border-radius:
