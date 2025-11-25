import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ HATA: .env dosyasında GOOGLE_API_KEY bulunamadı!")
else:
    print(f"🔑 API Key bulundu: {api_key[:5]}...{api_key[-3:]}")

    try:
        genai.configure(api_key=api_key)

        print("\n📡 Google AI Sunucularına bağlanılıyor ve modeller çekiliyor...\n")
        print("-" * 40)
        print("KULLANABİLECEĞİN CHAT MODELLERİ:")
        print("-" * 40)

        found_any = False
        # Tüm modelleri listele
        for m in genai.list_models():
            # Sadece metin/chat üretebilen modelleri filtrele
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ {m.name}")
                found_any = True

        if not found_any:
            print("⚠️ Hiçbir uygun model bulunamadı. API Key yetkilerini kontrol et.")

    except Exception as e:
        print(f"\n❌ BEKLENMEYEN HATA: {e}")