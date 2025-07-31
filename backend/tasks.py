from app import app, celery, mail
from models import db, User, Quiz, Score
from datetime import datetime, date
from flask_mail import Message
from flask import url_for, render_template_string
import csv, os

@celery.task
def send_daily_reminder():
    today = date.today()
    quizzes_today = Quiz.query.filter_by(date_of_quiz=today).all()
    users = User.query.filter_by(role="user").all()

    if not quizzes_today:
        return "No quizzes today"

    for user in users:
        msg = Message("Today's Quiz Reminder",
                      sender="sanjaysakthi000@gmail.com",
                      recipients=[user.username])
        msg.body = f"Hello {user.full_name},\n\nYou have quizzes scheduled today. Please log in and attempt them!"
        mail.send(msg)
    return "Reminders Sent"

@celery.task
def send_monthly_report():
    users = User.query.filter_by(role="user").all()
    start = date.today().replace(day=1)
    end = (start.replace(month=start.month+1) if start.month != 12 else start.replace(year=start.year+1, month=1))

    all_scores = Score.query.filter(Score.time_stamp_of_attempt >= start).all()
    rankings = {}

    for score in all_scores:
        uid = score.user_id
        rankings[uid] = rankings.get(uid, 0) + score.total_scored

    sorted_ranks = {uid: rank+1 for rank, (uid, _) in enumerate(sorted(rankings.items(), key=lambda x: -x[1]))}

    for user in users:
        scores = Score.query.filter(Score.user_id == user.id, Score.time_stamp_of_attempt >= start).all()
        total = sum(score.total_scored for score in scores)
        count = len(scores)
        avg = round(total / count, 2) if count else 0
        rank = sorted_ranks.get(user.id, "N/A")

        html = render_template_string("""
        <h3>Hi {{ name }},</h3>
        <p>Here's your performance summary for the month:</p>
        <ul>
            <li>Total quizzes attempted: <b>{{ count }}</b></li>
            <li>Total score: <b>{{ total }}</b></li>
            <li>Average score: <b>{{ avg }}</b></li>
            <li>Your rank: <b>{{ rank }}</b></li>
        </ul>
        """, name=user.full_name, count=count, total=total, avg=avg, rank=rank)

        msg = Message("Monthly Performance Report",
                      sender="sanjaysakthi000@gmail.com",
                      recipients=[user.username])
        msg.html = html
        mail.send(msg)

    return "Monthly Reports Sent"

@celery.task
def export_all_users_data():
    users = User.query.filter_by(role="user").all()
    filename = f"exports/admin_users_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name","Email","Total Attempts","Total Score"])
        for user in users:
            scores = Score.query.filter_by(user_id=user.id).all()
            total_score = sum(s.total_scored for s in scores)
            writer.writerow([user.full_name, user.username, len(scores), total_score])
    return filename
    