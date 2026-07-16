import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="StyleHub - Help Center", page_icon="🛍️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background: linear-gradient(180deg, #fef4f0 0%, #ffffff 100%); }
#MainMenu, footer, header {visibility: hidden;}
.navbar {
    background: linear-gradient(90deg, #9F2B8F, #6C2BD9);
    padding: 18px 25px;
    border-radius: 0px 0px 20px 20px;
    margin: -80px -80px 20px -80px;
    box-shadow: 0 4px 15px rgba(108,43,217,0.3);
}
.navbar-title { color: white; font-size: 26px; font-weight: 800; margin: 0; }
.navbar-sub { color: #f0d9ff; font-size: 13px; margin: 0; }
.bot-row { display: flex; align-items: flex-start; margin: 12px 0px; }
.bot-avatar {
    background: linear-gradient(135deg, #9F2B8F, #6C2BD9);
    color: white; width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; margin-right: 10px; flex-shrink: 0;
}
.bot-msg {
    background: white; border: 1px solid #f0e0ea; color: #333;
    padding: 14px 18px; border-radius: 4px 18px 18px 18px;
    max-width: 70%; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 14.5px; line-height: 1.5;
}
.user-row { display: flex; justify-content: flex-end; margin: 12px 0px; }
.user-msg {
    background: linear-gradient(135deg, #9F2B8F, #6C2BD9);
    color: white; padding: 14px 18px; border-radius: 18px 4px 18px 18px;
    max-width: 70%; font-size: 14.5px; line-height: 1.5;
    box-shadow: 0 2px 8px rgba(108,43,217,0.25);
}
.stButton>button {
    background: linear-gradient(90deg, #9F2B8F, #6C2BD9);
    color: white; border: none; border-radius: 12px; height: 46px;
    font-weight: 700; width: 100%; box-shadow: 0 2px 10px rgba(108,43,217,0.3);
}
.stButton>button:hover { transform: scale(1.02); }
div[data-testid="stTextInput"] input {
    background-color: white; border: 1.5px solid #e8d5e0;
    border-radius: 12px; color: #333; padding: 12px 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <p class="navbar-title">🛍️ StyleHub Help Center</p>
    <p class="navbar-sub">We're here to help 24/7 · Ask me anything!</p>
</div>
""", unsafe_allow_html=True)

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
        return "I'm sorry, I couldn't find a good match for that 😔 Try rephrasing, or contact support@stylehub.com for further help."
    return answers[best_idx]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("bot", "Hi there! 👋 I'm your StyleHub assistant. Ask me about orders, shipping, returns, sizing, or payments!")]
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

quick_questions = ["📦 Track my order", "↩️ Return policy", "💳 Payment options", "📏 Size guide"]
quick_map = {
    "📦 Track my order": "How can I track my order?",
    "↩️ Return policy": "What is your return policy?",
    "💳 Payment options": "What payment methods do you accept?",
    "📏 Size guide": "How do I know my size?"
}

st.write("**Quick questions:**")
chip_cols = st.columns(4)
for i, q in enumerate(quick_questions):
    with chip_cols[i]:
        if st.button(q, key=f"chip_{i}"):
            st.session_state.pending_query = quick_map[q]

st.write("")

for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f'<div class="user-row"><div class="user-msg">{msg}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-row"><div class="bot-avatar">🤖</div><div class="bot-msg">{msg}</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed", key="user_query")
with col2:
    send_clicked = st.button("Send ➤")

final_query = None
if send_clicked and user_input.strip() != "":
    final_query = user_input
elif st.session_state.pending_query:
    final_query = st.session_state.pending_query
    st.session_state.pending_query = None

if final_query:
    st.session_state.chat_history.append(("user", final_query))
    response = get_best_answer(final_query)
    st.session_state.chat_history.append(("bot", response))
    st.rerun()

with st.sidebar:
    st.header("🛍️ StyleHub")
    st.caption("Your fashion, delivered with care.")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = [("bot", "Hi there! 👋 I'm your StyleHub assistant. Ask me about orders, shipping, returns, sizing, or payments!")]
        st.rerun()
