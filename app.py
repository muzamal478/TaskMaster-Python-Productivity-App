import os
import json
from flask import current_app
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from config import Config
from models import db, User, Task
from forms import RegisterForm, LoginForm, TaskForm
from dateutil import parser as date_parser

app = Flask(__name__)
app.config.from_object(Config)

# initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ensure instance folder exists
os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
    # contact page accessible to anonymous users
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not (name and email and message):
            flash("Please fill all fields.", "warning")
            return redirect(url_for("contact"))

        # save message to instance/contact_messages.json
        os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
        file_path = os.path.join(app.root_path, "instance", "contact_messages.json")
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
            else:
                data = []
        except Exception:
            data = []

        entry = {"name": name, "email": email, "message": message, "timestamp": datetime.utcnow().isoformat()}
        data.append(entry)
        with open(file_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

        flash("Message sent. Thank you — we will contact you soon.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already registered", "danger")
            return render_template("register.html", form=form)
        user = User(email=form.email.data.lower(), name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("index"))

# Dashboard & Task list
@app.route("/dashboard")
@login_required
def dashboard():
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "", type=str)
    category = request.args.get("category", None, type=str)
    status = request.args.get("status", None, type=str)  # completed, pending
    sort = request.args.get("sort", "priority", type=str)

    tasks_query = Task.query.filter_by(user_id=current_user.id)

    if q:
        tasks_query = tasks_query.filter(Task.title.ilike(f"%{q}%") | Task.description.ilike(f"%{q}%"))
    if category:
        tasks_query = tasks_query.filter_by(category=category)
    if status == "completed":
        tasks_query = tasks_query.filter_by(completed=True)
    elif status == "pending":
        tasks_query = tasks_query.filter_by(completed=False)

    if sort == "due":
        tasks_query = tasks_query.order_by(Task.due_date.asc().nullslast())
    else:
        # priority ordering: Urgent, High, Medium, Low (map to ordering)
        priority_order = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}
        tasks = tasks_query.all()
        tasks = sorted(tasks, key=lambda t: (priority_order.get(t.priority, 3), t.due_date or datetime.max))
        # handle pagination manually
        per_page = app.config.get("PER_PAGE", 8)
        start = (page-1)*per_page; end = start + per_page
        paginated = tasks[start:end]
        total = len(tasks)
        return render_template("dashboard.html", tasks=paginated, page=page, per_page=per_page, total=total, q=q, category=category, status=status, sort=sort)

    paginated = tasks_query.paginate(page=page, per_page=app.config.get("PER_PAGE", 8))
    return render_template("dashboard.html", tasks=paginated.items, page=page, per_page=app.config.get("PER_PAGE", 8), total=paginated.total, q=q, category=category, status=status, sort=sort)

@app.route("/task/new", methods=["GET","POST"])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        due = None
        if form.due_date.data:
            try:
                due = date_parser.parse(form.due_date.data)
            except Exception:
                flash("Invalid due date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM", "warning")
                return render_template("task_form.html", form=form, title="New Task")
        t = Task(title=form.title.data, description=form.description.data, category=form.category.data or "General",
                 priority=form.priority.data, due_date=due, reminder=form.reminder.data, owner=current_user)
        db.session.add(t)
        db.session.commit()
        flash("Task created.", "success")
        return redirect(url_for("dashboard"))
    return render_template("task_form.html", form=form, title="New Task")

@app.route("/task/<int:task_id>/edit", methods=["GET","POST"])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    if request.method == "POST" and form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.category = form.category.data or "General"
        task.priority = form.priority.data
        task.reminder = form.reminder.data
        if form.due_date.data:
            try:
                task.due_date = date_parser.parse(form.due_date.data)
            except Exception:
                flash("Invalid due date format.", "warning")
                return render_template("task_form.html", form=form, title="Edit Task")
        else:
            task.due_date = None
        db.session.commit()
        flash("Task updated.", "success")
        return redirect(url_for("dashboard"))
    # prefill date string if exists
    if task.due_date:
        form.due_date.data = task.due_date.strftime("%Y-%m-%d %H:%M")
    return render_template("task_form.html", form=form, title="Edit Task")

@app.route("/task/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("dashboard"))

@app.route("/task/<int:task_id>/toggle_complete", methods=["POST"])
@login_required
def toggle_complete(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/task/<int:task_id>")
@login_required
def view_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    return render_template("view_task.html", task=task)

# REST API endpoints for cloud sync (simple)
@app.route("/api/tasks", methods=["GET","POST"])
@login_required
def api_tasks():
    if request.method == "GET":
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return jsonify([t.as_dict() for t in tasks])
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return jsonify({"error":"title required"}), 400
    due = None
    if data.get("due_date"):
        try:
            due = date_parser.parse(data.get("due_date"))
        except Exception:
            pass
    t = Task(title=title, description=data.get("description"), category=data.get("category") or "General",
             priority=data.get("priority") or "Medium", due_date=due, reminder=bool(data.get("reminder")),
             owner=current_user)
    db.session.add(t); db.session.commit()
    return jsonify(t.as_dict()), 201

# API single task
@app.route("/api/tasks/<int:task_id>", methods=["GET","PUT","DELETE"])
@login_required
def api_task_detail(task_id):
    t = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    if request.method == "GET":
        return jsonify(t.as_dict())
    if request.method == "DELETE":
        db.session.delete(t); db.session.commit()
        return jsonify({"ok":True})
    # PUT update
    data = request.get_json() or {}
    t.title = data.get("title", t.title)
    t.description = data.get("description", t.description)
    t.category = data.get("category", t.category)
    t.priority = data.get("priority", t.priority)
    if data.get("due_date"):
        try:
            t.due_date = date_parser.parse(data.get("due_date"))
        except Exception:
            pass
    t.reminder = bool(data.get("reminder", t.reminder))
    t.completed = bool(data.get("completed", t.completed))
    db.session.commit()
    return jsonify(t.as_dict())

# Service worker file route
@app.route("/sw.js")
def sw():
    return send_from_directory("static/js", "sw.js")

if __name__ == "__main__":
    app.run(debug=True)
