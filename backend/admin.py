from flask import Blueprint, jsonify, request
from auth import token_required
from models import User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime
from extensions import db, cache, limiter

admin = Blueprint("admin", __name__)

@admin.route("/api/admin/dashboard-data", methods=['GET'])
@token_required(role='admin')
def get_admin_dashboard_data(current_user):
    subject_list = []
    subjects = Subject.query.all()
    for subject in subjects:
        chapters_data = []
        for chapter in subject.chapters:
            quiz_count = Quiz.query.filter_by(chapter_id=chapter.id).count()
            chapters_data.append({
                "id": chapter.id,
                "name": chapter.name,
                "quiz_count": quiz_count
            })
        subject_list.append({
            "id": subject.id,
            "name": subject.name,
            "chapters": chapters_data
        })
    return jsonify({"subjects": subject_list})

@admin.route('/api/admin/users', methods=['GET'])
@token_required(role='admin')
def view_users(current_user):
    users = User.query.filter_by(role="user").all()
    return jsonify([{
        "id": u.id,
        "email": u.username,
        "full_name": u.full_name,
        "qualification": u.qualification,
        "dob": u.dob
    } for u in users])


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

@admin.route("/api/admin/subjects/<int:subject_id>/chapters", methods=['POST'])
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

@admin.route("/api/admin/subjects/<int:subject_id>/chapters", methods=['GET'])
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

@admin.route("/api/admin/<int:chapter_id>/quizzes", methods=['POST'])
@token_required(role='admin')
def create_quiz(current_user, chapter_id):
    data = request.json
    db.session.add(Quiz(
        chapter_id = chapter_id,
        title = data.get("title"),
        date_of_quiz = datetime.strptime(data.get("date_of_quiz"), "%Y-%m-%d").date(),
        time_duration=data.get("time_duration"),
        remarks=data.get("remarks")
    ))
    db.session.commit()
    return jsonify({"message":"Quiz created successfully"}), 201

@admin.route("/api/admin/<int:chapter_id>/quizzes", methods=['GET'])
@token_required(role='admin')
def read_quizzes(current_user, chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return jsonify([{
        "id":q.id,
        "title": q.title,
        "date_of_quiz": q.date_of_quiz.strftime("%Y-%m-%d"),
        "time_duration":q.time_duration,
        "remarks": q.remarks
    } for q in quizzes])

@admin.route("/api/admin/quizzes/<int:id>", methods=['PUT'])
@token_required(role='admin')
def update_quiz(current_user, id):
    data = request.json
    quiz = Quiz.query.get_or_404(id)
    quiz.title = data.get("title")
    quiz.date_of_quiz = datetime.strptime(data.get("date_of_quiz"), "%Y-%m-%d").date()
    quiz.time_duration = data.get("time_duration")
    db.session.commit()
    return jsonify({"message":"Quiz updated successfully"}), 201

@admin.route("/api/admin/quizzes/<int:id>", methods=['DELETE'])
@token_required(role='admin')
def delete_quiz(current_user, id):
    db.session.delete(Quiz.query.get_or_404(id))
    db.session.commit()
    return jsonify({"message":"Quiz deleted successfully"}), 201

@admin.route("/api/admin/<int:quiz_id>/questions", methods=['POST'])
@token_required(role='admin')
def create_question(current_user, quiz_id):
    data = request.json
    db.session.add(Question(
        quiz_id=quiz_id,
        question_statement=data.get("question_statement"),
        option_1=data.get("option_1"),
        option_2=data.get("option_2"),
        option_3=data.get("option_3"),
        option_4=data.get("option_4"),
        correct_option=data.get("correct_option")
    ))
    db.session.commit()
    return jsonify({"message":"Question added successfully"}), 201

@admin.route("/api/admin/<int:quiz_id>/questions", methods=['GET'])
@token_required(role='admin')
def read_questions(current_user, quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([{
        "id": q.id,
        "question_statement": q.question_statement,
        "option_1": q.option_1,
        "option_2": q.option_2,
        "option_3": q.option_3,
        "option_4": q.option_4,
        "correct_option": q.correct_option
    }for q in questions])

@admin.route("/api/admin/questions/<int:id>", methods=['PUT'])
@token_required(role='admin')
def update_question(current_user, id):
    data = request.json
    q = Question.query.get_or_404(id)
    q.question_statement = data.get("question_statement")
    q.option_1 = data.get("option_1")
    q.option_2 = data.get("option_2")
    q.option_3 = data.get("option_3")
    q.option_4 = data.get("option_4")
    q.correct_option = data.get("correct_option")
    db.session.commit()
    return jsonify({"message":"Question updated successfully"})

@admin.route("/api/admin/questions/<int:id>", methods=['DELETE'])
@token_required(role='admin')
def delete_question(current_user, id):
    db.session.delete(Question.query.get_or_404(id))
    db.session.commit()
    return jsonify({"message":"Question deleted successfully"})

@admin.route("/api/admin/search", methods=['POST'])
@token_required(role='admin')
def admin_search(user):
    data = request.json
    search_term = data.get("search_term","").strip()
    filter_by = data.get("filter_by",[])

    results = []

    if "subjects" in filter_by:
            subjects = Subject.query.filter(Subject.name.ilike(f"%{search_term}%")).all()
            results.extend([{"type":"subject", "name": s.name} for s in subjects])
    if "quizzes" in filter_by:
            quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{search_term}%")).all()
            results.extend([{"type":"quiz", "title": q.title} for q in quizzes])
    if "users" in filter_by:
            users = User.query.filter(User.full_name.ilike(f"%{search_term}%")).all()
            results.extend([{"type":"user", "name": u.full_name, "email":u.username} for u in users])
    if "questions" in filter_by:
            questions = Question.query.filter(Question.question_statement.ilike(f"%{search_term}%")).all()
            results.extend([{"type":"question", "statement": q.question_statement} for q in questions])

    return jsonify(results)

@admin.route('/api/admin/export-users-data', methods=['GET'])
@token_required(role='admin')
def admin_csv(user):
     from tasks import export_all_users_data
     task = export_all_users_data.delay()
     return jsonify({"message":"CSV export started","task_id":task.id})

@admin.route('/api/admin/summary', methods=['GET'])
@token_required(role='admin')
def quiz_summary(user):
    subjects = Subject.query.all()
    top_scores = {}

    for subject in subjects:
        quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject.id).all()
        quiz_ids = [q.id for q in quizzes]

        if not quiz_ids:
               continue
          
        top_result = (
               db.session.query(Score)
               .filter(Score.quiz_id.in_(quiz_ids))
               .order_by(Score.total_scored.desc())
               .first()
        )

        if top_result:
            user = User.query.get(top_result.user_id)
            top_scores[subject.name] = {
                "score": top_result.total_scored,
                "user": user.full_name if user else "Unknown"
            }

    return jsonify({"top_scores": top_scores})