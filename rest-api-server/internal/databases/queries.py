from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from .schema import AudioFile, SingleplatformAccount
import uuid

def create_audio_file(db: Session, filename: uuid, interaction_data: str) -> uuid:
    try:
        with db.begin():
            account_id = db.query(SingleplatformAccount).filter(SingleplatformAccount.interaction_data == interaction_data).one().id
 
            audio = AudioFile( source_id = account_id, s3_filename = str(filename), status = "pending")
            
            db.add(audio)
        return audio.id

    except NoResultFound:
        raise ValueError(f"Account with interaction_data={interaction_data} not found")
    finally:
        db.close()
