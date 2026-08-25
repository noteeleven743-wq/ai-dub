from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "AI Dub backend is running"
    })

@app.route("/dub", methods=["POST"])
def dub_video():
    if "video" not in request.files:
        return jsonify({
            "error": "No video uploaded"
        }), 400

    video = request.files["video"]
    voice = request.form.get("voice", "Myanmar Female Voice")

    if video.filename == "":
        return jsonify({
            "error": "No video selected"
        }), 400

    return jsonify({
        "success": True,
        "message": "Video received successfully",
        "filename": video.filename,
        "voice": voice
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
