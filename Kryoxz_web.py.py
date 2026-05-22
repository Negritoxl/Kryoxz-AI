import streamlit as st
import google.genai as genai

# Anahtarı kasanın içinden çek
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.title("❄️ Kryoxz AI")

# Sohbet geçmişini koru
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmişi ekrana yaz (Sadece yazdırma işlemi, API isteği değil)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# SADECE KULLANICI YAZI YAZDIĞINDA ÇALIŞ
if prompt := st.chat_input("Kryoxz AI'a bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Burası buton gibi davranır; kullanıcı yazmadan buraya girmez!
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ Kota dolu. Lütfen 60 saniye bekleyip sonra yaz.")
            else:
                st.error(f"Hata: {e}")
