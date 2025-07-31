from auth import token_required
from flask import Blueprint, jsonify, json, request, session
from models import Quiz, User, Chapter, Question, Subject, Score
from datetime import datetime, timezone, timedelta
from extensions import db, cache, limiter

user = Blueprint("user", __name__)

@user.route("/api/user/quizzes", methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=60)
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

from datetime import datetime

@user.route("/user/quizzes/<int:quiz_id>/attempt", methods=["GET", "POST"])
@token_required(role='user')
def attempt_quiz(current_user, quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    if request.method == "GET":
        return jsonify({
            "quiz": {
                "id": quiz.id,
                "title": quiz.title,
                "time_duration": quiz.time_duration
            },
            "questions": [
                {
                    "id": q.id,
                    "statement": q.question_statement,
                    "options": [q.option_1, q.option_2, q.option_3, q.option_4]
                } for q in questions
            ]
        })

    if request.method == "POST":
        data = request.get_json()
        answers = data.get("answers", {})
        score = 0

        for q in questions:
            selected = answers.get(str(q.id))
            if selected and int(selected) == q.correct_option:
                score += 1

        start_time = data.get("start_time")
        end_time = datetime.now(timezone.utc)
        if start_time:
            try:
                start = datetime.fromisoformat(start_time)
                if start.tzinfo is not None:
                    start = start.astimezone(timezone.utc)
                else:
                    start = start.replace(tzinfo=timezone.utc)
                duration = (end_time - start).seconds
                minutes = duration // 60
                seconds = duration % 60
            except Exception as e:
                minutes, seconds = 0, 0
        else:
            minutes, seconds = 0, 0

        new_score = Score(
            quiz_id=quiz_id,
            user_id=current_user.id,
            time_stamp_of_attempt=end_time,
            total_scored=score,
            completion_minutes=minutes,
            completion_seconds=seconds
        )
        db.session.add(new_score)
        db.session.commit()

        return jsonify({
            "message": "Quiz submitted!",
            "score": score,
            "total": len(questions),
            "minutes": minutes,
            "seconds": seconds
        })

@user.route("/api/user/scores", methods=['GET'])
@token_required(role='user')
def user_scores(current_user):
    scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).all()
    data = []
    for score in scores:
        quiz = score.quiz
        question_count = quiz.questions.count()
        ist_time = score.time_stamp_of_attempt + timedelta(hours=5, minutes=30)
        data.append({
            "title": quiz.title,
            "attempted_on": ist_time.strftime("%d-%m-%Y %H:%M:%S"),
            "total_scored": score.total_scored,
            "question_count": question_count,
            "completion_minutes": score.completion_minutes,
            "completion_seconds": score.completion_seconds,
        })
    return jsonify(data)

@user.route("/api/user/summary", methods=['GET'])
@token_required(role='user')
def quiz_summary(current_user):
    scores = Score.query.filter_by(user_id=current_user.id).all()
    highest_scores = {}
    for score in scores:
        quiz_title = score.quiz.title
        if quiz_title in highest_scores:
            highest_scores[quiz_title] = max(highest_scores[quiz_title], score.total_scored)
        else:
            highest_scores[quiz_title] = score.total_scored
        
    return jsonify({
        "quiz_titles": list(highest_scores.keys()),
        "scores_list": list(highest_scores.values())
    })

@user.route("/api/user/search", methods=['POST'])
@token_required(role='user')
def user_search(user):
    data = request.json
    search_term = data.get("search_term","").strip()
    filter_by = data.get("filter_by",[])

    results = []
    if "subjects" in filter_by:
            subjects = Subject.query.filter(Subject.name.ilike(f"%{search_term}%")).all()
            results.extend([{"type":"subject", "name": s.name} for s in subjects])
    if "quizzes" in filter_by:
            quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{search_term}%")).all()
            results.extend([{"type":"quiz", "name": q.name} for q in quizzes])

    return jsonify(results)