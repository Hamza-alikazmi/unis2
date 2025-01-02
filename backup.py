from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

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

# Route for handling the home page and form submissions
@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        desc = request.form['desc']

        # Create a new Todo entry
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    # Fetch all todos
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

# Route to update a todo
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        # Update the todo with form data
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect("/admin/panel") if 'admin' in session else redirect("/")
    
    # Render the update page with the todo details
    return render_template("update.html", todo=todo)

# Route to delete a todo
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/admin/panel") if 'admin' in session else redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5050)
