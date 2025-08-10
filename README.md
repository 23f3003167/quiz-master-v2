# quiz-master-v2
Quiz master app that allows users to attempt quizzes and upgrade their knowledge.

# Getting Started

### Run the Application

`python app.py` - This will initialise the flask app. Imports database models and sets home route to the login page. A New database file will be created with predefined Admin Credentials (if not already created). We use `pip install -r requirements.txt` to install all dependencies (Flask, SQLAlchemy, etc.) either globally or inside a virtual environment. This ensures the app runs without missing package errors.

`npm run serve` - Navigate to frontend directory and run `npm install` to install necessary packages and then run `npm run serve` to start the local server. Before that, run `npm install` to install all required packages. 

`celery -A app.celery worker --loglevel=info --pool=solo` - To run celery worker, make sure redis is running at localhost:6379 port

`celery -A app.celery beat --loglevel=info` - Add scheduled jobs using Celery Beat
