from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from googletrans import Translator
from gtts import gTTS
import os

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
    "ko", "it", "pt", "tr", "nl", "bn", "ta", "ml", "gu", "mr", "pa"
]

# Define frontend file path
FRONTEND_FILE = os.path.join(os.getcwd(), "final.html")

# Serve final.html as the main UI
@app.get("/")
async def serve_frontend():
    if os.path.exists(FRONTEND_FILE):
        return FileResponse(FRONTEND_FILE)
    return JSONResponse(content={"error": "final.html not found"}, status_code=404)

@app.get("/translate")
async def translate(text: str, target_lang: str):
    if not text:
        return JSONResponse(content={"error": "No text provided"}, status_code=400)
    
    if target_lang not in SUPPORTED_LANGUAGES:
        return JSONResponse(content={"error": f"Language '{target_lang}' not supported"}, status_code=400)

    translated_text = translator.translate(text, dest=target_lang).text
    return {"translated_text": translated_text}

@app.get("/speech")
async def text_to_speech(text: str, lang: str):
    if not text:
        return JSONResponse(content={"error": "No text provided"}, status_code=400)

    if lang not in SUPPORTED_LANGUAGES:
        return JSONResponse(content={"error": f"Language '{lang}' not supported"}, status_code=400)

    speech = gTTS(text=text, lang=lang, slow=False)
    filename = "output.mp3"
    speech.save(filename)
    
    return FileResponse(filename, media_type="audio/mpeg", filename="speech.mp3")
