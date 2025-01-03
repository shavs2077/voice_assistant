import os
from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import ollama

from utils.VideoTranscriber import VideoTranscriber

app = FastAPI()

with open("./Modelfile", "r") as f:
    ollama.create("Elenna", modelfile=f.read())
    f.close()

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


def write_to_file(path: str, data_str: str):
    with open(path, "wb") as transcription_file:
        transcription_file.write(data_str.encode("utf-8"))

        transcription_file.close()

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

    os.remove(audio_path)

    # Here you can add code to handle the audio file, e.g., save it, process it, etc.
    return {
        "transcription": transcript,
    }

@app.post("/ask_question")
async def ask_question(
    question: str = Form(...),
):
    response = ollama.chat("Elenna", [
        {
            "role": "user",
            "content": question
        }
    ])
    return {
        "response": response['message']['content'],
    }
