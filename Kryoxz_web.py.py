import streamlit as st
from google import genai
from google.genai import types

# Web sayfasının sekme ayarları
st.set_page_config(page_title="Kryoxz AI", page_icon="🚀", layout="centered")

# 🎨 Gelişmiş Siber/Hacker Teması (CSS Tasarımı)
st.markdown("""
    <style>
    .stApp { background-color: #111111 !important; }
    .baslik {
        color: #FF7F00;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .user-box {
        background-color: #222222; padding: 12px; border-radius: 8px;
        border-left: 5px solid #FFFF00; margin-bottom: 15px; color: #FFFF00;
        font-family: 'Courier New', Courier, monospace;
    }
    .bot-box {
        background-color: #1a1a1a; padding: 12px; border-radius: 8px;
        border-left: 5px solid #FF0000; margin-bottom: 15px; color: #FF0000;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="baslik">❄️ Kryoxz AI İnternet Asistanı</div>', unsafe_allow_html=True)

API_KEY = "AIzaSyDmxRBi-9mKYVgkaO1NaNrhm_nk4x2cGds"

# 🔑 En Güvenli İstemci ve Sohbet Başlatma Mantığı
if "chat" not in st.session_state:
    try:
        # Client nesnesini doğrudan session_state içinde saklayarak kapanmasını önlüyoruz
        st.session_state.client = genai.Client(api_key=API_KEY)
        kryoxz_config = types.GenerateContentConfig(
            system_instruction=(
                "Senin adın 'Kryoxz AI'. Sen zeki, yardımsever, fütüristik ve gelişmiş bir yapay zeka asistanısın. "
                "Seni Eren geliştirdi ve kurdu. Sana kim olduğun sorulduğunda 'Ben Kryoxz AI'ım' demelisin. "
                "Seni kimin kurduğu sorulduğunda gururla 'Beni Eren kurdu' demelisin."
            ),
            temperature=0.7
        )
        st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash", config=kryoxz_config)
    except Exception as e:
        st.error(f"Bağlantı başlatılamadı: {e}")

# Sohbet geçmişi hafızası
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Kryoxz AI: Sistem başarıyla başlatıldı. Merhaba Eren, web sunumuna hazırım! 😊"}
    ]

# Eski mesajları ekrana bas
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-box"><b>Siz:</b> {msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-box">{msg["text"]}</div>', unsafe_allow_html=True)

# Girdi formu
with st.form("mesaj_formu", clear_on_submit=True):
    kullanici_girdisi = st.text_input("Kryoxz AI'a bir şeyler yazın...", placeholder="Buraya yazın...")
    gonder = st.form_submit_button("Gönder")

if gonder and kullanici_girdisi:
    st.session_state.messages.append({"role": "user", "text": kullanici_girdisi})
    
    with st.spinner("Kryoxz AI düşünüyor..."):
        try:
            # Doğrudan hafızadaki chat üzerinden mesaj gönderiyoruz
            response = st.session_state.chat.send_message(kullanici_girdisi)
            cevap = response.text
        except Exception as e:
            cevap = f"Bir hata oluştu: {e}"
            
    st.session_state.messages.append({"role": "bot", "text": f"Kryoxz AI: {cevap}"})
    st.rerun()
