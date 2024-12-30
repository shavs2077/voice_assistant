import os
from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from utils.VideoTranscriber import VideoTranscriber

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "mesage": "Hello World",
    }


@app.post("/transcribe_audio")
async def transcribe_audio(
    audio_file: UploadFile = Form(...),
):
    data = await audio_file.read()
    save_to_dir = "./../tmp/"
    audio_path = save_to_dir + "/" + audio_file.filename
    transcription_path = save_to_dir + "/" + "transcription.txt"

    with open(audio_path, "wb") as audio_file:
        audio_file.write(data)

    audio_file.close()

    transcriber = VideoTranscriber()

    transcript = transcriber.transcript(audio_path)

    with open(transcription_path, "wb") as transcription_file:
        transcription_file.write(transcript.encode("utf-8"))

    transcription_file.close()
    os.remove(audio_path)

    # Here you can add code to handle the audio file, e.g., save it, process it, etc.
    return {
        "message": "Audio transcription received",
    }

