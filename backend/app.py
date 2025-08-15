from flask import Flask, send_from_directory, jsonify, request
import os
import json
from flask_cors import CORS
from flask import Response, stream_with_context
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, Response
import csv
from datetime import datetime

app = Flask(__name__, static_folder="build")
CORS(app)

ANNOTATION_FILE = "./data/annotations.json"

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-change-me")

if not os.path.exists(ANNOTATION_FILE):
    with open(ANNOTATION_FILE, "w") as f:
        json.dump({}, f)

def get_db():
    conn = sqlite3.connect(os.path.join(app.root_path, "./data/app.db"))
    conn.row_factory = sqlite3.Row
    return conn

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "auth_required"}), 401
        return fn(*args, **kwargs)
    return wrapper

def get_user(username):
    conn = sqlite3.connect(os.path.join(app.root_path, "./data/app.db"))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row

# -----------------
# API routes
# -----------------
@app.route("/api/annotations", methods=["GET"])
def get_annotations():
    with open(ANNOTATION_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/api/annotations", methods=["POST"])
def save_annotation():
    new_data = request.json
    with open(ANNOTATION_FILE, "r") as f:
        data = json.load(f)
    data.update(new_data)
    with open(ANNOTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "success"})

@app.route("/api/exercises", methods=["GET"])
def list_exercises():
    videos_dir = os.path.join(app.root_path, "videos")
    return jsonify([d for d in os.listdir(videos_dir) if os.path.isdir(os.path.join(videos_dir, d))])

#@app.route("/api/videos/<exercise>", methods=["GET"])
#def list_videos(exercise):
#    exercise_dir = os.path.join(app.root_path, "videos", exercise)
#    return jsonify([f for f in os.listdir(exercise_dir) if os.path.isfile(os.path.join(exercise_dir, f))])


@app.route("/api/videos/<exercise>")
@login_required
def get_videos(exercise):
    exercise_dir = os.path.join(app.root_path, "videos", exercise)
    all_videos = [f for f in os.listdir(exercise_dir) if os.path.isfile(os.path.join(exercise_dir, f))]

    user_id = session["user_id"]
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT video FROM label_events
        WHERE user_id = ? AND exercise = ?
    """, (user_id, exercise))
    done_set = {row["video"] for row in cur.fetchall()}
    conn.close()

    return jsonify([
        {"name": v, "done": v in done_set}
        for v in all_videos
    ])

#@app.route("/api/videos/<exercise>/<video>")
#def serve_video(exercise, video):
#    return send_from_directory(
#        os.path.join(app.root_path, "videos", exercise),
#        video,
#        mimetype="video/mp4"
#    )


@app.route("/api/videos/<exercise>/<video>")
def serve_video(exercise, video):
    path = os.path.join(app.root_path, "videos", exercise, video)
    def generate():
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                yield chunk
    return Response(stream_with_context(generate()), mimetype="video/mp4")

@app.route("/api/labels", methods=["GET"])
def get_labels():
    conn = sqlite3.connect("./data/app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, question FROM labels ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to list of dicts
    labels = [{"name": row[0], "question": row[1]} for row in rows]
    return jsonify(labels)


@app.post("/api/register")
def register():
    data = request.json or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if not username or not password:
        return jsonify({"error": "username_and_password_required"}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "username_taken"}), 409
    finally:
        conn.close()

    return jsonify({"status": "ok"})
    
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    row = get_user(username)
    if not row or not check_password_hash(row["password_hash"], password):
        return {"error": "Invalid username or password"}, 401

    session["user_id"] = row["id"]
    return {"username": username}

@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"status": "ok"})

@app.get("/api/me")
def me():
    if "user_id" not in session:
        return jsonify({"authenticated": False})
    return jsonify({
        "authenticated": True,
        "user_id": session["user_id"],
        "username": session["username"],
        "is_admin": session.get("is_admin", 0)
    })

@app.post("/api/label_events")
@login_required
def save_label_events():
    payload = request.json or {}
    exercise = (payload.get("exercise") or "").strip()
    video = (payload.get("video") or "").strip()
    answers = payload.get("answers") or []

    if not exercise or not video or not isinstance(answers, list) or not answers:
        return jsonify({"error": "invalid_payload"}), 400

    user_id = session["user_id"]
    conn = get_db()
    cur = conn.cursor()
    cur.executemany(
        """
        INSERT INTO label_events (user_id, exercise, video, question_name, label_value)
        VALUES (?, ?, ?, ?, ?)
        """,
        [(user_id, exercise, video, a.get("question_name"), int(a.get("label_value", 0))) for a in answers]
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok", "saved": len(answers)})


# -----------------
# Serve React frontend
# -----------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)

