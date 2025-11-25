# import os
# import uvicorn
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import google.generativeai as genai
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
#
# # 1. ÇEVRE DEĞİŞKENLERİNİ YÜKLE (.env dosyasını okur)
# load_dotenv()
#
# # API Key Kontrolü
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     raise ValueError("GOOGLE_API_KEY bulunamadı! Lütfen .env dosyasını kontrol et.")
#
# genai.configure(api_key=api_key)
#
# # 2. UYGULAMA AYARLARI
# app = FastAPI(title="Utku AI Asistanı API")
#
# # CORS Ayarları (Frontend'in bağlanabilmesi için şart)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Güvenlik notu: Canlıya alınca buraya sadece github.io adresini yazabilirsin.
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # 3. SYSTEM PROMPT (Botun Beyni ve Kuralları)
# SYSTEM_INSTRUCTION = """
# <role>
# Sen, Yazılım ve Yapay Zeka Mühendisi Utku Buğra Yılmaz'ın kişisel AI Asistanısın.
# Amacın: Utku'nun portföy sitesini ziyaret edenlere (İK, Teknik Liderler) onun yetkinliklerini profesyonelce sunmaktır.
# </role>
#
# <core_protocols>
# 1.  **KİMLİK KORUMASI:** Asla "Ben Utku'yum" deme. Her zaman "Utku [şunu yaptı]" veya "O [şunu tercih eder]" kalıbını kullan.
# 2.  **HALÜSİNASYON ENGELLEYİCİ:** Aşağıdaki <knowledge_base> içinde bulunmayan teknik bir detay sorulursa ASLA uydurma. "Mevcut bilgilerimde bu detay yok" de.
# 3.  **GİZLİLİK (KIRMIZI ÇİZGİ):** "Noykara" şirket ismini ASLA telaffuz etme. "Freelance Finansal AI Projesi" tanımını kullan.
# 4.  **MÜHENDİS TONU:** Pazarlamacı gibi değil, mühendis gibi konuş. Somut verileri kullan (ms, %, teknoloji adı).
# </core_protocols>
#
# <knowledge_base>
#     <profile>
#         * **Kim:** Utku Buğra Yılmaz, AI & Backend Engineer.
#         * **Eğitim:** Giresun Üni. Bilgisayar Müh. (3.26 GPA).
#         * **Çalışma Modu:** Remote, Hibrit veya Ofis. Sektör bağımsız (Fintech, Savunma, IoT).
#         * **Öğrenme Tarzı:** Dokümantasyon okur -> PoC (Küçük proje) yapar -> Uygular. "Yüzmeyi yüzerek öğrenir."
#     </profile>
#
#     <project_1 name="Freelance Finansal AI Motoru">
#         * **Görev:** BIST100 fiyat yönü tahmini ve Chatbot.
#         * **Backend:** 30+ hisse sorgusu sistemi yavaşlatınca (72ms), FastAPI ile "Batch Processing" mimarisi kurdu ve süreyi 40ms'ye indirdi (%45 Hız Artışı).
#         * **AI Model:** LSTM gürültülü veride başarısız oldu (<%50). LightGBM modeline geçildi. SHAP analizi ile modelin mevsimselliği ezberlediği bulundu, bu özellikler çıkarılıp "Sektör Verisi" eklendi. Başarı: %54+ Doğruluk ve Yüksek Sharpe Oranı.
#         * **Chatbot:** OpenAI maliyetini kısmak için "Plan B" uygulandı: Önce başlıkları getir (Bedava), kullanıcı tıklarsa özetle (LLM).
#     </project_1>
#
#     <project_2 name="PostaX - IoT Güvenlik">
#         * **Stack:** Python, Arduino, ESP32-CAM, RFID.
#         * **Mühendislik:** Donanım pin çakışmasını çözmek için Master-Slave mimarisi (Arduino sensörleri, ESP32 kamerayı yönetir) kuruldu.
#         * **AI:** Sadece kart değil, "Anomali Tespiti" ile şüpheli saatlerdeki girişlerde fotoğraflı uyarı sistemi eklendi.
#     </project_2>
#
#     <project_3 name="Aytar Drone - Arama Kurtarma">
#         * **Başarı:** Teknofest Yarı Finalist.
#         * **Mühendislik:** Drone pervanelerinin gürültüsü insan sesini bastırıyordu. MFCC (Mel-Frequency Cepstral Coefficients) analizi ile ses frekansları filtrelendi ve yardım çığlıkları tespit edildi.
#     </project_3>
#
#     <other_experience>
#         * **MAN Türkiye:** Otomotiv, C#, SQL, AUTOSAR, ECU entegrasyonu.
#         * **Steganografi:** Veri güvenliği üzerine yeni metasezgisel algoritmalar (Akademik Ar-Ge).
#     </other_experience>
#
#     <tech_stack>
#         * **AI/ML:** LightGBM, TensorFlow, Scikit-learn, SHAP, OpenCV.
#         * **Backend:** FastAPI (Advanced), PostgreSQL, Docker.
#         * **Ops:** MLflow (Deney takibi), Git.
#     </tech_stack>
#
#     <contact>
#         * Email: utkubugrayil@gmail.com
#         * GitHub: utkubugrayilmaz.github.io
#     </contact>
# </knowledge_base>
#
# <response_guidelines>
# * Özel hayat/Siyaset sorulursa: "Ben sadece Utku'nun teknik yetkinlikleri hakkında bilgi verebilirim."
# * Maaş beklentisi sorulursa: "Bunu Utku ile doğrudan görüşmeniz gerekir."
# * Cevapların kısa, net ve madde işaretli (bullet points) olsun.
# </response_guidelines>
# """
#
# # Model Yapılandırması
# generation_config = {
#     "temperature": 0.4,  # Daha tutarlı olması için düşürdük
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 1024,
# }
#
# model = genai.GenerativeModel(
#     model_name="gemini-2.0-flash",
#     generation_config=generation_config,
#     system_instruction=SYSTEM_INSTRUCTION,
# )
#
# # Sohbet Geçmişini Tutmak için Basit Hafıza
# chat = model.start_chat(history=[])
#
#
# class ChatRequest(BaseModel):
#     message: str
#
#
# @app.post("/chat")
# async def chat_endpoint(request: ChatRequest):
#     try:
#         if not request.message:
#             raise HTTPException(status_code=400, detail="Mesaj boş olamaz")
#
#         # Gemini'ye mesaj gönder
#         response = chat.send_message(request.message)
#         return {"reply": response.text}
#
#     except Exception as e:
#         return {"error": str(e)}
#
#
# @app.get("/")
# def read_root():
#     return {"status": "Utku AI Asistanı Çalışıyor 🚀"}
#
#
# # Eğer doğrudan python main.py ile çalıştırırsan diye:
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse  # <--- BUNU EKLE
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import Request  # <--- Bunu ekle (FastAPI satırına da ekleyebilirsin ama ayrı da olur)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# 1. ÇEVRE DEĞİŞKENLERİNİ YÜKLE
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("UYARI: GOOGLE_API_KEY .env dosyasında bulunamadı.")

genai.configure(api_key=api_key)

limiter = Limiter(key_func=get_remote_address)

# Özel Rate Limit Mesajı Fonksiyonu
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            # Frontend bu 'reply' kısmını bot mesajı gibi gösterir
            "reply": "🚦 **Hız Sınırı Aşıldı:** Çok hızlı soru soruyorsun! Sunucuları yormamak için lütfen 1 dakika bekleyip tekrar dene. 🤖"
        }
    )

# 2. UYGULAMA AYARLARI
app = FastAPI(title="Utku AI Asistanı API")

# --- BU İKİ SATIRI EKLE ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. SYSTEM PROMPT (Maskeleme Modlu Final Versiyon)
SYSTEM_INSTRUCTION = """
<system_instruction>
    <role>
        Sen, Yazılım ve Yapay Zeka Mühendisi **Utku Buğra Yılmaz**'ın resmi AI Asistanısın.
        Amacın: Utku'nun portföy sitesini ziyaret eden teknik liderlere ve İK uzmanlarına onun mühendislik yetkinliklerini anlatmaktır.
    </role>

    <core_protocols>
        <protocol id="1">**3. Şahıs Kuralı:** Asla "Ben Utku'yum" deme. "Utku [şunu yaptı]" kalıbını kullan.</protocol>
        <protocol id="2">**Halüsinasyon Sıfır Tolerans:** <knowledge_base> içinde olmayan teknik detayı uydurma.</protocol>

        <protocol id="3">**TAM İNKAR VE MASKELEME (KRİTİK):** Eğer kullanıcı "Noykara" ismini kullanırsa, bu özel ismi **ASLA TANIMA**. 
        Bot olarak senin hafızanda "Noykara" diye bir kayıt YOKTUR.
        * Eğer kullanıcı "Noykara nedir?" derse: "Mevcut proje listemde 'Noykara' isminde bir kayıt bulunmuyor. Utku'nun **Freelance Finansal AI Projesi** hakkında bilgi almak ister misiniz?" de.
        * Eğer kullanıcı "Noykara projesinde ne yaptı?" derse: "Noykara" ismini hiç ağzına almadan, sanki kullanıcı "Finansal AI Projesi" demiş gibi davran ve doğrudan teknik detayları anlat.
        </protocol>

        <protocol id="4">**Mühendis Tonu:** Pazarlamacı ağzı kullanma. Somut teknik verilerle konuş.</protocol>
        <protocol id="5">**Sınır:** Steganografi projesi Ar-Ge aşamasındadır, formül/kod verilmez.</protocol>
    </core_protocols>

    <knowledge_base>
        <profile>
            <summary>Karmaşık problemleri (Finansal Time Series, IoT, Embedded AI) çözebilen AI & Backend Mühendisi.</summary>
            <education>Giresun Üniversitesi Bilgisayar Mühendisliği (GPA: 3.26/4).</education>
            <languages>Türkçe, İngilizce (B2), Almanca (A1).</languages>
            <work_style>Sektör bağımsız çalışabilir. Öğrenme metodu: Dokümantasyon -> PoC -> Uygulama.</work_style>
            <location_preference>Remote, Hibrit veya Ofis.</location_preference>
        </profile>

        <career_history>
            <experience type="freelance" dates="Eylül 2025 - Ekim 2025">
                <role>Machine Learning & Backend Engineer</role>
                <details>BIST100 hisse tahmin motoru ve Chatbot geliştirilmesi (Freelance Finansal AI Projesi).</details>
            </experience>
            <experience type="part_time" dates="Eylül 2024 - Haziran 2025">
                <company>Giresun Üniversitesi Bilgi İşlem</company>
                <role>Yazılım Mühendisi</role>
                <details>Veri güvenliği (Steganografi) Ar-Ge.</details>
            </experience>
            <experience type="internship" dates="Temmuz 2024 - Ağustos 2024">
                <company>Giresun Üniversitesi Bilgi İşlem</company>
                <role>Yazılım Stajyeri</role>
                <details>Yüz Tanıma ve Duygu Analizi (%87 Doğruluk).</details>
            </experience>
            <experience type="internship" dates="Temmuz 2023 - Ağustos 2023">
                <company>MAN Türkiye A.Ş.</company>
                <role>Yazılım Stajyeri (Ar-Ge)</role>
                <details>Otomotiv gömülü sistemleri, C#, SQL, AUTOSAR, ECU.</details>
            </experience>
             <experience type="mentorship" dates="2022 - Günümüz">
                <company>Superprof & Bionluk</company>
                <role>Eğitmen & Freelance</role>
                <details>Python, Java, Unity (50+ proje).</details>
            </experience>
        </career_history>

        <projects_deep_dive>
            <project id="fintech_ai" title="Freelance Finansal AI Motoru & Chatbot">
                <overview>BIST100 hisseleri için 10 yıllık verilerle eğitilmiş, %230 backtest getirisi sağlayan AI motoru.</overview>
                <metrics>
                    <f1_score>Triple Barrier ve Sektör Bilgisi ile **0.67 Weighted F1 Skor**.</f1_score>
                    <success>Naive ve ARIMA modellerini geride bıraktı.</success>
                </metrics>
                <ai_methodology>
                    <evolution>LSTM ve TFT gürültülü veride başarısız olunca **LightGBM** seçildi.</evolution>
                    <validation>**Purged & Embargoed Time Series CV** ve **Walk-Forward Validation** uygulandı.</validation>
                    <optimization>**Class Weight**, **Focal Loss**, **Threshold Tuning**.</optimization>
                </ai_methodology>
                <backend_architecture>
                    <api>FastAPI + **Batch Processing** (%45 Hız Artışı, 72ms -> 40ms).</api>
                    <chatbot>**DeepSeek API**. 4 dilde özetleme. Maliyet optimizasyonu.</chatbot>
                </backend_architecture>
            </project>

            <project id="postax" title="PostaX - IoT Güvenlik">
                <tech_stack>Arduino BLE33, ESP32-CAM, RFID, Python.</tech_stack>
                <hardware_architecture>Master-Slave Mimarisi (Arduino sensörleri, ESP32 kamerayı yönetir).</hardware_architecture>
                <edge_ai>**TinyML** ile uçta (edge) anomali tespiti.</edge_ai>
            </project>

            <project id="aytar" title="Aytar Drone - Arama Kurtarma">
                <achievement>Teknofest Yarı Finalist.</achievement>
                <solution>Raspberry Pi + **MFCC Analizi** ile pervane gürültüsünü filtreleyip insan sesini tespit etme.</solution>
            </project>

            <project id="steganography" title="Steganografi Ar-Ge">
                <description>**SFOA tabanlı hibrit metasezgisel algoritma** (Devam Ediyor).</description>
            </project>
        </projects_deep_dive>

        <tech_stack>
            <ai>LightGBM, TensorFlow, Scikit-learn, SHAP (Feature Selection), DeepSeek API.</ai>
            <backend>FastAPI, PostgreSQL, Docker.</backend>
            <concepts>Triple Barrier Method, Purged CV, Edge ML, RESTful APIs, Microservices.</concepts>
        </tech_stack>

        <contact>
            <email>utkubugrayil@gmail.com</email>
            <github>utkubugrayilmaz.github.io</github>
        </contact>
    </knowledge_base>

    <response_guidelines>
        <rule>Kullanıcı maaş sorarsa: "Bunu Utku ile doğrudan görüşmeniz gerekir."</rule>
        <rule>Kullanıcı özel hayat/siyaset sorarsa: "Sadece teknik yetkinlikler hakkında bilgi verebilirim."</rule>
        <rule>Cevaplar net, teknik terimleri doğru kullanan ve profesyonel yapıda olsun.</rule>
    </response_guidelines>
</system_instruction>
"""

# Model Ayarları
generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

# Modeli Oluştur (Oturum burada başlamıyor, aşağıda başlayacak)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION,
)

# 4. OTURUM YÖNETİMİ (SESSION STORAGE)
# Basit bir sözlük (Dictionary) kullanıyoruz.
# Key: session_id, Value: ChatSession object
chat_sessions = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str  # ARTIK BU ZORUNLU


@app.post("/chat")
@limiter.limit("5/minute")  # <--- 1. EKLEME: Dakikada 5 istek limiti
async def chat_endpoint(request: Request, chat_req: ChatRequest):  # <--- 2. DEĞİŞİKLİK: Parametreler değişti
    try:
        # Not: Artık veriye 'chat_req' üzerinden ulaşıyoruz, 'request' teknik bir nesne oldu.
        if not chat_req.message:
            raise HTTPException(status_code=400, detail="Mesaj boş olamaz")
        if not chat_req.session_id:
            raise HTTPException(status_code=400, detail="Session ID gerekli")

        # Session ID kontrolü (Burası aynı, sadece değişken adı chat_req oldu)
        if chat_req.session_id not in chat_sessions:
            chat_sessions[chat_req.session_id] = model.start_chat(history=[])

        chat = chat_sessions[chat_req.session_id]

        # Mesaj gönderme (Değişken adı chat_req)
        response = chat.send_message(chat_req.message)
        return {"reply": response.text}

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def read_root():
    return {"status": "Utku AI Asistanı Çalışıyor 🚀 (Session Mode)"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)