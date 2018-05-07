from flask_app.app import db
# from flask_app.app import app
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY


import numpy as np

# db = SQLAlchemy(app)
# migrate = Migrate(app, db) 


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True) ## --- Primary Key ---
    ruby_id = db.Column(db.Integer) ## --- id of image from input ---
    image_hash = db.Column(db.String(512), unique=True) ## --- hash of image ---
    image_url = db.Column(db.String(512)) ## --- url of image we get ---
    added_on = db.Column(db.DateTime, default=datetime.now) ## --- Delault upload date (database) ---
    captions = db.Column(db.String(512)) ## --- caption of image from input ---
    group_id = db.Column(db.String(512)) ## --- group/school id of image from input ---


    def __init__(self, image_url, ruby_id, image_hash, captions, group_id):
        self.image_url =  image_url
        self.ruby_id =  ruby_id
        self.image_hash = image_hash
        self.captions = captions
        self.group_id = group_id

    def __repr__(self):
        return '<Photo %r>' % self.id

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128)) ## --- Name of Person ---
    mean_encoding = db.Column(ARRAY(db.Float)) ## --- Mean Encoding of face ---
    group_id = db.Column(db.Integer) ## --- From which group/school ---
    kid_id = db.Column(db.Integer) ## ---  ---
    is_labeled = db.Column(db.Boolean) ## --- is person labeled (0-NO, 1-YES)---

    def __init__(self, mean_encoding, name, group_id=None, kid_id = None, is_labeled=False):
        self.name = name
        self.mean_encoding = mean_encoding
        self.group_id = group_id
        self.kid_id = kid_id
        self.is_labeled = is_labeled

    
    def __repr__(self):
        return '<Person %r>' % self.id

    # change function accorning to need
    def update_average_face_encoding(self, face_encoding):
        myself = self.mean_encoding
        encodings = []
        encodings.append(myself)
        encodings.append(face_encoding)
        mean_encoding = np.array(encodings).mean(axis=0)
        self.mean_encoding = list(mean_encoding)

class Face(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    # face_id = db.Column(db.String(64))
    photo = db.Column(db.ForeignKey('photo.id')) ## --- photo from where this face is taken from (Photo.id) ---
    # face_embedding = db.Column(ARRAY(db.Float))
    encoding = db.Column(ARRAY(db.Float)) ## --- Features of image ---
    person = db.Column(db.Integer, db.ForeignKey('person.id')) ## --- Who's face is this (Person.id) ---
    person_is_labeled = db.Column(db.Boolean) ## --- is face/person known (0 - NO, 1 - YES) ---
    image_path = db.Column(db.String(64)) ## --- Path of face on our server ---

    location_top = db.Column(db.Integer) ## --- Location of face in photo ---
    location_bottom = db.Column(db.Integer) ## --- Location of face in photo ---
    location_left = db.Column(db.Integer) ## --- Location of face in photo ---
    location_right = db.Column(db.Integer) ## --- Location of face in photo ---

    def __init__(self, f_uuid, photo_id, encoding, person, location_top, location_bottom, location_left, location_right, person_is_labeled = False):
        self.id = f_uuid
        self.photo = photo_id
        self.encoding = encoding
        self.person = person
        self.image_path = str(f_uuid) + '.jpg'

        self.location_top = location_top
        self.location_bottom = location_bottom
        self.location_left = location_left
        self.location_right = location_right
        self.person_is_labeled = person_is_labeled

    
    def __repr__(self):
        return '<Face %r>' % self.id

# was cluster


# to do many to many field
class AlbumUser(db.Model):
    album_id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(128)) ## --- Title of Album ---
    timestamp = db.Column(db.DateTime, unique=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    # photos = db.relationship('Photo', ) # many to many