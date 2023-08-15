from flask import Flask, request, jsonify, Response, send_file
from models.models import db, Video, Subtitle
from flask_cors import CORS
import os
import pyrebase
from dotenv import load_dotenv

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})

firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()

@app.route("/", methods=["GET"])
def list_videos():
    videos = Video.get_all()
    videos_json = [video.json() for video in videos]
    return jsonify(videos_json)

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if file:
        video_name = file.filename
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
        file.save(video_path)

        new_video = Video(video_name=video_name, video_path=video_path)
        new_video.insert()
        return jsonify({"video_id": new_video.video_id})

@app.route("/subtitle/<int:video_id>", methods=["POST"])
def add_subtitle(video_id):
    subtitle_text = request.json.get("subtitle_text")
    if not subtitle_text:
        return "Subtitle text is required", 400

    video = Video.get_by_id(video_id)
    if not video:
        return "Video not found", 404

    new_subtitle = Subtitle(video_id=video_id, subtitle_text=subtitle_text)
    new_subtitle.insert()

    # Save the subtitle to a .vtt file
    subtitle_filename = f"{video_id}.vtt"
    subtitle_path = os.path.join(app.config['UPLOAD_FOLDER'], subtitle_filename)
    with open(subtitle_path, "w") as subtitle_file:
        subtitle_file.write("WEBVTT\n\n")
        subtitle_file.write(f"{subtitle_text}")

    return "Subtitle added successfully"

@app.route("/video/<int:video_id>", methods=["GET", "DELETE"])
def manage_video(video_id):
    video = Video.get_by_id(video_id)
    if not video:
        return "Video not found", 404

    if request.method == "GET":
        return send_subtitle_file(video_id)

    elif request.method == "DELETE":
        video_path = video.video_path
        subtitle_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{video_id}.vtt")

        if os.path.exists(subtitle_path):
            os.remove(subtitle_path)

        video.delete()
        os.remove(video_path)
        return "Video deleted successfully"

def send_subtitle_file(video_id):
    subtitle_filename = f"{video_id}.vtt"
    subtitle_path = os.path.join(app.config['UPLOAD_FOLDER'], subtitle_filename)
    
    if os.path.exists(subtitle_path):
        with open(subtitle_path, "r") as subtitle_file:
            subtitle_content = subtitle_file.read()
            response = Response(subtitle_content, content_type='text/vtt')
            response.headers["Content-Disposition"] = f"attachment; filename={subtitle_filename}"
            return response
    else:
        return "Subtitle file not found", 404
    
@app.route('/video/<int:video_id>/stream', methods=['GET'])
def stream_video(video_id):
    video = Video.get_by_id(video_id)

    if not video:
        return "Video not found", 404
    
    video_path = video.video_path.replace("\\", "/")
    if os.path.exists(video_path):
        return send_file(video_path, as_attachment=False)
    else:
        return "Video file not found", 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
