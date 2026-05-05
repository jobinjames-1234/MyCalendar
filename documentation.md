# Project Documentation & Deployment Guide

This document provides a comprehensive guide for deploying and maintaining the Calendar application.

---

## 1. Project Architecture

- **Frontend**: React 18, Vite, Axios, Tailwind CSS (optional/if used), React Router.
- **Backend**: Django 5, Django REST Framework, MySQL (TiDB compatible).
- **Database**: TiDB Cloud (Serverless) - A scalable, MySQL-compatible distributed database.

---

## 2. Database Setup (TiDB)

1. **Create Cluster**: Sign up for [TiDB Cloud](https://tidbcloud.com/) and create a "Serverless" cluster.
2. **Get Credentials**:
   - Go to the cluster dashboard -> **Connect**.
   - Choose **Connect with MySQL Client** or **Standard Connection**.
   - Copy the `Host`, `Port`, `User`, and `Password`.
3. **Configure Django**:
   - Install `mysqlclient` (already in `requirements.txt`).
   - Set the following environment variables in your production environment:
     - `MYSQL_DATABASE`
     - `MYSQL_USER`
     - `MYSQL_PASSWORD`
     - `MYSQL_HOST`
     - `MYSQL_PORT` (usually 4000 for TiDB)

---

## 3. Backend Deployment (Django)

You can deploy the Django backend on platforms like **Railway**, **Render**, or **DigitalOcean App Platform**.

### Steps:
1. **GitHub Repository**: Push your code to a private GitHub repository.
2. **Environment Variables**: Set the following in your deployment platform:
   - `DJANGO_SECRET_KEY`: A long, random string.
   - `DJANGO_DEBUG`: `False`.
   - `DJANGO_ALLOWED_HOSTS`: Your backend domain (e.g., `api.myapp.com`).
   - `DJANGO_CORS_ALLOWED_ORIGINS`: Your Vercel frontend URL.
   - All `MYSQL_*` variables for TiDB.
3. **Database Migrations**: Run migrations during the build or post-deployment phase:
   ```bash
   python manage.py migrate
   ```
4. **Static Files**: Run `collectstatic` to prepare CSS/JS for production:
   ```bash
   python manage.py collectstatic --noinput
   ```

---

## 4. Frontend Deployment (Vercel)

Vercel is the recommended platform for the Vite/React frontend.

### Steps:
1. **New Project**: In Vercel, click "Add New" -> "Project".
2. **Import Repo**: Select your GitHub repository.
3. **Framework Preset**: Vercel should automatically detect **Vite**.
4. **Root Directory**: Select `frontend`.
5. **Environment Variables**:
   - `VITE_API_BASE_URL`: The URL of your deployed Django API.
6. **Deploy**: Click "Deploy".

---

## 5. Security & Best Practices

- **HTTPS**: Both frontend and backend MUST use HTTPS in production.
- **CSRF**: Handled automatically by Django and Axios (ensure `withCredentials` is true).
- **Sensitive Data**: Never commit your `.env` files to Git (they are ignored by `.gitignore`).
- **Allowed Origins**: Be restrictive with `CORS_ALLOWED_ORIGINS`. Only include your actual production domain.
