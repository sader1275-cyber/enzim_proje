# -------------------------
# FASTA OKUMA FONKSİYONU
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
# BASİT FORMATTING
# -------------------------
def format_baslik(text):
    return f"🧪 {text}"


# -------------------------
# RAPOR METNİ (İLERİDE PDF İÇİN)
# -------------------------
def rapor_olustur(enzim, skor, risk, yorum):

    return f"""
ENZİM ANALİZ RAPORU
--------------------
Enzim: {enzim}
Genel Skor: {skor}/100
Risk: {risk}
Yorum: {yorum}
"""