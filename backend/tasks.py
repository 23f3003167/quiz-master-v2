from app import app, celery, mail
from models import db, User, Quiz, Score
from datetime import datetime, date
from flask_mail import Message
from flask import url_for
import csv, os

@celery.task
def send_daily_reminder():
        today = date.today()
        quizzes = Quiz.query.filter_by(date_of_quiz=today).all()
        users = User.query.filter_by(role="user").all()
        
        if not quizzes: 
            return

        for user in users:
            msg = Message("Today's Quiz Reminder", sender="sanjaysakthi000@gmail.com", recipients=[user.username])
            msg.body = f"Hello {user.full_name},\n\n You have quizzes scheduled for today. Attempt quickly."
            mail.send(msg)
        
        return "Reminder Sent"

        # for user in users:
        #     print(f"Hello {user.full_name}, attempt today's quizzes:")
        #     for quiz in quizzes:
        #         print(f" - {quiz.title} | {quiz.chapter.subject.name} | {quiz.chapter.name}")

@celery.task
def send_monthly_report():
        users = User.query.filter_by(role="user").all()
        for user in users:
            scores = Score.query.filter_by(user_id=user.id).all()
            total = sum(score.total_scored for score in scores)
            attempts = len(scores)
            msg = Message("Monthly Quiz Report", sender="sanjaysakthi000@gmail.com", recipients=[user.username])
            msg.body = f"Hello {user.full_name},\n\n Your total quiz score so far is: {total}."
            mail.send(msg)
        return "Monthly report sent"

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
    