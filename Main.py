import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random

puan = 0
can = 5

print("Kelime Oyununa Hoş Geldiniz!")
print("Haydi başlayalım... Öncelikle Kendi Kullanıcı adınızı oluşturun ve yazın.")
oyuncu_adi = input("Adınızı girin: ")

seviyeler = {
    "kolay": {
        "kedi": "cat",
        "köpek": "dog",
        "elma": "apple",
        "süt": "milk",
        "güneş": "sun"
    },

    "orta": {
        "muz": "banana",
        "okul": "school",
        "arkadaş": "friend",
        "pencere": "window",
        "sarı": "yellow"
    },

    "zor": {
        "teknoloji": "technology",
        "üniversite": "university",
        "bilgi": "information",
        "telaffuz": "pronunciation",
        "hayal gücü": "imagination"
    }
}

duration = 7
sample_rate = 44100

print("\n🎮 İNGİLİZCE KELİME OYUNU 🎮")
print("Türkçe kelime gösterilecek.")
print("İngilizcesini söylemeye çalış!")
print("Her doğru cevap +5 puan.")
print("5 canın var.\n")

while can > 0:

    print("\nSeviyeler:")
    print("• kolay")
    print("• orta")
    print("• zor")

    seviye = input("\nSeviye seç:kolay/orta/zor ").lower()

    if seviye not in seviyeler:
        print("❌ Geçersiz seviye!")
        continue

    turkce_kelime = random.choice(list(seviyeler[seviye].keys()))
    ingilizce_kelime = seviyeler[seviye][turkce_kelime]

    print("\nTürkçe kelime:")
    print("👉", turkce_kelime)
    print("\nİngilizcesini söyle!")

    input("\nHazırsan Enter'a bas...")

    print("🎤 Kayıt başladı...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    wav.write("output.wav", sample_rate, recording)

    print("✅ Kayıt tamamlandı.")
    print("🔎 Ses analiz ediliyor...")

    recognizer = sr.Recognizer()

    try:

        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("🗣️ Söylediğin:", text)

        if text.lower().strip() == ingilizce_kelime.lower():

            puan += 5

            print("✅ Doğru!")
            print("⭐ Puan:", puan)

            if puan >= 20:
                print("\n🌟 ÇOK BAŞARILISIN! 🌟")
                print(Bir zorluk seçmek ister misin? (kolay/orta /zor))

        else:

            can -= 1

            print("❌ Yanlış!")
            print("Doğru cevap:", ingilizce_kelime)
            print("❤️ Kalan can:", can)

    except Exception as hata:

        can -= 1

        print("⚠️ Ses algılanamadı.")
        print("Hata:", hata)
        print("❤️ Kalan can:", can)

print("\n💀 OYUN BİTTİ!")
print("🏆 Final Puanın:", puan)

# Skoru kaydet
with open("skorlar.txt", "a", encoding="utf-8") as dosya:
    dosya.write(f"{oyuncu_adi},{puan}\n")

# Skor tablosunu göster
print("\n🏆 SKOR TABLOSU 🏆")

try:

    skorlar = []

    with open("skorlar.txt", "r", encoding="utf-8") as dosya:

        for satir in dosya:

            isim, skor = satir.strip().split(",")

            skorlar.append((isim, int(skor)))

    skorlar.sort(key=lambda x: x[1], reverse=True)

    for sira, (isim, skor) in enumerate(skorlar[:10], start=1):
        print(f"{sira}. {isim} - {skor} puan")

except FileNotFoundError:
    print("Henüz skor kaydı bulunamadı.")
