from flask import request, jsonify
from flask_restful import Resource, reqparse
# from flask_app.Model import Face, Person, Photo
from flask_app import Model
from flask_app.app import db, app
import pdb

# Untag Person Manually (Arguments:- person_id, photo_id as post request)
class ManualUntagKid(Resource):
    def post(self):
        # parse = reqparse.RequestParser()
        # parse.add_argument('photo_id', type = str) # argument for photo id
        # parse.add_argument('person_id', type = str) # argument for person id
        # args = parse.parse_args()
        data = dict(request.get_json(force=True))
        if len(data) > 1:
        # if data['photo_id'] != "" and data['person_id'] != "":
            ruby_id = int(data['ruby_photo_id'])
            kid_id = int(data['kid_id'])
            photoObj = db.session.query(Model.Photo).filter_by(ruby_id=ruby_id).first()
            photo_id = photoObj.id
            personObj = db.session.query(Model.Person).filter_by(kid_id=kid_id).first()
            person_id = personObj.id
            faces = db.session.query(Model.Face).filter_by(photo=photo_id, person=person_id).all() # Getting all faces with given photo id
            for face in faces:
                # if face.person == person_id:
                face.person = None # Removing person from photo when person == given person
                db.session.commit()
                return jsonify({ 'status': 200, 'message': 'Person with person id '+ str(person_id) + " is removed from photo" })
            
            return jsonify({ 'status': 404, 'message': 'Person with person id '+ str(person_id) + " not found in photo" })
        else:
            return jsonify({'status': 406, 'message': 'Please provide both photo id and person id'})