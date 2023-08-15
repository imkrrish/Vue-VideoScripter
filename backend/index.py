from flask import Flask, request, jsonify, redirect
from models.models import db, Video, Subtitle
from flask_cors import CORS
import os
import io
import pyrebase
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": ""
}

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

        # Upload video to Firebase Storage
        video_path = f"videos/{video_name}"
        storage.child(video_path).put(file)

        new_video = Video(video_name=video_name, video_path=video_path)
        db.session.add(new_video)
        db.session.commit()
        return jsonify({"video_id": new_video.video_id})

@app.route("/subtitle/<int:video_id>", methods=["GET", "POST"])
def manage_subtitle(video_id):
    if request.method == "POST":
        subtitle_text = request.json.get("subtitle_text")
        if not subtitle_text:
            return "Subtitle text is required", 400

        video = db.session.get(Video, video_id)
        if not video:
            return "Video not found", 404
        subtitle_path = f"subtitles/{video_id}.vtt"
        new_subtitle = Subtitle(video_id=video_id, subtitle_text=subtitle_text, subtitle_path=subtitle_path)
        db.session.add(new_subtitle)
        db.session.commit()

        # Upload subtitle to Firebase Storage
        subtitle_filename = f"{video_id}.vtt"
        subtitle_content = f"WEBVTT\n\n{subtitle_text}"

        subtitle_storage_path = f"subtitles/{subtitle_filename}"

        subtitle_bytes = subtitle_content.encode('utf-8')
        subtitle_io = io.BytesIO(subtitle_bytes)

        storage.child(subtitle_storage_path).put(subtitle_io)

        return "Subtitle added successfully"
    elif request.method == "GET":
        subtitle_filename = f"{video_id}.vtt"
        subtitle_storage_path = f"subtitles/{subtitle_filename}"

        try:
            subtitle_url = storage.child(subtitle_storage_path).get_url(None)
            return redirect(subtitle_url)
        except:
            return "Subtitle file not found", 404


@app.route("/video/<int:video_id>", methods=["GET", "DELETE"])
def stream_video(video_id):
    video = db.session.get(Video, video_id)

    if not video:
        return "Video not found", 404

    video_path = video.video_path
    try:
        download_url = storage.child(video_path).get_url(None)
        return redirect(download_url)
    except:
        return "Video file not found", 404

def manage_video(video_id):
    video = db.session.get(Video, video_id)
    subtitle = db.session.get(Subtitle, video_id)
    if not video:
        return "Video not found", 404

    if request.method == "GET":
        logging.debug(subtitle)
        return stream_video(video_id)

    elif request.method == "DELETE":
        try:
            # Delete subtitle file from storage
            storage.child(subtitle.subtitle_path).delete()
        except Exception as e:
            logging.debug(f"Subtitle deletion error: {e}")
        
        try:
            # Delete video file from storage
            storage.child(video.video_path).delete()
        except Exception as e:
            logging.debug(f"Video deletion error: {e}")

        try:
            # Delete related subtitle records from the database
            db.session.query(Subtitle).filter_by(video_id=video_id).delete()
            # Delete video record from the database
            db.session.delete(video)
            # Commit the changes to the database
            db.session.commit()
            return "Video deleted successfully"
        except Exception as e:
            # Rollback the database changes in case of an error
            db.session.rollback()
            return f"Deletion error: {e}", 500



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
