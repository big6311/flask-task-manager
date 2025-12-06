from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "tasks.json"
tasks = []
next_id = 1


def load_tasks():
    global tasks, next_id

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []
    else:
        tasks = []

    if tasks:
        next_id = max(task["id"] for task in tasks) + 1
    else:
        next_id = 1


def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/add_task", methods=["GET"])
def add_task():
    global next_id

    title = request.args.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(task)
    next_id += 1
    save_tasks()

    return jsonify(task)


@app.route("/complete_task", methods=["GET"])
def complete_task():
    task_id = request.args.get("id", type=int)

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks()
            return jsonify(task)

    return jsonify({"error": "task not found"}), 404


@app.route("/delete_task", methods=["GET"])
def delete_task():
    task_id = request.args.get("id", type=int)

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted = tasks.pop(i)
            save_tasks()
            return jsonify(deleted)

    return jsonify({"error": "task not found"}), 404


if __name__ == "__main__":
    load_tasks()
    app.run(debug=True)
