import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="StyleHub", page_icon="🛍️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background: linear-gradient(180deg, #fef4f0 0%, #ffffff 100%); }
#MainMenu, footer, header {visibility: hidden;}
.navbar {
    background: linear-gradient(90deg, #9F2B8F, #6C2BD9);
    padding: 18px 25px; border-radius: 0px 0px 20px 20px;
    margin: -80px -80px 20px -80px; box-shadow: 0 4px 15px rgba(108,43,217,0.3);
}
.navbar-title { color: white; font-size: 26px; font-weight: 800; margin: 0; }
.navbar-sub { color: #f0d9ff; font-size: 13px; margin: 0; }
.hero {
    background: linear-gradient(135deg, #9F2B8F, #6C2BD9);
    border-radius: 20px; padding: 40px 30px; text-align: center; color: white; margin-bottom: 20px;
}
.hero h1 { font-size: 34px; font-weight: 800; margin-bottom: 8px; }
.hero p { font-size: 15px; opacity: 0.9; }
.card {
    background: white; border-radius: 16px; padding: 20px; text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #f5eaf0; height: 100%;
}
.card h3 { color: #6C2BD9; font-size: 17px; margin: 10px 0 6px 0; }
.card p { color: #777; font-size: 13px; }
.bot-row { display: flex; align-items: flex-start; margin: 12px 0px; }
.bot-avatar {
    background: linear-gradient(135deg, #9F2B8F, #6C2BD9); color: white;
    width: 36px; height: 36px; border-radius: 50%; display: flex;
    align-items: center; justify-content: center; font-size: 18px; margin-right: 10px; flex-shrink: 0;
}
.bot-msg {
    background: white; border: 1px solid #f0e0ea; color: #333;
    padding: 14px 18px; border-radius: 4px 18px 18px 18px; max-width: 70%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); font-size: 14.5px; line-height: 1.5;
}
.user-row { display: flex; justify-content: flex-end; margin: 12px 0px; }
.user-msg {
    background: linear-gradient(135deg, #9F2B8F, #6C2BD9); color: white;
    padding: 14px 18px; border-radius: 18px 4px 18px 18px; max-width: 70%;
    font-size: 14.5px; line-height: 1.5; box-shadow: 0 2px 8px rgba(108,43,217,0.25);
}
.stButton>button {
    background: linear-gradient(90deg, #9F2B8F, #6C2BD9); color: white;
    border: none; border-radius: 12px; height: 46px; font-weight: 700;
    width: 100%; box-shadow: 0 2px 10px rgba(108,43,217,0.3);
}
.stButton>button:hover { transform: scale(1.02); }
div[data-testid="stTextInput"] input {
    background-color: white; border: 1.5px solid #e8d5e0;
    border-radius: 12px; color: #333; padding: 12px 16px;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [("bot", "Hi there! 👋 I'm your StyleHub assistant. Ask me about orders, shipping, returns, sizing, or payments!")]
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

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
        return "I'm sorry, I couldn't find a good match for that 😔 Try rephrasing, or contact support@stylehub.com."
    return answers[best_idx]

def navbar():
    st.markdown("""
    <div class="navbar">
        <p class="navbar-title">🛍️ StyleHub</p>
        <p class="navbar-sub">Fashion delivered with care</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    st.markdown("""
    <div class="hero" style="margin-top:60px;">
        <h1>🛍️ Welcome to StyleHub</h1>
        <p>Your one-stop destination for trendy fashion</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("### Sign in to continue")
        name = st.text_input("Your Name", placeholder="Enter your name")
        if st.button("Continue ➤"):
            if name.strip() != "":
                st.session_state.username = name
                st.session_state.page = "home"
                st.rerun()
            else:
                st.warning("Please enter your name to continue.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HOME PAGE ----------------
elif st.session_state.page == "home":
    navbar()
    st.markdown(f"""
    <div class="hero">
        <h1>Hey {st.session_state.username}! 👋</h1>
        <p>Discover the latest trends. Shop smart, shop StyleHub.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("### Shop by Category")
    cols = st.columns(4)
    categories = [("👗", "Women"), ("👕", "Men"), ("👟", "Footwear"), ("👜", "Accessories")]
    for col, (icon, name) in zip(cols, categories):
        with col:
            st.markdown(f"<div class='card'><h1>{icon}</h1><h3>{name}</h3><p>Explore now</p></div>", unsafe_allow_html=True)

    st.write("")
    st.write("### Explore StyleHub")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("🏬")
        st.write("**About Us**")
        st.write("Learn about our story and mission")
        if st.button("Visit", key="nav_about"):
            st.session_state.page = "about"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("⚙️")
        st.write("**Our Services**")
        st.write("Shipping, returns, rewards & more")
        if st.button("Visit", key="nav_services"):
            st.session_state.page = "services"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("💬")
        st.write("**Help Center**")
        st.write("Chat with our support assistant")
        if st.button("Visit", key="nav_chat"):
            st.session_state.page = "chatbot"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ABOUT PAGE ----------------
elif st.session_state.page == "about":
    navbar()
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("""
    <div class="hero">
        <h1>About StyleHub</h1>
        <p>Fashion for everyone, everywhere</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="card" style="text-align:left; padding:30px;">
    <p>StyleHub was founded with a simple mission — to make trendy, affordable fashion accessible to everyone across India. 
    From everyday essentials to statement pieces, we curate collections that help you express your unique style.</p>
    <p>With over 50,000 happy customers, fast delivery, and a hassle-free return policy, we're committed to making 
    your shopping experience smooth and enjoyable.</p>
    <p><b>Founded:</b> 2022 &nbsp; | &nbsp; <b>Headquarters:</b> Bengaluru, India &nbsp; | &nbsp; <b>Categories:</b> Women, Men, Footwear, Accessories</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- SERVICES PAGE ----------------
elif st.session_state.page == "services":
    navbar()
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("""
    <div class="hero">
        <h1>Our Services</h1>
        <p>Everything we offer to make shopping easier</p>
    </div>
    """, unsafe_allow_html=True)
    services = [
        ("🚚", "Fast Delivery", "Get your orders delivered within 4-7 days, or choose express for 2-3 days."),
        ("↩️", "Easy Returns", "15-day hassle-free return and exchange policy on all products."),
        ("💳", "Secure Payments", "Multiple payment options with SSL-encrypted secure transactions."),
        ("🎁", "Rewards Program", "Earn points on every purchase and redeem them for exciting discounts."),
        ("📞", "24/7 Support", "Our help center is always available to assist you."),
        ("🔔", "Restock Alerts", "Get notified the moment your favorite items are back in stock.")
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(services):
        with cols[i % 3]:
            st.markdown(f"<div class='card'><h1>{icon}</h1><h3>{title}</h3><p>{desc}</p></div>", unsafe_allow_html=True)
            st.write("")

# ---------------- CHATBOT PAGE ----------------
elif st.session_state.page == "chatbot":
    navbar()
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.write("### 💬 StyleHub Help Center")

    quick_questions = ["📦 Track my order", "↩️ Return policy", "💳 Payment options", "📏 Size guide"]
    quick_map = {
        "📦 Track my order": "How can I track my order?",
        "↩️ Return policy": "What is your return policy?",
        "💳 Payment options": "What payment methods do you accept?",
        "📏 Size guide": "How do I know my size?"
    }
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

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = [("bot", "Hi there! 👋 I'm your StyleHub assistant. Ask me about orders, shipping, returns, sizing, or payments!")]
        st.rerun()
