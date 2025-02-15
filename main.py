from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from googletrans import Translator

app = FastAPI()

# CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

translator = Translator()

# Supported languages
SUPPORTED_LANGUAGES = [
    "en", "te", "hi", "fr", "es", "de", "zh-CN", "ja", "ru", "ar",
    "ko", "it", "pt", "tr", "nl", "bn"
]

@app.get("/translate")
async def translate(text: str, target_lang: str):
    if not text:
        return {"error": "No text provided"}
    
    if target_lang not in SUPPORTED_LANGUAGES:
        return {"error": f"Language '{target_lang}' not supported"}

    translated_text = translator.translate(text, dest=target_lang).text
    return {"translated_text": translated_text}
