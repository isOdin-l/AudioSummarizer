from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    JSON,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class MultiplatformAccount(Base):
    __tablename__ = "multiplatform_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(128), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    # Relations
    singleplatform = relationship("SingleplatformAccount", back_populates="user", cascade="all, delete")
    audio_files = relationship("AudioFile", back_populates="user")


class SingleplatformAccount(Base):
    __tablename__ = "singleplatform_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("multiplatform_accounts.id", ondelete="SET NULL"), nullable=True)
    interaction_data = Column(Text, unique=True, nullable=False)
    type = Column(String(32), nullable=False)
    meta_data = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    # Relations
    user = relationship("MultiplatformAccount", back_populates="singleplatform")
    audio_files = relationship("AudioFile", back_populates="source")


class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("multiplatform_accounts.id", ondelete="CASCADE"))
    source_id = Column(UUID(as_uuid=True), ForeignKey("singleplatform_accounts.id", ondelete="CASCADE"))
    s3_filename = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    # Relations
    user = relationship("MultiplatformAccount", back_populates="audio_files")
    source = relationship("SingleplatformAccount", back_populates="audio_files")

    transcriptions = relationship("Transcription", back_populates="audio_file", cascade="all, delete")
    summaries = relationship("Summary", back_populates="audio_file", cascade="all, delete")


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio_id = Column(UUID(as_uuid=True), ForeignKey("audio_files.id", ondelete="CASCADE"))
    s3_filename = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    # Relation
    audio_file = relationship("AudioFile", back_populates="transcriptions")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio_id = Column(UUID(as_uuid=True), ForeignKey("audio_files.id", ondelete="CASCADE"))
    s3_filename = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    # Relation
    audio_file = relationship("AudioFile", back_populates="summaries")
