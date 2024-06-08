# backend/Dockerfile

# استفاده از تصویر پایه پایتون
FROM python:3.9-slim

# تنظیم پوشه کاری
WORKDIR /app

# کپی کردن فایل‌های requirements.txt و نصب کتابخانه‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن باقی فایل‌های پروژه
COPY . .

# باز کردن پورت مورد نیاز
EXPOSE 8000

# اجرای سرور جنگو
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
