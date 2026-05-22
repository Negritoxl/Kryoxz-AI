import streamlit as st
import os
import google.genai as genai

# Anahtarı kodun içinden değil, Streamlit'in gizli kasasından çeker
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Kryoxz AI", page_icon="❄️")
st.title("❄️ Kryoxz AI İnternet Asistanı")

# Mesaj geçmişini tut
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana yaz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Yeni kullanıcı girişi
if prompt := st.chat_input("Kryoxz AI'a bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Gemini'a bağlan
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
