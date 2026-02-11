from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# ایجاد فایل دیتابیس در همان پوشه پروژه
DATABASE_URL = "sqlite:///./gpu_service.db"

# تنظیمات موتور دیتابیس
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # این دستور تمام جداولی که در models تعریف کردیم را واقعا می‌سازد
    Base.metadata.create_all(bind=engine)