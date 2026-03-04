from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from model import analyze_audio, generate_spectrogram
from audio_engine import convert_webm_to_wav
from alert_engine import generate_alerts
from database import init_db, log_event

app = Flask(__name__)
CORS(app)

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

init_db()

# ------------------ CONTINUOUS MONITORING ------------------
@app.route("/monitor", methods=["POST"])
def monitor():
    if "audio" not in request.files:
        return jsonify({"error": "No audio"}), 400

    webm_path = os.path.join(TEMP_DIR, "chunk.webm")
    wav_path = os.path.join(TEMP_DIR, "chunk.wav")

    request.files["audio"].save(webm_path)
    convert_webm_to_wav(webm_path, wav_path)

    results = analyze_audio(wav_path)
    spectrogram = generate_spectrogram(wav_path)

    for r in results:
        log_event(r["label"], r["score"])

    alerts = generate_alerts(results)

    return jsonify({
        "results": results[:5],
        "alerts": alerts,
        "spectrogram": spectrogram
    })


# ------------------ UPLOAD & ANALYZE ------------------
@app.route("/upload", methods=["POST"])
def upload():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    wav_path = os.path.join(TEMP_DIR, "upload.wav")
    request.files["audio"].save(wav_path)

    results = analyze_audio(wav_path)
    spectrogram = generate_spectrogram(wav_path)

    for r in results:
        log_event(r["label"], r["score"])

    alerts = generate_alerts(results)

    return jsonify({
        "results": results,
        "alerts": alerts,
        "spectrogram": spectrogram
    })


if __name__ == "__main__":
    app.run(port=8000, debug=True)
