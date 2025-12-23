from sqlalchemy.orm import Session
from internal.database.schema import Transcription
import uuid

async def create_transcription(db: Session, audio_id: str, filename: uuid):
    try:
        with db.begin():
            transcription = Transcription( audio_id = audio_id, s3_filename = str(filename), status = "pending")
            
            db.add(transcription)
    except Exception as e:
        print(f"Ошибка: {e}")