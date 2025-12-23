from faster_whisper import WhisperModel
import io

class TranscribeModel():
    def __init__(self):
        self.model = WhisperModel(model_size_or_path="/app/model", device="cpu", compute_type="int8", local_files_only=True)

    async def transcribe(self, audio_data: bytes) -> str:
        audio_stream = io.BytesIO(audio_data)
        audio_stream.seek(0) 

        # Транскрибация
        segments, _ = self.model.transcribe(audio_stream)
        # получаем весь текст из сегментов
        text = ""
        for segment in segments:
            text += segment.text
        return text

transcriber = TranscribeModel()