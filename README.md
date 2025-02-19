# 🛒 E-Commerce Backend (Django)

This is the **backend API** for the e-commerce platform, built using **Django** and **Django REST Framework (DRF)**. It provides endpoints for managing products, categories, orders, customers, and shipping information.

After you have successfully run the backend, you should be able to:
- ✅ Access all the API endpoints at [http://127.0.0.1:8000](http://127.0.0.1:8000)
- ✅ Access the frontend at [https://product-zm.vercel.app](https://product-zm.vercel.app)
## 🚀 Important Notice: Run Backend Before Frontend
The [**React frontend**](https://product-zm.vercel.app) **will not function properly** without the backend running.  
Before starting the frontend, make sure the **Django server** is up and running.

---

## 📌 1️⃣ Requirements

Ensure you have the following installed:

- **Python** (≥ 3.8)  
- **Django** (≥ 4.0)  
- **Django REST Framework** (DRF)  
- **django-cors-headers** (for CORS handling)  
- **PostgreSQL** (or SQLite for local development)  

## 📌 2️⃣ Development Setup:
```bash
pip install virtualenv
```
```bash
virtualenv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
python manage.py migrate
```
```bash
python manage.py collectstatic --no-input
```
```bash
python manage.py createsuperuser
```
```bash
python manage.py runserver 0.0.0.0:8000
```

## 📌 3️⃣ Load Fixture Data(Optional):
```bash
python manage.py loaddata categories.json
python manage.py loaddata products.json
python manage.py loaddata product_images.json
```

## 📌 System Architecture
The project system design & client side workflows are located on google drive: 👇
https://drive.google.com/file/d/1G5T5IuQ8VuzOcyHNc-k2fZqzBz5JnIkH/view?usp=drive_link