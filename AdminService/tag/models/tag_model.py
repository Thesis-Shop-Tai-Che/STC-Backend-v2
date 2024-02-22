from sqlalchemy import (TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, Enum, DateTime,
                        String, text, event)
from sqlalchemy.orm import relationship, Session
from enum import Enum as PythonEnum
from database import Base, get_db
import datetime

class Tag(Base):
    __tablename__ = "Tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name
