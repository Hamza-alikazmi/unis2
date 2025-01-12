from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = "can'tsharewithyou"  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    link = db.Column(db.String(300), nullable=True)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Admin Login Route
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "Invalid credentials", 401
    return render_template('admin_login.html')

# Admin Panel Route
@app.route("/admin/panel")
def admin_panel():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    alltodo = Todo.query.all()
    return render_template('admin_panel.html', alltodo=alltodo)

# Logout Route
@app.route("/admin/logout")
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        try:
            title = request.form['title']
            subject_name = request.form['subject_name']
            course_name = request.form['course_name']
            link = request.form['link']

            todo = Todo(title=title, subject_name=subject_name, course_name=course_name, link=link)
            db.session.add(todo)
            db.session.commit()

            alltodo = Todo.query.all()
            return render_template('index.html', alltodo=alltodo)    
        except Exception as e:
            return str(e), 500
# Route to update a todo
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.subject_name = request.form['subject_name']  # Fixed field reference
        todo.course_name = request.form['course_name']    # Fixed field reference
        db.session.commit()
        return redirect("/admin/panel") if 'admin' in session else redirect("/")
    
    return render_template("update.html", todo=todo)

# Route to delete a todo
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/admin/panel") if 'admin' in session else redirect("/")

# No need for app.run() here for Vercel
