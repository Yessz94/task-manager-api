from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    tasks = load_tasks()
    data = request.json
    
    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)

    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            return jsonify(task)

    return {"error": "Task not found"}, 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]

    save_tasks(tasks)

    return {"message": "Task deleted"}

if __name__ == "__main__":
    app.run(debug=True)
