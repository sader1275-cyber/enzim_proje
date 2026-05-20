import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from hesaplama import yorum_uret, risk_belirle

# -------------------------
# FASTA OKUMA
# -------------------------
def proteinleri_yukle(dosya_yolu):

    proteinler = {}

    with open(dosya_yolu, "r") as file:
        lines = file.readlines()

    current_name = ""

    for line in lines:

        line = line.strip()

        if line.startswith(">"):

            parts = [p.strip() for p in line[1:].split("|")]

            isim = parts[0]
            opt_temp = float(parts[1].split(":")[1])
            opt_ph = float(parts[2].split(":")[1])
            tip = parts[3].split(":")[1]

            proteinler[isim] = {
                "sicaklik": opt_temp,
                "ph": opt_ph,
                "tip": tip,
                "sekans": ""
            }

            current_name = isim

        else:
            proteinler[current_name]["sekans"] += line

    return proteinler


# -------------------------
# SKOR FONKSİYONU
# -------------------------
def uyum_skoru(kullanici, optimal):

    fark = abs(kullanici - optimal)

    if fark <= 2:
        return 100
    elif fark <= 5:
        return 80
    elif fark <= 10:
        return 50
    else:
        return 20


# -------------------------
# STREAMLIT
# -------------------------
st.set_page_config(page_title="NanoVita Pro", layout="wide")
st.title("🧪 NanoVita Karar Destek Sistemi")

proteinler = proteinleri_yukle("protein_veritabani.fasta")


# -------------------------
# ENZİM SEÇİM
# -------------------------
secilen_enzim = st.selectbox("Bir enzim seç", list(proteinler.keys()))
enzim = proteinler[secilen_enzim]

st.success(f"Seçilen enzim: {secilen_enzim}")


# -------------------------
# BİLGİLER
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.info(f"Tip: {enzim['tip']}")
    st.info(f"Sıcaklık: {enzim['sicaklik']} °C")

with col2:
    st.info(f"pH: {enzim['ph']}")
    st.info(f"Uzunluk: {len(enzim['sekans'])}")


# -------------------------
# INPUT
# -------------------------
kullanici_sicaklik = st.slider("Sıcaklık", 20, 80, 37)
kullanici_ph = st.slider("pH", 0.0, 14.0, 7.0)


# -------------------------
# SKORLAR
# -------------------------
sicaklik_skor = uyum_skoru(kullanici_sicaklik, enzim["sicaklik"])
ph_skor = uyum_skoru(kullanici_ph, enzim["ph"])

genel_skor = int((sicaklik_skor + ph_skor) / 2)


# -------------------------
# RİSK + YORUM
# -------------------------
risk = risk_belirle(genel_skor)
yorum = yorum_uret(genel_skor)

st.subheader("⚠️ Risk")
st.info(risk)

st.subheader("🧠 Yorum")
st.success(yorum)


# -------------------------
# TABLO
# -------------------------
st.subheader("📊 Karşılaştırma")

sonuclar = []

for isim, enz in proteinler.items():

    s1 = uyum_skoru(kullanici_sicaklik, enz["sicaklik"])
    s2 = uyum_skoru(kullanici_ph, enz["ph"])

    toplam = int((s1 + s2) / 2)

    sonuclar.append({
        "Enzim": isim,
        "Tip": enz["tip"],
        "Genel": toplam
    })

df = pd.DataFrame(sonuclar)
st.dataframe(df)


# -------------------------
# GRAFİK (KESİN DOĞRU YER)
# -------------------------
st.subheader("📊 Görsel Analiz")

if sonuclar:

    isimler = [i["Enzim"] for i in sonuclar]
    skorlar = [i["Genel"] for i in sonuclar]

    fig, ax = plt.subplots()
    ax.bar(isimler, skorlar)

    ax.set_ylabel("Skor")
    ax.set_title("Enzim Performans")

    st.pyplot(fig)


# -------------------------
# EN İYİ ENZİM
# -------------------------
st.subheader("🏆 En Uygun Enzim")

en_iyi = max(sonuclar, key=lambda x: x["Genel"])

st.success(f"{en_iyi['Enzim']} ({en_iyi['Genel']}/100)")


# -------------------------
# RAPOR
# -------------------------
st.subheader("📄 Rapor")

if st.button("Rapor Oluştur"):

    rapor = f"""
NanoVita Rapor

Enzim: {secilen_enzim}
Skor: {genel_skor}
Risk: {risk}
Yorum: {yorum}

En İyi Enzim: {en_iyi['Enzim']}
"""

    st.text_area("Rapor", rapor, height=250)
    st.download_button("İndir", rapor, "rapor.txt")