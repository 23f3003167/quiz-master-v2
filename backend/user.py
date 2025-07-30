from auth import token_required
from flask import Blueprint, jsonify, json, request
from models import db, Quiz, User, Chapter, Question, Subject, Score
from datetime import datetime

user = Blueprint("user", __name__)

@user.route("/api/user/quizzes", methods=['GET'])
@token_required(role='user')
def view_quizzes(current_user):
    quizzes = Quiz.query.join(Chapter).join(Subject).all()
    data = []
    for quiz in quizzes:
        data.append({
            "id": quiz.id,
            "title": quiz.title,
            "date_of_quiz": quiz.date_of_quiz.strftime("%Y-%m-%d"),
            "subject": quiz.chapter.subject.name,
            "chapter": quiz.chapter.name,
            "question_count": Question.query.filter_by(quiz_id=quiz.id).count()
        })
    return jsonify(data)

@user.route("/api/user/quizzes/<int:quiz_id>/questions", methods=['GET'])
@token_required(role='user')
def get_quiz_questions(current_user, quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify({
        "quiz": {
            "title": quiz.title,
            "time_duration": quiz.time_duration
        },
        "questions": [
            {
                "id": q.id,
                "question_statement": q.question_statement,
                "option_1": q.option_1,
                "option_2": q.option_2,
                "option_3": q.option_3,
                "option_4": q.option_4
            } for q in questions
        ]
    })

@user.route("/api/user/quizzes/<int:quiz_id>/submit", methods=["POST"])
@token_required(role="user")
def submit_quiz(current_user, quiz_id):
    data = request.json
    answers = data.get("answers",[])
    start_time = datetime.fromisoformat(data.get("start_time"))
    end_time = datetime.now()

    score = 0
    for ans in answers:
        question = Question.query.get(ans["question_id"])
        if question and question.correct_option == ans["selected"]:
            score +=1
    
    time_taken = (end_time - start_time).seconds
    minutes = time_taken//60
    seconds = time_taken%60

    db.session.add(
        Score(
            quiz_id=quiz_id,
            user_id = current_user.id,
            time_stamp_of_attempt = end_time,
            total_scored = score,
            completion_minutes = minutes,
            completion_seconds = seconds
        )
    )
    db.session.commit()

    return jsonify({"message": "Quiz submitted", "score": score, "time": f"{minutes} minutes {seconds} seconds"})

@user.route("/api/user/scores", methods=['GET'])
@token_required(role='user')
def user_scores():
    scores = Score.query.filter_by(user_id=g.user.id).order_by(Score.time_stamp_of_attempt.desc()).all()
    data = []
    for score in scores:
        quiz = score.quiz
        question_count = len(quiz.questions)
        data.append({
            "title": quiz.title,
            "attempted on": score.time_stamp_of_attempt.strftime("%d-%m-%Y %H:%M:%S"),
            "total_scored": score.total_scored,
            "question_count": question_count,
            "completion_minutes": score.completion_minutes,
            "completion_seconds": score.completion_seconds,
        })
    return jsonify(data)