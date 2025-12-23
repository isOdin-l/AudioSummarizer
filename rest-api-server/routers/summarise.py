from fastapi import APIRouter, Form, File, UploadFile, Depends
from sqlalchemy.orm import Session
from internal.databases.queries import create_audio_file
from internal.databases.postgres.connection import get_db
from pydantic import BaseModel
from .router import baseRouter
from typing import Any, Dict
from internal.s3.s3_client import s3_client
from internal.kafka.kafka import kafka_client
import io
import uuid

class InputDTO(BaseModel):
    source_type: str = Form(...)
    interaction_data: str = Form(...)
    metadata: Dict[str, Any]

summariseRouter = APIRouter()
summariseRouter.include_router(baseRouter)

@summariseRouter.post("/api/v0/audio_summarise")
async def handle_summarization(source_type: str = Form(...), interaction_data: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_bytes = await file.read()
    file_data = io.BytesIO(file_bytes)
    filename = uuid.uuid4()

    audio_id = await create_audio_file(db, filename, interaction_data, source_type)

    await s3_client.upload_file(file_data = file_data, file_length=len(file_bytes), object_name=filename, content_type=file.content_type)

    await kafka_client.start_producer()
    await kafka_client.send(message={"audio_id": str(audio_id), "s3_filename": str(filename), "interaction_data": interaction_data})
    await kafka_client.stop_producer()

    return {"status":"ok", "audio_id": audio_id}