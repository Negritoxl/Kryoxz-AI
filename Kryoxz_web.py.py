import streamlit as st
import os
import google.genai as genai

# Anahtarı kasanın içinden çeker
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Kryoxz AI", page_icon="❄️")
st.title("❄️ Kryoxz AI İnternet Asistanı")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Kryoxz AI'a bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # HATA YÖNETİMİ BURADA BAŞLIYOR
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # 429 hatası kota aşımıdır, kullanıcıya kibarca söyler
            if "429" in str(e):
                st.warning("⚠️ Kota sınırı aşıldı. Lütfen 20 saniye bekleyip tekrar dene.")
            else:
                st.error(f"Bir hata oluştu: {e}")
