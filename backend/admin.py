from flask import Blueprint, jsonify, request, current_app
from auth import token_required
from models import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime

admin = Blueprint("admin", __name__)

@admin.route("/api/admin/subjects", methods=['POST'])
@token_required(role='admin')
def create_subject(current_user):
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if Subject.query.filter_by(name=name).first():
        return jsonify({"message":"Subject already created"}), 400
    
    db.session.add(Subject(name=name, description=description))
    db.session.commit()
    return jsonify({"message":"Subject created successfully!"}), 201
    
@admin.route("/api/admin/subjects", methods=['GET'])
@token_required(role='admin')
def read_subjects(current_user):
    subjects = Subject.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "description": s.description 
    } for s in subjects])

@admin.route("/api/admin/subjects/<int:id>", methods=['PUT'])
@token_required(role='admin')
def update_subject(current_user, id):
    data = request.json
    Subject.query.get_or_404(id).name = data.name
    Subject.query.get_or_404(id).description = data.description
    db.session.commit()
    return jsonify({"message":"Subject updated successfully!"})

@admin.route("/api/admin/subjects/<int:id>", methods=['DELETE'])
@token_required(role='admin')
def delete_subject(current_user, id):
    db.session.delete(Subject.query.get_or_404(id))
    db.session.commit()
    return jsonify({"message":"Subject deleted successfully!"})