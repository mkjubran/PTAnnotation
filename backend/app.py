from flask import Flask, send_from_directory, jsonify, request
import os
import json
from flask_cors import CORS
from flask import Response, stream_with_context
import sqlite3

app = Flask(__name__, static_folder="build")
CORS(app)

ANNOTATION_FILE = "annotations.json"

if not os.path.exists(ANNOTATION_FILE):
    with open(ANNOTATION_FILE, "w") as f:
        json.dump({}, f)

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

@app.route("/api/videos/<exercise>", methods=["GET"])
def list_videos(exercise):
    exercise_dir = os.path.join(app.root_path, "videos", exercise)
    return jsonify([f for f in os.listdir(exercise_dir) if os.path.isfile(os.path.join(exercise_dir, f))])

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
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, question FROM labels ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to list of dicts
    labels = [{"name": row[0], "question": row[1]} for row in rows]
    return jsonify(labels)

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

