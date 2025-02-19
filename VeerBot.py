import wikipedia as wk
import streamlit as st
from gtts import gTTS


# Custom CSS for styling
st.markdown("""
    <style>
        /* Style Navigation Bar */
        header[data-testid="stHeader"] {
            background-color: #fd9206 !important; /* Red Navbar */
           
        }
        .stApp {
            background-color: #eec187 !important;
        }
        body {
            background-color: #eec187;
            color: #eec187;
        }
        .title {
            text-align: center;
            font-size: 36px;
            color: #FFA500;
        }
        .selectbox, .text_input {
            width: 80%;
            margin: auto;
        }
        .info-box {
            background: rgb(242, 153, 36);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(255, 165, 0, 0.5);
            margin: 20px 0;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 15px;
        }
        .stButton>button {
            background: linear-gradient(45deg, #FFA500, #FF4500);
            border-radius: 8px;
            color: white;
            font-size: 16px;
        }
        .stButton>button:hover {
            background: #FF6347;
            transition: 0.3s;
        }

        /*Scroll Bar */ 
        .scrollable-content {
            max-height: 500px; /* Adjust height as needed */
            overflow-y: auto;
            padding: 10px;
            background: rgb(242, 153, 36);
            color: black;
            border-radius: 5px;
        }

        /* Custom Scrollbar Styling */
        .scrollable-content::-webkit-scrollbar {
            width: 8px;
        }
        .scrollable-content::-webkit-scrollbar-thumb {
            background: #FFA500;
            border-radius: 10px;
        }
        .scrollable-content::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🔥 Indian Warriors Information Chatbot 🔥</h1>", unsafe_allow_html=True)

# Language Selection
select = st.selectbox("🌐 Select Language:", options=["Marathi", "Hindi", "English"])
language_code = 'en'

if select == "Marathi":
    search_name = st.text_input("✍️ एका भारतीय योद्ध्याचे नाव प्रविष्ट करा:")  
    language_code = 'mr'

elif select == "Hindi":
    search_name = st.text_input("✍️ एक भारतीय योद्धा का नाम दर्ज करें:")
    language_code = 'hi'
    
else:
    search_name = st.text_input("✍️ Enter the name of an Indian warrior:")
    language_code = 'en'

if search_name:
    try:
        wk.set_lang(language_code)
        page = wk.page(search_name)

        st.markdown(f"<div class='info-box'><h3>📜 Warrior Name: {search_name}</h3><div class='scrollable-content'>{page.content}</div></div>", unsafe_allow_html=True)
    
        col1, col2, col3 = st.columns(3)

        with col1:
            bt1 = st.button("📄 Summary")
        with col2:
            bt2 = st.button("🖼️ Images")
        with col3:
            bt3 = st.button("🔗 Links")

        # Summary
        sum_text = wk.summary(search_name)
        speak = False
        if bt1:  
            st.markdown(f"<div class='info-box'><p>{sum_text}</p></div>", unsafe_allow_html=True)
        
        speak = True

        if speak:
            audio = st.button("🔊")
            if audio:
                g = gTTS(sum_text, lang=language_code)
                g.save("speech.mp3")
                st.audio("speech.mp3")

        # Images
        if bt2:
            if page.images:
                st.image(list(page.images)[:5])  # Show the first 5 images
            else:
                st.warning("⚠️ No images available.")

        # Links
        if bt3:
            st.markdown(f"[🔗 Click here for more information]({page.url})")

    except wk.exceptions.DisambiguationError:
        st.error("⚠️ The name is ambiguous. Please be more specific.")
    except wk.exceptions.PageError:
        st.error("❌ No page found. Please try a different name.")
    except Exception as e:
        st.error(f"❗ An error occurred: {e}")
else:
    st.info("🔍 Please enter a warrior's name to search for information.")
