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
    Subject.query.get_or_404(id).name = data.get("name")
    Subject.query.get_or_404(id).description = data.get("description")
    db.session.commit()
    return jsonify({"message":"Subject updated successfully!"})

@admin.route("/api/admin/subjects/<int:id>", methods=['DELETE'])
@token_required(role='admin')
def delete_subject(current_user, id):
    db.session.delete(Subject.query.get_or_404(id))
    db.session.commit()
    return jsonify({"message":"Subject deleted successfully!"})

@admin.route("/api/admin/<int:subject_id>/chapters", methods=['POST'])
@token_required(role='admin')
def create_chapter(current_user, subject_id):
    data = request.json
    name = data.get("name")
    description = data.get("description")

    if Chapter.query.filter_by(subject_id=subject_id, name=name).first():
        return jsonify({"message": "Chapter already exists"}), 400
    
    db.session.add(Chapter(name=name, description=description, subject_id=subject_id))
    db.session.commit()
    return jsonify({"message":"Chapter created successfully"}), 201

@admin.route("/api/admin/<int:subject_id>/chapters", methods=['GET'])
@token_required(role='admin')
def read_chapters(current_user, subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([
        {"id": c.id, "name": c.name, "description": c.description}
        for c in chapters
    ])

@admin.route("/api/admin/chapters/<int:id>", methods=['PUT'])
@token_required(role='admin')
def update_chapter(current_user, id):
    data = request.json
    Chapter.query.get_or_404(id).name = data.get("name")
    Chapter.query.get_or_404(id).description = data.get("description")
    db.session.commit()
    return jsonify({"message": "Chapter updated successfully"})

@admin.route("/api/admin/chapters/<int:id>", methods=['DELETE'])
@token_required(role='admin')
def delete_chapter(current_user, id):
    db.session.delete(Chapter.query.get_or_404(id))
    db.session.commit()
    return jsonify({"message":"Chapter deleted successfully"})

# @admin.route("/api/admin/<int:chapter_id>/quizzes", methods=['POST'])
# @token_required(role='admin')
# def create_quiz(current_user, chapter_id):
#     data = request.json
#     return jsonify()

# @admin.route("/api/admin/<int:chapter_id>/quizzes", methods=['GET'])
# @token_required(role='admin')
# def read_quizzes(current_user, chapter_id):
#     return jsonify()

# @admin.route("/api/admin/quizzes/<int:id>", methods=['PUT'])
# @token_required(role='admin')
# def update_quiz(current_user, id):
#     data = request.json
#     return jsonify()

# @admin.route("/api/admin/quizzes/<int:id>", methods=['DELETE'])
# @token_required(role='admin')
# def delete_quiz(current_user, id):
#     return jsonify()

# @admin.route("/api/admin/<int:quiz_id>/questions", methods=['POST'])
# @token_required(role='admin')
# def create_quiz(current_user, quiz_id):
#     data = request.json
#     return jsonify()

# @admin.route("/api/admin/<int:quiz_id>/questions", methods=['GET'])
# @token_required(role='admin')
# def read_quizzes(current_user, quiz_id):
#     return jsonify()

# @admin.route("/api/admin/questions/<int:id>", methods=['PUT'])
# @token_required(role='admin')
# def update_quiz(current_user, id):
#     data = request.json
#     return jsonify()

# @admin.route("/api/admin/questions/<int:id>", methods=['DELETE'])
# @token_required(role='admin')
# def delete_quiz(current_user, id):
#     return jsonify()