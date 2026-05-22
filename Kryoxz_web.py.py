import streamlit as st
import google.genai as genai

# Anahtarı kasanın içinden çek
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.title("Kryoxz AI")

# Sohbeti tut
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sadece sen yazınca çalışır
if prompt := st.chat_input("Bir şey yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # API'ye bağlan
            response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            st.error("Şu an çok yoğun, lütfen 1 saat sonra dene.")
