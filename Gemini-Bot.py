import streamlit as st 
from streamlit_chat import message 
from datetime import date
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import os

# about the chat bot 
def chat_bot():
    # Initialize session state with model start chat message
    if 'chat' not in st.session_state:
        model = genai.GenerativeModel('gemini-pro')
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.history = []

    # Initialize session state with todays date
    if 'today_date' not in st.session_state:
        st.session_state.today_date = date.today().strftime("%d %B %Y")

    st.markdown(f"""
    <style>
        /* Set the background image for the entire app */
        .stApp {{
            background-image: url("https://i.pinimg.com/736x/29/51/8d/29518df9a720818938a3a58cf6c026df.jpg");
            background-size: 100px;
            background-repeat:no;
            background-attachment: auto;
            background-position:center;
        }}
        .user-message {{
            border-radius: 10px;
            padding: 20px;
            margin: 5px 0;
            max-width: 100%;
            align-self: flex-end;
            background-color: #dcf8c6;
        }}
        .bot-message {{
        border-radius: 10px;
        align-self: flex-start;
        padding: 10px;
        margin: 5px 0;
        max-width: 80%;
        background-color: #ffffff;
        border: 1px solid #e5e5e5;
                }}
        .chat-date {{
            text-align: center;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100px;
            background-color: #F0F0F0;
            margin: -15px auto;
            padding: 5px;
        }}
        .message-container {{
            display: flex;
            flex-direction: column;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Display the chat history
    st.markdown(f'<div class="chat-date" style="align:center;">{st.session_state.today_date}</div>', unsafe_allow_html=True)
    for message in st.session_state.history:
        st.markdown(f'<div class="message-container"><div class="user-message">{message["user"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="message-container"><div class="bot-message">{message["bot"]}</div></div>', unsafe_allow_html=True)

    # Function to add message to history
    def add_message(user, bot):
        st.session_state.history.append({"user": user, "bot": '🤖\n\n'+bot})

    # Function to handle question input and response
    def handle_question(question):
        try:
            response = st.session_state.chat.send_message(question)
            add_message(question, response.text)
        except Exception as e:
            st.error(f"Error generating response: {e}")

    # Input box for user questions
    question = st.chat_input("Say something")
    if question:
        handle_question(question)
        st.experimental_rerun()

# about the image 
def image_search_bot():
    st.markdown(f"""
    <style>
        /* Set the background image for the entire app */
        .stApp {{
            background-image:url("https://getwallpapers.com/wallpaper/full/2/1/4/1402363-free-download-cool-plain-backgrounds-2560x1600-lockscreen.jpg");
            background-size: 1300px;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
      
        </style>
    """, unsafe_allow_html=True)
    model=genai.GenerativeModel("gemini-1.5-flash-latest")
    uploaded_file = st.file_uploader("Choose a image file",type=["png","jpg","jpeg"])
    if uploaded_file is not None:
        img=Image.open(uploaded_file)
        st.write(img)
        prompt=st.text_input("Enter what you want to find image:")
        button=st.button("Search")
        if button:
            response=model.generate_content([prompt,img])
            st.text_area("",response.parts)
            
# text  
def text_search_bot():
    st.markdown(f"""
    <style>
        /* Set the background image for the entire app */
        .stApp {{
            background-image:url("https://tse3.mm.bing.net/th?id=OIP.1Wd11So0xosR8h5LQNwhigHaEo&pid=Api&P=0&h=180");
            background-size: 1300px;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
      
        </style>
    """, unsafe_allow_html=True)
    model = genai.GenerativeModel('gemini-pro')
    query=st.text_input("Enter what you want to search:")
    button=st.button("Search")
    if button:
        response = model.generate_content(["Write the answer for  the given query in 3 lines", query])
        st.text_area("",response.text)
    
            
# main code 
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.sidebar.title("Select your Choice ")
file_type = st.sidebar.radio("Choose your BOT", ("Chat bot", "Image bot","Text bot"))

if file_type == "Chat bot":
    st.title("                  GeminiAI chat bot 🤖")
    chat_bot()
elif file_type == "Image bot":
    st.title("    GeminiAI Image bot 📸 ")
    image_search_bot()  
elif file_type == "Text bot":
    st.title("  GeminiAI text bot  📖 ")
    text_search_bot()   