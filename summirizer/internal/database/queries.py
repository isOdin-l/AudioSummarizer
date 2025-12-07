from sqlalchemy.orm import Session
from internal.database.schema import Summary
import uuid

def craete_summary(db: Session, audio_id: uuid, filename: uuid):
    try:
        with db.begin():
            summary = Summary( audio_id = audio_id, s3_filename = filename, status = "pending")
            
            db.add(summary)
    except:
        raise NameError("error")