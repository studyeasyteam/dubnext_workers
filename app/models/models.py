from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Sample(Base):
    __tablename__ = "Sample"

    document_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, index=True, unique=True)
    document_name = Column(String, nullable=False)
