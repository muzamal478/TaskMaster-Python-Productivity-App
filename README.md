TaskMaster - Flask Task Management App
=====================================

Requirements:
  - Python 3.8+
  - pip

Setup (Linux / macOS / Windows)
-------------------------------
1. Create and activate virtualenv (recommended)
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows

2. Install requirements
   pip install -r requirements.txt

3. Run the app
   python app.py

4. Open browser
   http://127.0.0.1:5000/

Notes:
 - The app uses an SQLite DB located at `instance/taskmaster.sqlite` created automatically.
 - To run in production, set environment variables:
   FLASK_ENV=production
   SECRET_KEY='your-prod-secret'
   and use a WSGI server like gunicorn.

Packaging as Desktop App:
 - You can package into a single executable using PyInstaller.
 - For cross-platform desktop with web UI, package a small wrapper that launches the local server and opens a browser window.

Cloud Sync:
 - Use the /api/tasks endpoints (protected by login) to sync tasks with other devices.

If you want, I can:
 - Add email reminders (SMTP) or cron job support.
 - Add an export/import CSV feature.
 - Provide an annotated walkthrough and a ready-to-run zip file.
