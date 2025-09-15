import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from deep_translator import GoogleTranslator
from gtts import gTTS
import uvicorn

app = FastAPI()

# ✅ CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For localhost development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create static directory if it doesn't exist
static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# ✅ Mount the static directory for serving HTML & audio files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ All supported languages from GoogleTranslator
SUPPORTED_LANGUAGES = [
    'af', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bm', 'eu', 'be', 'bn', 
    'bho', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-CN', 'zh-TW', 'co', 'hr', 'cs', 
    'da', 'dv', 'doi', 'nl', 'en', 'eo', 'et', 'ee', 'tl', 'fi', 'fr', 'fy', 
    'gl', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 
    'hu', 'is', 'ig', 'ilo', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 
    'rw', 'gom', 'ko', 'kri', 'ku', 'ckb', 'ky', 'lo', 'la', 'lv', 'ln', 'lt', 
    'lg', 'lb', 'mk', 'mai', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mni-Mtei', 
    'lus', 'mn', 'my', 'ne', 'no', 'or', 'om', 'ps', 'fa', 'pl', 'pt', 'pa', 
    'qu', 'ro', 'ru', 'sm', 'sa', 'gd', 'nso', 'sr', 'st', 'sn', 'sd', 'si', 
    'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 
    'ti', 'ts', 'tr', 'tk', 'ak', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 
    'yi', 'yo', 'zu'
]

# ✅ Define frontend file path inside static folder
FRONTEND_FILE = os.path.join(os.path.dirname(__file__), "static", "final.html")

# ✅ Serve `final.html` as the main UI
@app.get("/")
async def serve_frontend():
    if os.path.exists(FRONTEND_FILE):
        return FileResponse(FRONTEND_FILE)
    return JSONResponse(content={"error": "final.html not found in static folder"}, status_code=404)

# ✅ Translation API using `deep-translator`
@app.get("/translate")
async def translate(text: str, target_lang: str):
    if not text:
        return JSONResponse(content={"error": "No text provided"}, status_code=400)
    
    if target_lang not in SUPPORTED_LANGUAGES:
        return JSONResponse(content={"error": f"Language '{target_lang}' not supported"}, status_code=400)

    try:
        print(f"Translating '{text}' to language: {target_lang}")
        translated_text = GoogleTranslator(source="auto", target=target_lang).translate(text)
        print(f"Translation result: {translated_text}")
        
        return {"translated_text": translated_text}
    except Exception as e:
        print(f"Translation error: {str(e)}")
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

# ✅ Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
