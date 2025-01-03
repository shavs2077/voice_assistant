import wave
from faster_whisper import WhisperModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5Tokenizer, T5ForConditionalGeneration
import pyaudio
import numpy as np

import whisper

class VideoTranscriber:
    def __init__(self):
        self.whisper = whisper.load_model("medium", device="cpu")
        # self.whisper = WhisperModel("medium", device="cpu", compute_type="float32")
        # self.whisper = WhisperModel("large-v3", device="cpu", compute_type="float16")

    def transcript(self, mp3_route):
        transcript_list = []

        # p = pyaudio.PyAudio()
        # stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

        # frames = []
        # for _ in range(0, int(16000 / 1024 * 1)):
        #     data = stream.read(1024)
        #     frames.append(data)

        # Read audio file at mp3_route as np array of bytes. Then detect language

        # audio = whisper.load_audio(mp3_route)
        # audio = whisper.pad_or_trim(audio)

        # mel = whisper.log_mel_spectrogram(audio, n_mels=self.whisper.dims.n_mels).to(self.whisper.device)

        # _, probs = self.whisper.detect_language(mel)

        # print("Detected language '%s' with probability %f" % (max(probs, key=probs.get), 0))
        print("Transcripting video...")

        # options = whisper.DecodingOptions()
        # result = whisper.decode(self.whisper, mel, options)

        # Encoding with UTF-8
        # transcript_utf8 = result.text.encode('utf-8').decode('utf-8')
        result = self.whisper.transcribe(audio=mp3_route, language="es", verbose=True)

        transcript_utf8 = result.get("text", "")

        if transcript_utf8:
            print("Transcription Done!")
        else:
            print("There was an error")

        return transcript_utf8
