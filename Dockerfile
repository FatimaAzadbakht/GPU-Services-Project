# 1. استفاده از نسخه سبک پایتون
FROM python:3.11-slim

# 2. تعیین پوشه کاری داخل داکر
WORKDIR /app

# 3. کپی کردن فایل نیازمندی‌ها و نصب آن‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. کپی کردن تمام فایل‌های پروژه به داخل داکر
COPY . .

# 5. دستوری که برنامه را اجرا می‌کند
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]