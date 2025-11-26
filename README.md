# 📌 TaskMaster – Python Productivity App  
### Modern Task Management Application (Python + Flask)

**Created by: Muzamal Asghar — October 2025**

---

## 🚀 Overview

**TaskMaster** is a modern, responsive, and beautifully designed productivity application built using **Python, Flask, SQLAlchemy, and Flask-Login**.  
It helps users manage tasks, organize daily routines, and boost productivity with a clean UI, smooth animations, and secure backend.

This application includes a **modern landing page**, animations, dark theme UI, authentication system, and a professional page structure with all required sections.

---

## ✨ Key Features

### 🔐 User Authentication
- Register / Login / Logout  
- Secure password hashing  
- Session management via Flask-Login  

### 📝 Task Management
- Create new tasks  
- Update tasks  
- Delete tasks  
- Mark tasks as completed  
- Priorities & categories support  

### 🎨 UI & Frontend
- Fully responsive design  
- Modern dark theme  
- Smooth animations & transitions  
- Professional landing page sections:
  - Hero  
  - About  
  - Docs  
  - Contact  
  - Footer with links  

### ⚙ Backend & Database
- Python + Flask  
- SQLite + SQLAlchemy ORM  
- Clean and modular project structure  

### 📱 Fully Responsive
- Desktop  
- Tablet  
- Mobile  

### 🧹 Zero UI Bugs
- Footer fixed  
- Margins & spacing optimized  
- Consistent styling across all pages  

---

## 🖥️ Tech Stack

|     Area                                 |                Technology                       |
|------------------------------------------|-------------------------------------------------|
| Backend                                  |           Python, Flask                         |
| Database                                 |           SQLite, SQLAlchemy                    |
| Authentication                           |           Flask-Login                           |
| Forms & Validation                       |           Flask-WTF, WTForms                    |
| UI                                       |           HTML5, CSS3, JS, Bootstrap 5          |
| Animations                               |           CSS + JavaScript                      |
| Deployment                               |           Vercel (via wrapper), Render, Railway |

---

## 📁 Project Folder Structure

```

taskmaster/
├── __pycache__
├── instance
├── app.py
├── forms.py
├── models.py
├── config.py
├── .env
├── requirements.txt
│
├── static/
│   ├── css/ 
│   │   └── main.css
│   ├── js/
|   |   ├──sw.js
│   │   └── main.js
│   └── images/
│       └── (icons, logos, backgrounds)
│
├── templates/
│   ├── layout.html
|   ├── task_form.html
|   ├── view_task.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── about.html
│   ├── contact.html
│   ├── docs.html
|   └── components
        └── task_card.html


````

---

## 📸 Screenshots

### 🏠 Landing Page  
(Add your screenshot here after uploading)

```markdown
![TaskMaster Screenshot](static/images/landing.png)
````

---

## ⚙️ Run the Project Locally

```bash
git clone https://github.com/muzamalasgharofficial/TaskMaster-Python-Productivity-App
cd TaskMaster-Python-Productivity-App

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
python app.py
```

Your app will run on:
👉 `http://127.0.0.1:5000/`

---

## 🌐 Deployment Guide

### ❗ Important Note

Flask cannot *directly* run on Vercel because Vercel is frontend-oriented.
However, you **CAN deploy using a Python serverless adapter**, or use a recommended platform:

### ✔ Recommended Deployment Platforms

* Render.com
* Railway.app
* Deta Space
* PythonAnywhere
* Any PaaS with Python support

---

## 🚀 Deploy Flask App on Vercel (Working Method)

### 1️⃣ Install Vercel CLI

```bash
pip install vercel
```

### 2️⃣ Create `vercel.json` (required)

Create a file named **vercel.json** in the root folder:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 3️⃣ Deploy to Vercel

```bash
vercel
```

Your live deployment link will appear in the terminal.

---

## 🔥 GitHub Repository Information

### 📌 Repository Name

```
TaskMaster-Python-Productivity-App
```

### 📌 Repository Description

```
A modern task management application built using Python, Flask, SQLAlchemy, and Flask-Login. Includes user authentication, responsive UI, dark theme, landing page, animations, and complete task CRUD system.
```

---

## 🧑‍💻 GitHub Upload Commands (VS Code → GitHub)

Open VS Code terminal inside project folder, then run:

```bash
git init
git add .
git commit -m "Initial commit - TaskMaster App"
git branch -M main
git remote add origin https://github.com/muzamalasgharofficial/TaskMaster-Python-Productivity-App.git
git push -u origin main
```

Your project is now uploaded to GitHub.

---

# 🌐 Host on Vercel — How You Will See Your Project

Visit:
👉 [https://vercel.com/muzamal-asghars-projects](https://vercel.com/muzamal-asghars-projects)

After deploying using:

```bash
vercel
```

Your project will appear in the dashboard automatically.

---

## 🧑‍💻 Author

**👤 Muzamal Asghar**
Software Engineer | Flutter & React Native Developer | AI/ML Enthusiast
Pakistan

🔗 LinkedIn: [https://www.linkedin.com/in/muzamalasgharofficial](https://www.linkedin.com/in/muzamalasgharofficial)
🔗 GitHub: [https://github.com/muzamalasgharofficial](https://github.com/muzamalasgharofficial)

---

## 📜 License

**MIT License**
Free to use and modify for personal or commercial projects.

---

```

---

### ✅ Your README is 100% ready  
### ✅ Professional  
### ✅ Beautiful formatting  
### ✅ Full details included  
### ✅ Copy-Paste ready for GitHub  

If you'd like, I can also:  
🔥 Add badges  
🔥 Add more screenshots  
🔥 Add GIF preview  
🔥 Add docs pages inside README  
🔥 Add installation video section  

Just tell me — I’m here for you, Muzamal! 🚀
```
