from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database
import auth
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.Base.metadata.create_all(bind=database.engine)
    print("--- جداول دیتابیس ساخته شدند ---")
    yield

app = FastAPI(title="GPU as a Service", lifespan=lifespan)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "فعال"}

@app.post("/register")
def register(username: str, password: str, role: str = "user", db: Session = Depends(get_db)):
    # چک کردن تکراری نبودن
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="این کاربر قبلاً ثبت شده")
    
    # هش کردن رمز
    hashed_pwd = auth.get_password_hash(password)
    
    # ساخت کاربر با تمام فیلدها
    new_user = models.User(
        username=username, 
        password_hash=hashed_pwd, 
        role=role,
        gpu_hours_quota=10.0
    )
    db.add(new_user)
    db.commit()
    return {"message": "کاربر با موفقیت ساخته شد"}

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # پیدا کردن کاربر
    user = db.query(models.User).filter(models.User.username == username).first()
    
    # بررسی رمز عبور (با همان متدی که در auth ساختیم)
    if not user or not auth.verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="نام کاربری یا رمز عبور اشتباه است")
    
    # ساخت توکن JWT
    access_token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role
    }

# بخش ثبت تسک جدید (مخصوص کاربر)
@app.post("/jobs")
def create_job(command: str, gpu_type: str, hours: float, username: str, db: Session = Depends(get_db)):
    # 1. پیدا کردن کاربر
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")
    
    # 2. چک کردن سهمیه GPU (بخش نمره‌آور)
    if user.gpu_hours_quota < hours:
        raise HTTPException(status_code=400, detail="سهمیه GPU شما کافی نیست")
    
    # 3. کسر سهمیه و ثبت تسک
    user.gpu_hours_quota -= hours
    new_job = models.Job(command=command, gpu_type=gpu_type, estimated_hours=hours, user_id=user.id)
    
    db.add(new_job)
    db.commit()
    return {"message": "تسک با موفقیت ثبت شد", "remaining_quota": user.gpu_hours_quota}

# بخش مشاهده تسک‌ها
@app.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()


# قابلیت تغییر وضعیت تسک (فقط برای ادمین)
@app.patch("/jobs/{job_id}")
def update_job_status(job_id: int, status: str, admin_username: str, db: Session = Depends(get_db)):
    # 1. بررسی اینکه آیا درخواست‌دهنده ادمین است؟
    admin = db.query(models.User).filter(models.User.username == admin_username).first()
    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="فقط ادمین اجازه تغییر وضعیت دارد")
    
    # 2. پیدا کردن تسک
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="تسک مورد نظر پیدا نشد")
    
    # 3. تغییر وضعیت (مثلاً از PENDING به APPROVED یا RUNNING)
    job.status = status
    db.commit()
    return {"message": f"وضعیت تسک به {status} تغییر یافت"}