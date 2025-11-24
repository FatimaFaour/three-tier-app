import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME", "three_tier_db"),
        user=os.environ.get("DB_USER", "three_tier_user"),
        password=os.environ.get("DB_PASSWORD", "three_tier_password"),
        host=os.environ.get("DB_HOST", "db"),  # important
        port=os.environ.get("DB_PORT", 5432),
    )
    return conn

@app.route("/message")
def get_message():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM messages LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return jsonify({"message": row[0]})
    else:
        return jsonify({"message": "No message found"}), 404

@app.route("/")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
