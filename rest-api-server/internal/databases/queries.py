from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from .schema import AudioFile, SingleplatformAccount
import uuid

async def create_audio_file(db: Session, filename: uuid, interaction_data: str, source_type: str) -> uuid:
    try:
        with db.begin():
            account = db.query(SingleplatformAccount).filter(SingleplatformAccount.interaction_data == interaction_data).first()
            account_id = uuid.uuid4() if account is None else account.id

            if account is None:
                account = SingleplatformAccount(id = account_id, interaction_data = interaction_data, type = source_type)
                db.add(account)

            audio = AudioFile( source_id = account_id, s3_filename = str(filename), status = "pending")
            
            db.add(audio)
        return audio.id

    except Exception as e:
        raise NameError(f"Error: {e}")
