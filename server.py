from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import requests

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/dub", methods=["POST"])
def dub_video():

    if not ELEVENLABS_API_KEY:
        return jsonify({
            "success": False,
            "error": "ELEVENLABS_API_KEY is not configured"
        }), 500

    if "video" not in request.files:
        return jsonify({
            "success": False,
            "error": "No video uploaded"
        }), 400

    video = request.files["video"]

    if video.filename == "":
        return jsonify({
            "success": False,
            "error": "No video selected"
        }), 400

    voice = request.form.get(
        "voice",
        "Myanmar Female Voice"
    )

    filename = (
        str(uuid.uuid4())
        + "_"
        + video.filename
    )

    video_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    video.save(video_path)

    try:

        with open(video_path, "rb") as video_file:

            files = {
                "file": (
                    filename,
                    video_file,
                    video.mimetype or "video/mp4"
                )
            }

            data = {
                "reference": "AI Dub Project",
                "target_language": "my",
                "model_id": "dubbing_v2"
            }

            headers = {
                "xi-api-key": ELEVENLABS_API_KEY
            }

            response = requests.post(
                "https://api.elevenlabs.io/v1/dubbing/project",
                headers=headers,
                data=data,
                files=files,
                timeout=120
            )

        if response.status_code not in [200, 201]:
            return jsonify({
                "success": False,
                "error": response.text
            }), 500

        result = response.json()

        project_id = result.get("project_id")

        return jsonify({
            "success": True,
            "message": "AI dubbing started successfully!",
            "project_id": project_id,
            "voice": voice
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.route("/dub-status/<project_id>")
def dub_status(project_id):

    if not ELEVENLABS_API_KEY:
        return jsonify({
            "success": False,
            "error": "ELEVENLABS_API_KEY is not configured"
        }), 500

    try:

        headers = {
            "xi-api-key": ELEVENLABS_API_KEY
        }

        response = requests.get(
            f"https://api.elevenlabs.io/v1/dubbing/project/{project_id}",
            headers=headers,
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                "success": False,
                "error": response.text
            }), 500

        result = response.json()

        return jsonify({
            "success": True,
            "project_id": project_id,
            "status": result.get("status"),
            "data": result
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
