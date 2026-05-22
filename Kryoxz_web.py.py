
import streamlit as st
import google.genai as genai

# --- SADECE GEREKLİ OLDUĞUNDA BAĞLAN ---
st.title("❄️ Kryoxz AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekrana getir
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı yazı yazdığı anda çalışır
if prompt := st.chat_input("Bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # API anahtarını burada, yani SADECE soru sorulduğunda çekiyoruz
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.warning("⚠️ Bir hata oluştu. Lütfen sayfayı yenileme, sadece bekle ve tekrar dene.")
            st.write(f"Detay: {e}")
