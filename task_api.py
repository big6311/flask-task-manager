# task_api.py
import os
import json
from flask import Flask, request, jsonify, render_template
from models import db, Task  # <- now imports db AND Task from models.py

app = Flask(__name__)

# Use SQLite for now
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Attach db to this app
db.init_app(app)

# Create tables when the app starts (locally)
with app.app_context():
    db.create_all()

DATA_FILE = "tasks.json"
tasks = []
next_id = 1  # will be updated after loading tasks

def is_valid_title(title):
    if not title:
        return False
    if "http://" in title or "https://" in title:
        return False
    if len(title.strip()) < 3:
        return False
    return True

def load_tasks():
    """Load tasks from the JSON file if it exists."""
    global tasks, next_id

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []
    else:
        tasks = []

    # Set next_id so it is always bigger than any existing task id
    if tasks:
        max_id = max(task["id"] for task in tasks)
        next_id = max_id + 1
    else:
        next_id = 1


def save_tasks():
    """Save current tasks list to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks."""
    return jsonify(tasks)


@app.route("/add_task", methods=["GET"])
def add_task():
    """Add a new task with a title."""
    global next_id

    title = request.args.get("title")
    if not is_valid_title(title):
      return jsonify({
        "error": "Invalid title. Must be at least 3 characters and not contain URLs."
    }), 400

    task = {
        "id": next_id,
        "title": title,
        "done": False
    }
    tasks.append(task)
    next_id += 1

    save_tasks()  # persist change
    return jsonify(task)


@app.route("/complete_task", methods=["GET"])
def complete_task():
    """Mark a task as done using its id."""
    task_id = request.args.get("id", type=int)

    if task_id is None:
        return jsonify({"error": "id is required, like /complete_task?id=1"}), 400

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks()  # persist change
            return jsonify(task)

    return jsonify({"error": "task not found"}), 404


@app.route("/delete_task", methods=["GET"])
def delete_task():
    """Delete a task using its id."""
    task_id = request.args.get("id", type=int)

    if task_id is None:
        return jsonify({"error": "id is required, like /delete_task?id=1"}), 400

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            save_tasks()  # persist change
            return jsonify({"deleted": deleted_task})

    return jsonify({"error": "task not found"}), 404

@app.route("/")
def home():
    load_tasks()
    return render_template("tasks.html")

if __name__ == "__main__":
    app.run(debug=True)
