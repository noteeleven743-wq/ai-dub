from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/dub", methods=["POST"])
def dub_video():

    if "video" not in request.files:
        return jsonify({
            "success": False,
            "error": "No video uploaded"
        }), 400

    video = request.files["video"]

    voice = request.form.get(
        "voice",
        "Myanmar Female Voice"
    )

    if video.filename == "":
        return jsonify({
            "success": False,
            "error": "No video selected"
        }), 400


    unique_name = (
        str(uuid.uuid4())
        + "_"
        + video.filename
    )

    video_path = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )

    video.save(video_path)


    return jsonify({
        "success": True,
        "message": "Video uploaded successfully. AI dubbing will start.",
        "filename": unique_name,
        "voice": voice
    })


if __name__ == "__main__":
    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
