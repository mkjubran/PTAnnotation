from flask import Flask, send_from_directory, jsonify, request
import os
import json

app = Flask(__name__, static_folder="build")

ANNOTATION_FILE = "annotations.json"

if not os.path.exists(ANNOTATION_FILE):
    with open(ANNOTATION_FILE, "w") as f:
        json.dump({}, f)

# Serve React frontend
#@app.route("/", defaults={"path": ""})
#@app.route("/<path:path>")
#def serve(path):
#    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
#        return send_from_directory(app.static_folder, path)
#    return send_from_directory(app.static_folder, "index.html")

# API: list exercises
@app.route("/exercises", methods=["GET"])
def list_exercises():
    exercises = [name for name in os.listdir("videos") if os.path.isdir(os.path.join("videos", name))]
    return jsonify(exercises)

# API: list videos for an exercise
@app.route("/videos/<exercise>", methods=["GET"])
def list_videos(exercise):
    path = os.path.join("videos", exercise)
    videos = os.listdir(path) if os.path.exists(path) else []
    return jsonify(videos)

# API: save annotations
@app.route("/annotations", methods=["POST"])
def save_annotation():
    new_data = request.json
    if os.path.exists(ANNOTATION_FILE):
        with open(ANNOTATION_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data.update(new_data)
    with open(ANNOTATION_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "success"})


# Serve React frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)

