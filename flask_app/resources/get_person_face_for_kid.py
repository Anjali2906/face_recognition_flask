from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_app import Model
from flask_app.app import db
import pdb

class GetPersonFaceForKid(Resource):
    def get(self, kid_id):
        person = db.session.query(Model.Person).filter_by(kid_id=kid_id).first()
        mapped_person_id = person.id
        faces = db.session.query(Model.Face).filter_by(person=person.id).all()
        defaultFace = person.default_face
        mapped_person_face = faces[0].image_path
        mapped_person_images_ids = []
        for face in faces:
            if face.id == defaultFace:
                mapped_person_face = face.image_path
            photoObj = db.session.query(Model.Photo).filter_by(id = face.photo).first()
            mapped_person_images_ids.append(photoObj.ruby_id)

        response = {kid_id: {"mapped_person_id": mapped_person_id, 
                            "mapped_person_face": mapped_person_face, 
                            "mapped_person_images_ids": mapped_person_images_ids}}
        return jsonify({"status": 200, "message": response})

