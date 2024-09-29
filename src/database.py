from __future__ import annotations

import uuid
from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UUID, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session, Mapped

import constants

# SQLAlchemy base model
Base = declarative_base()


# Define the Image model
class ImageModel(Base):
    __tablename__ = "images"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: str = Column(String, nullable=False)
    format = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    hash: str = Column(String, nullable=True)  # Add this column to store image hash
    thumbnails: Mapped[list[ThumbnailModel]] = relationship(
        "ThumbnailModel", back_populates="image"
    )


# Define the Thumbnail model
class ThumbnailModel(Base):
    __tablename__ = "thumbnails"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID, ForeignKey("images.id"), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    filename: str = Column(String, nullable=False)
    image: Mapped[ImageModel] = relationship("ImageModel", back_populates="thumbnails")


@lru_cache
def get_engine() -> Engine:
    engine = create_engine(constants.CONNECTION_STRING)
    Base.metadata.create_all(engine)
    return engine


@lru_cache
def get_session_maker() -> sessionmaker[Session]:
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


# Dependency to get DB session
def get_session() -> Generator[Session, None, None]:
    session = get_session_maker()()
    try:
        yield session
    finally:
        session.close()
