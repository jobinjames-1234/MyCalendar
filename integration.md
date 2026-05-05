# Integration Guide: Frontend & Backend

This document explains how to integrate the React/Vite frontend with the Django backend for both local development and production environments.

---

## 1. Local Integration

### Backend Configuration (Django)
1. **CORS Settings**: The backend uses `django-cors-headers` to allow requests from the frontend.
2. **Environment Variables**: Create a `.env` file in the `backend/` directory:
   ```env
   DJANGO_DEBUG=True
   DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:5173
   ```
3. **Run Server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Configuration (Vite)
1. **Environment Variables**: Create a `.env` file in the `frontend/` directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```
2. **Axios Client**: The frontend uses `axios` with `withCredentials: true` and CSRF header support (configured in `src/api/client.js`).
3. **Run Dev Server**:
   ```bash
   npm run dev
   ```

---

## 2. Production Integration (Vercel + TiDB)

### Frontend (Vercel)
1. **Deployment**: Connect your GitHub repository to Vercel.
2. **Environment Variables**: In the Vercel Dashboard, add:
   - `VITE_API_BASE_URL`: The URL of your deployed Django backend (e.g., `https://api.yourdomain.com`).
3. **Build Command**: `npm run build`.

### Backend (Django)
1. **CORS Production**: Set `DJANGO_CORS_ALLOWED_ORIGINS` in your production environment variables to include your Vercel URL (e.g., `https://your-app.vercel.app`).
2. **Database (TiDB)**:
   - Use TiDB Cloud (Serverless) for a MySQL-compatible database.
   - Update backend environment variables with TiDB credentials:
     ```env
     MYSQL_DATABASE=your_db_name
     MYSQL_USER=your_user.root
     MYSQL_PASSWORD=your_password
     MYSQL_HOST=gateway01.ap-southeast-1.prod.aws.tidbcloud.com
     MYSQL_PORT=4000
     ```
3. **Allowed Hosts**: Ensure `DJANGO_ALLOWED_HOSTS` includes your backend domain.

---

## 3. Communication Flow

1. **Authentication**: The frontend sends login requests to `/api/accounts/login/`.
2. **Session Persistence**: Django sets a session cookie. Axios automatically includes this cookie in subsequent requests because `withCredentials` is set to `true`.
3. **CSRF Protection**: Django provides a `csrftoken` cookie. Axios reads this cookie and sends it back in the `X-CSRFToken` header for state-changing requests (POST, PUT, DELETE).
