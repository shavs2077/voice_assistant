from faster_whisper import WhisperModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5Tokenizer, T5ForConditionalGeneration

class VideoTranscriber:
    def __init__(self):
        self.whisper = WhisperModel("small", device="cpu", compute_type="float32")

    def transcript(self, mp3_route):
        transcript_list = []

        segments, info = self.whisper.transcribe(mp3_route, beam_size=5)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        print("Transcripting video...")

        for segment in segments:
            transcript_list.append(segment.text)

        transcript_text = "".join(transcript_list)

        # Encoding with UTF-8
        transcript_utf8 = transcript_text.encode('utf-8').decode('utf-8')

        if transcript_utf8:
            print("Transcription Done!")
        else:
            print("There was an error")

        return transcript_utf8
