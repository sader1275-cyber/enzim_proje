# -------------------------
# UYUM SKORU FONKSİYONU
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
# RİSK BELİRLEME
# -------------------------
def risk_belirle(genel_skor):

    if genel_skor >= 80:
        return "Düşük Risk"
    elif genel_skor >= 60:
        return "Orta Risk"
    elif genel_skor >= 40:
        return "Yüksek Risk"
    else:
        return "Kritik Risk"


# -------------------------
# YORUM MOTORU
# -------------------------
def yorum_uret(genel_skor):

    if genel_skor >= 80:
        return "Enzim seçilen koşullar için oldukça uygundur. Yüksek verim ve stabilite beklenir."

    elif genel_skor >= 60:
        return "Enzim genel olarak uyumludur ancak bazı optimizasyonlar (pH/sıcaklık) gerekebilir."

    elif genel_skor >= 40:
        return "Enzim orta seviyede uyum göstermektedir. Deneysel risk bulunmaktadır."

    else:
        return "Bu enzim seçilen koşullar için uygun değildir. Kullanım önerilmez."