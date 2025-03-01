import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from deep_translator import GoogleTranslator  # ✅ Use deep-translator instead of googletrans
from gtts import gTTS

app = FastAPI()

# ✅ CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount the static directory for serving HTML & audio files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Supported languages
SUPPORTED_LANGUAGES = [
    "en", "te", "hi", "fr", "es", "de", "zh-CN", "ja", "ru", "ar",
    "ko", "it", "pt", "tr", "nl", "bn", "ta", "ml", "gu", "mr", "pa"
]

# ✅ Define frontend file path inside static folder
FRONTEND_FILE = os.path.join(os.path.dirname(__file__), "static", "final.html")

# ✅ Serve `final.html` as the main UI
@app.get("/")
async def serve_frontend():
    if os.path.exists(FRONTEND_FILE):
        return FileResponse(FRONTEND_FILE)
    return JSONResponse(content={"error": "final.html not found"}, status_code=404)

# ✅ Translation API using `deep-translator`
@app.get("/translate")
async def translate(text: str, target_lang: str):
    if not text:
        return JSONResponse(content={"error": "No text provided"}, status_code=400)
    
    if target_lang not in SUPPORTED_LANGUAGES:
        return JSONResponse(content={"error": f"Language '{target_lang}' not supported"}, status_code=400)

    try:
        translated_text = GoogleTranslator(source="auto", target=target_lang).translate(text)
        return {"translated_text": translated_text}
    except Exception as e:
        return JSONResponse(content={"error": f"Translation failed: {str(e)}"}, status_code=500)

# ✅ Text-to-Speech API using `gTTS`
@app.get("/speech")
async def text_to_speech(text: str, lang: str):
    if not text:
        return JSONResponse(content={"error": "No text provided"}, status_code=400)

    if lang not in SUPPORTED_LANGUAGES:
        return JSONResponse(content={"error": f"Language '{lang}' not supported"}, status_code=400)

    try:
        filename = os.path.join("static", "output.mp3")
        speech = gTTS(text=text, lang=lang, slow=False)
        speech.save(filename)
        return FileResponse(filename, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        return JSONResponse(content={"error": f"Speech synthesis failed: {str(e)}"}, status_code=500)
