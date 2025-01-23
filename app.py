from flask import Flask, request, jsonify
import speech_recognition as sr
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/convert", methods=["POST"])
def convert_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    filename = secure_filename(audio_file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    audio_file.save(filepath)

    recognizer = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({"text": text})
        except sr.UnknownValueError:
            return jsonify({"text": "Could not understand the audio"})
        except sr.RequestError as e:
            return jsonify({"text": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
