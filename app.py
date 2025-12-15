import streamlit as st
import time
import random

# --- Page Config ---
st.set_page_config(
    page_title="Kerala Ayurveda Wellness Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling & Theme ---
# Colors:
# Deep Green: #2e5c1d
# Earthy Red: #d84315
# Soft Cream: #fcfdfa
# Text Color: #333333

st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #fcfdfa;
        color: #333333;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2e5c1d !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #fcfdfa;
        border-right: 1px solid #e0e0e0;
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
    }
    
    /* User Message */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #f0f2f6; 
        border-left: 5px solid #d84315;
        color: #333333 !important;
    }
    
    /* Bot Message */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #e8f5e9; /* Light Green */
        border-left: 5px solid #2e5c1d;
        color: #333333 !important;
    }

    /* Force text color for all elements inside chat message */
    [data-testid="stChatMessage"] * {
        color: #333333 !important;
    }
    
    /* Buttons (Standard & Link) */
    .stButton > button, [data-testid="stLinkButton"] > a {
        background-color: #2e5c1d !important;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
        text-decoration: none;
    }
    .stButton > button:hover, [data-testid="stLinkButton"] > a:hover {
        background-color: #d84315 !important;
        color: white !important;
    }

    /* Product Card in Sidebar */
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    .product-price {
        font-size: 1.2rem;
        font-weight: bold;
        color: #d84315;
    }
    .old-price {
        text-decoration: line-through;
        color: #888;
        font-size: 0.9rem;
    }

</style>
""", unsafe_allow_html=True)

# --- Mock RAG Backend (Chat Logic) ---
def get_bot_response(user_input):
    """
    Simulates the RAG model response based on interaction guidelines.
    """
    user_input = user_input.lower()
    
    # 1. Sugar / Diabetes
    if "sugar" in user_input or "diabetes" in user_input or "diabetic" in user_input or "sweet" in user_input:
        return (
            "It is **free from refined white sugar**, which is harmful. However, our Chyavanprash is sweetened with "
            "**Jaggery (Gud) and wild Honey**, which are natural sweeteners essential for the *Lehya* consistency "
            "and to act as carriers (*Yogavahi*) for the herbs. \n\n"
            "⚠️ **Note:** If you are diabetic, please consult your physician, as jaggery still affects blood sugar."
        )

    # 2. Competitors (Dabur, etc.)
    elif "dabur" in user_input or "better" in user_input or "brand" in user_input or "difference" in user_input:
        return (
            "That's a great question! Many commercial brands use **sugar candy (refined sugar)** as the main base to cut costs. "
            "**Kerala Ayurveda** uses **only Jaggery and Honey**.\n\n"
            "We also follow the ancient **Lehya Paaka Vidhi** (slow-cooking process) that preserves the Vitamin C in Amla, "
            "whereas others may overcook or use Amla powder. We ensure **2 whole wild Amlas in every scoop**! 🌿"
        )
    
    # 3. Kids / Safety
    elif "kid" in user_input or "child" in user_input or "baby" in user_input or "safe" in user_input or "age" in user_input:
        return (
            "Yes, absolutely! It is safe for children **above 3 years old**. It helps build their immunity against school-time "
            "colds and coughs. \n\n"
            "👶 **Dosage for Kids:** ½ tablespoon daily."
        )

    # 4. Taste
    elif "taste" in user_input or "flavor" in user_input:
        return (
            "It has a beautifully balanced taste—**sweet** from jaggery & honey, **sour** from fresh wild Amla, and a **mild spicy kick** "
            "from herbs like Pippali. It is delicious and not overly sweet like jam. It tastes like authentic wellness! 😋"
        )
    
    # 5. Price / Buy (Refined to avoid capturing "Why buy")
    elif "price" in user_input or "cost" in user_input or ("buy" in user_input and "why" not in user_input) or "order" in user_input or "shipping" in user_input:
        return (
            "The MRP is ₹410, but it is currently on sale for approximately **₹369**! \n\n"
            "Would you like to order a jar to boost your family's immunity today? I can help you with the link."
        )

    # 6. Benefits / Why Buy
    elif "benefit" in user_input or "why" in user_input or "good" in user_input or "work" in user_input or "use" in user_input:
        return (
            "Kerala Ayurveda Chyavanprash helps you in **5 key ways**:\n\n"
            "🛡️ **Immunity**: Builds resilience against seasonal flus.\n"
            "🔥 **Digestion**: Kindles digestive fire (*Agni*) without being too spicy.\n"
            "🫁 **Respiratory**: Supports clear lungs and breathing.\n"
            "💪 **Strength**: Reduces fatigue and builds vitality (*Ojas*).\n"
            "✨ **Longevity**: An anti-aging *Rasayana* for long-term wellness."
        )

    # 7. Ingredients
    elif "ingredient" in user_input or "contain" in user_input or "made of" in user_input:
        return (
             "Our Chyavanprash is a blend of **over 40 Ayurvedic herbs**! 🌿\n\n"
             "Key ingredients include:\n"
             "🟢 **Wild Amla**: Rich in Vitamin C & Tannins for immunity.\n"
             "🍇 **Draksha (Raisins)**: For energy and infection fighting.\n"
             "🍯 **Wild Honey & Jaggery**: Natural sweeteners (No refined sugar!).\n"
             "🧈 **Cultured Ghee**: For deep tissue nourishment.\n"
             "🌿 **Pippali & Shatavari**: For respiratory and lung health."
        )
    
    # 8. Seasons / Summer / Winter (New)
    elif "summer" in user_input or "winter" in user_input or "season" in user_input or "hot" in user_input:
        return (
            "Chyavanprash is a **Rasayana** suitable for year-round use to build immunity. \n\n"
            "☀️ **In Summer**: If you find it heating, you can take it with a glass of **cold milk**.\n"
            "❄️ **In Winter**: It is excellent for protection against colds and flu. Take it with **warm milk** or warm water.\n\n"
            "Always listen to your body! 🌿"
        )
    
    # Default / General Persona Response
    else:
        return (
            "Namaste! 🙏 I am your **Kerala Ayurveda Wellness Assistant**. \n\n"
            "I'm here to answer your questions about **Benefits**, **Ingredients**, **Dosage**, or **Price**. \n\n"
            "For example, you can ask: \n"
            "- *'What are the key ingredients?'* \n"
            "- *'Is it safe for diabetics?'* \n"
            "- *'How do I take it?'*"
        )

# --- Sidebar Content ---
with st.sidebar:
    st.image("assets/product_image.png", use_container_width=True)
    
    st.markdown("""
        <div class='product-card'>
            <h3>Chyavanprash Lehyam</h3>
            <p>Immunity & Longevity</p>
            <p class='product-price'>₹369 <span class='old-price'>₹410</span></p>
            <p style='color: green; font-weight: bold;'>Save 10%</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.link_button("🛒 Buy Now", "https://keralaayurveda.com/products/chyavanprash", use_container_width=True)
    
    st.markdown("### ✨ Product Highlights")
    st.markdown("""
    - **No Refined Sugar** (Jaggery & Honey only)
    - **2 Whole Wild Amlas** per scoop
    - **GMP Certified**
    - **5000-Year-Old Recipe**
    - **100% Natural**
    """)
    
    st.markdown("---")
    st.markdown("### 🌿 About Us")
    st.info("Kerala Ayurveda has a legacy of over 80 years, bringing authentic healing to the modern world.")

# --- Main Chat Area ---

# Header
col1, col2 = st.columns([1, 8])
with col1:
    st.write("🌿") # Placeholder for Logo if image not available
with col2:
    st.title("Kerala Ayurveda Wellness Assistant")

st.write("Your trusted guide to authentic Ayurvedic immunity.")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 🙏 I am here to guide you on your wellness journey with **Kerala Ayurveda Chyavanprash**. How may I assist you today?"}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick Reply Handlers
def handle_quick_reply(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Force rerun to show user message immediately
    # In a real app we might not need to force rerun if using the input mechanism differently, 
    # but with streamlits execution model, we usually process the input and then rerun.
    # Here we just append to state so the next run loop picks it up if we trigger one,
    # or we can process it immediately.
    
    # Process immediately
    with st.chat_message("assistant"):
        with st.spinner("Consulting the ancient texts..."):
            time.sleep(0.5) # Simulating thinking
            response = get_bot_response(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


# Quick Reply Buttons (A bit tricky in Streamlit to not auto-submit but we can use columns)
st.markdown("### Quick Questions:")
q_col1, q_col2, q_col3 = st.columns(3)

if q_col1.button("Is it sugar-free?"):
    handle_quick_reply("Is it sugar-free?")
    st.rerun()

if q_col2.button(" Safe for kids?"):
    handle_quick_reply("Is it safe for kids?")
    st.rerun()

if q_col3.button("Why is it better?"):
    handle_quick_reply("Why is it better than other brands?")
    st.rerun()


# Chat Input
if prompt := st.chat_input("Ask me about Chyavanprash..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Consulting the ancient texts..."):
            time.sleep(1) # Simulating processing
            response = get_bot_response(prompt)
            st.markdown(response)
    
    # Add Assistant Message
    st.session_state.messages.append({"role": "assistant", "content": response})

