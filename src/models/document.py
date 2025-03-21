from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    doc_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String)
    file_hash = Column(String, unique=True)
    filesize = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    onedrive_path = Column(String)
    source = Column(String)
