from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ADMIN, TEACHER, STUDENT, PARENT
    full_name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    attendance = relationship("Attendance", back_populates="student")
    marks = relationship("Mark", back_populates="student")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, nullable=False)  # PRESENT, ABSENT, LATE

    student = relationship("User", back_populates="attendance")

class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, default=100.0)

    student = relationship("User", back_populates="marks")