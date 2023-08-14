from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(255))
    video_path = db.Column(db.String(255))

    def __init__(self, video_name, video_path):
        self.video_name = video_name
        self.video_path = video_path

    def json(self):
        return {'video_id': self.video_id, 'video_name': self.video_name}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Video.query.all()

    @staticmethod
    def get_by_id(video_id):
        return Video.query.get(video_id)

    @staticmethod
    def delete_by_id(video_id):
        video = Video.query.get(video_id)
        if video:
            video.delete()
            return True
        return False

class Subtitle(db.Model):
    subtitle_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    subtitle_text = db.Column(db.Text)

    def __init__(self, video_id, subtitle_text):
        self.video_id = video_id
        self.subtitle_text = subtitle_text

    def json(self):
        return {'subtitle_id': self.subtitle_id, 'video_id': self.video_id, 'subtitle_text': self.subtitle_text}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_video_id(video_id):
        return Subtitle.query.filter_by(video_id=video_id).all()
