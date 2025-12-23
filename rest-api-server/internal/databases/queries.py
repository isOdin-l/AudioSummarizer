from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from .schema import AudioFile, SingleplatformAccount
import uuid

async def create_audio_file(db: Session, filename: uuid, interaction_data: str, source_type: str) -> uuid:
    try:
        with db.begin():
            account = db.query(SingleplatformAccount).filter(SingleplatformAccount.interaction_data == interaction_data).first()
 
            if account is None:
                account = SingleplatformAccount(interaction_data = interaction_data, type = source_type)
                db.add(account)

            audio = AudioFile( source_id = account.id, s3_filename = str(filename), status = "pending")
            
            db.add(audio)
        return audio.id

    except Exception as e:
        raise NameError(f"Error: {e}")
    finally:
        db.close()
