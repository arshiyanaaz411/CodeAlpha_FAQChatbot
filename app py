import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="FAQ Chatbot", page_icon="👗", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Fira+Code:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1a3d 0%, #0d0d1f 45%, #05050f 100%);
    }
    .main-title {
        font-size: 44px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #58a6ff, #bc8cff, #ff7eb3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #9aa0b4;
        margin-bottom: 25px;
        font-size: 15px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4A90E2, #9B59B6);
        color: white;
        border: none;
        border-radius: 10px;
        height: 46px;
        font-weight: 700;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(88,166,255,0.5);
    }
    .user-msg {
        background: linear-gradient(90deg, #4A90E2, #9B59B6);
        color: white;
        padding: 12px 18px;
        border-radius: 15px 15px 0px 15px;
        margin: 8px 0px;
        max-width: 75%;
        margin-left: auto;
        font-family: 'Poppins', sans-serif;
    }
    .bot-msg {
        background: #14142b;
        border: 1px solid #2e2e55;
        color: #e6e6f0;
        padding: 12px 18px;
        border-radius: 15px 15px 15px 0px;
        margin: 8px 0px;
        max-width: 75%;
        font-family: 'Poppins', sans-serif;
    }
    div[data-testid="stTextInput"] input {
        background-color: #14142b;
        border: 1px solid #2e2e55;
        border-radius: 10px;
        color: #e6e6f0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">👗 StyleHub FAQ Chatbot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ask me anything about orders, shipping, returns & more!</p>', unsafe_allow_html=True)

faqs = {
    "What are your shipping charges?": "We offer free shipping on orders above ₹999. For orders below that, a flat ₹99 shipping fee applies.",
    "How long does delivery take?": "Standard delivery takes 4-7 business days. Express delivery takes 2-3 business days.",
    "Do you offer cash on delivery?": "Yes, Cash on Delivery (COD) is available for all orders within India.",
    "What is your return policy?": "You can return any product within 15 days of delivery, provided it is unused and has original tags attached.",
    "How do I exchange a product?": "Go to 'My Orders', select the item, and click 'Exchange'. Choose your preferred size or color and we'll process it within 3-5 days.",
    "How can I track my order?": "You will receive a tracking link via SMS and email once your order is shipped. You can also check status under 'My Orders'.",
    "What payment methods do you accept?": "We accept Credit/Debit Cards, UPI, Net Banking, and Cash on Delivery.",
    "Is my payment information secure?": "Yes, all transactions are encrypted with SSL security and we do not store your card details.",
    "How do I know my size?": "Check our Size Guide page under every product listing. It includes detailed measurements for accurate fitting.",
    "Can I cancel my order?": "Orders can be cancelled within 24 hours of placing them, as long as they haven't been shipped yet.",
    "Do you offer international shipping?": "Currently we only ship within India. International shipping will be available soon.",
    "How do I contact customer support?": "You can reach us via email at support@stylehub.com or call us at 1800-123-4567, Monday to Saturday, 9 AM to 7 PM.",
    "Are the product colors accurate in photos?": "We try our best to display accurate colors, but slight variations may occur due to screen settings and lighting.",
    "Do you have a loyalty or rewards program?": "Yes! Join StyleHub Rewards to earn points on every purchase, redeemable for discounts on future orders.",
    "Can I modify my order after placing it?": "Unfortunately, orders cannot be modified once placed. You may cancel within 24 hours and place a new order instead.",
    "What if I receive a damaged product?": "Please contact support within 48 hours of delivery with photos of the damaged item, and we'll arrange a replacement or refund.",
    "Do you restock sold-out items?": "Popular items are usually restocked within 2-3 weeks. You can click 'Notify Me' on the product page to get an alert.",
    "How do I apply a discount coupon?": "Enter your coupon code at checkout in the 'Apply Coupon' box before making payment."
}

questions = list(faqs.keys())
answers = list(faqs.values())

vectorizer = TfidfVectorizer(stop_words="english")
question_vectors = vectorizer.fit_transform(questions)

def get_best_answer(user_query):
    user_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(user_vector, question_vectors)
    best_idx = similarities.argmax()
    best_score = similarities[0][best_idx]
    if best_score < 0.2:
        return "I'm sorry, I couldn't find a good match for that. Try rephrasing your question, or contact support@stylehub.com for further help."
    return answers[best_idx]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("💡 Try asking about:")
    st.write("• Shipping & delivery")
    st.write("• Returns & exchanges")
    st.write("• Payments")
    st.write("• Order tracking")
    st.write("• Sizing")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f'<div class="user-msg">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg}</div>', unsafe_allow_html=True)

user_input = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed", key="user_query")

col1, col2 = st.columns([5, 1])
with col2:
    send_clicked = st.button("Send ➤")

if send_clicked and user_input.strip() != "":
    st.session_state.chat_history.append(("user", user_input))
    response = get_best_answer(user_input)
    st.session_state.chat_history.append(("bot", response))
    st.rerun()
