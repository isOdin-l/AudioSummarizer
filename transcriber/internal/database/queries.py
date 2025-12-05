from sqlalchemy.orm import Session
from internal.database.schema import Transcription
import uuid

def create_transcription(db: Session, audio_id: uuid, filename: uuid):
    try:
        with db.begin():
            transcription = Transcription( audio_id = audio_id, s3_filename = filename, status = "pending")
            
            db.add(transcription)
    except:
        raise NameError("error")