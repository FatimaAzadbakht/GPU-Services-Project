from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class JobStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String) # نقش کاربر: admin یا user
    gpu_hours_quota = Column(Float, default=10.0) # سهمیه ساعت کاربر 

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    command = Column(String) # دستور اجرا
    gpu_type = Column(String) # نوع GPU
    estimated_hours = Column(Float) # تخمین زمان اجرا
    status = Column(Enum(JobStatus), default=JobStatus.PENDING) # وضعیت تسک
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User")