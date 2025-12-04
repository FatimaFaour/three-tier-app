import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_db_connection():
     conn = psycopg2.connect(
         dbname=os.environ.get("DB_NAME", "three_tier_db"),
         user=os.environ.get("DB_USER", "three_tier_user"),
         password=os.environ.get("DB_PASSWORD", "three_tier_password"),
         host=os.environ.get("DB_HOST", "db"),
         port=os.environ.get("DB_PORT", 5432),
     )
     return conn


@app.route("/")
def health():
    return jsonify({"status": "ok"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    """
    Return all tasks.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, task_text, is_done FROM tasks ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tasks = [
        {"id": r[0], "task_text": r[1], "is_done": r[2]}
        for r in rows
    ]
    return jsonify({"tasks": tasks})

@app.route("/tasks", methods=["POST"])
def add_task():
    """
    Create a new task. Expects JSON: { "task_text": "something" }.
    """
    data = request.get_json(silent=True) or {}
    task_text = data.get("task_text")

    if not task_text or not task_text.strip():
        return jsonify({"error": "task_text is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (task_text) VALUES (%s) RETURNING id, is_done;",
        (task_text.strip(),)
    )
    new_id, is_done = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": new_id,
        "task_text": task_text.strip(),
        "is_done": is_done
    }), 201

@app.route("/tasks/<int:task_id>/toggle", methods=["PUT"])
def toggle_task(task_id):
    """
    Toggle a task's is_done flag (true/false).
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Get current state
    cur.execute("SELECT is_done FROM tasks WHERE id = %s;", (task_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    current = row[0]
    new_value = not current

    cur.execute(
        "UPDATE tasks SET is_done = %s WHERE id = %s;",
        (new_value, task_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": task_id, "is_done": new_value})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Delete a task by id.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", (task_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"status": "deleted", "id": task_id})
    

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)

