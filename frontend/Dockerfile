# استفاده از تصویر پایه node
FROM node:20-slim

# تنظیم پوشه کاری
WORKDIR /app

# کپی کردن فایل‌های package.json و نصب کتابخانه‌ها
COPY package*.json ./
COPY svelte.config.js ./
COPY vite.config.js ./
RUN npm install

# کپی کردن باقی فایل‌های پروژه
COPY . .

# باز کردن پورت مورد نیاز
EXPOSE 8080

# اجرای سرور
CMD ["npm", "run", "dev"]
