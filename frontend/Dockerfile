# frontend/Dockerfile

# استفاده از تصویر پایه node
FROM node:14

# تنظیم پوشه کاری
WORKDIR /app

# کپی کردن فایل‌های package.json و نصب کتابخانه‌ها
COPY package.json package-lock.json ./
RUN npm install

# کپی کردن باقی فایل‌های پروژه
COPY . .

# ساخت پروژه برای تولید
RUN npm run build

# باز کردن پورت مورد نیاز
EXPOSE 5000

# اجرای سرور
CMD ["npm", "run", "dev"]
