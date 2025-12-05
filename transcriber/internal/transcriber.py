from faster_whisper import WhisperModel
import io

def transcribe(audio_data) -> str:
    audio_stream = io.BytesIO(audio_data)
    audio_stream.seek(0) 

    # Транскрибация
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_stream)

    # получаем весь текст из сегментов
    text = ""
    for segment in segments:
        text += segment.text
    return text

