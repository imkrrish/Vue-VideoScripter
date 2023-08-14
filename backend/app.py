from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


from models.models import db
db.init_app(app)

CORS(app)

from models.models import Video, Subtitle

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def list_videos():
    videos = Video.query.all()
    video_list = [{"id": video.id, "title": video.title} for video in videos]
    return jsonify(video_list)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video part in request", 400
    
    video_file = request.files['video']
    if video_file.filename == '':
        return "No selected file", 400
    
    filename = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(filename)
    
    title = request.form.get('title', 'Untitled Video')
    video = Video(title=title, filename=filename)
    db.session.add(video)
    db.session.commit()
    
    return jsonify({"message": "Video uploaded successfully", "video_id": video.id})

@app.route('/subtitle/<int:video_id>', methods=['POST'])
def add_subtitle(video_id):
    data = request.json
    video = Video.query.get(video_id)
    
    if not video:
        return "Video not found", 404
    
    subtitles = data.get('subtitles', [])
    for subtitle_data in subtitles:
        subtitle = Subtitle(
            video_id=video.id,
            start_timestamp=subtitle_data['start_timestamp'],
            end_timestamp=subtitle_data['end_timestamp'],
            subtitle_text=subtitle_data['subtitle']
        )
        db.session.add(subtitle)
    
    db.session.commit()
    return jsonify({"message": "Subtitles added successfully"})

@app.route('/video/<int:video_id>', methods=['GET', 'DELETE'])
def get_delete_video(video_id):
    video = Video.query.get(video_id)
    
    if not video:
        return "Video not found", 404
    
    if request.method == 'GET':
        subtitles = Subtitle.query.filter_by(video_id=video.id).all()
        
        video_data = {
            "id": video.id,
            "title": video.title,
            "subtitles": [
                {
                    "start_timestamp": subtitle.start_timestamp,
                    "end_timestamp": subtitle.end_timestamp,
                    "subtitle": subtitle.subtitle_text
                }
                for subtitle in subtitles
            ]
        }
        
        return jsonify(video_data)
    
    if request.method == 'DELETE':
        db.session.delete(video)
        db.session.commit()
        return jsonify({"message": "Video deleted successfully"})


@app.route('/video/<int:video_id>/stream', methods=['GET'])
def stream_video(video_id):
    video = Video.query.get(video_id)

    if not video:
        return "Video not found", 404

    return send_file(video.filename, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
