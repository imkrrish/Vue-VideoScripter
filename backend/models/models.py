from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    subtitles = db.relationship('Subtitle', backref='video', lazy=True)

class Subtitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    start_timestamp = db.Column(db.String(10), nullable=False)
    end_timestamp = db.Column(db.String(10), nullable=False)
    subtitle_text = db.Column(db.Text, nullable=False)
