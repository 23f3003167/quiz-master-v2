# quiz-master-v2
Quiz master app that allows users to attempt quizzes and upgrade their knowledge.

# Getting Started

### Run the Application

`python app.py` - This will initialise the flask app. Imports database models and sets home route to the login page. A New database file will be created with predefined Admin Credentials (if not already created). 

`npm run serve` - Navigate to frontend directory and run `npm install` to install necessary packages and then run `npm run serve` to start the local server.

`celery -A app.celery worker --loglevel=info --pool=solo` - To run celery worker, make sure redis is running at localhost:6379 port

`celery -A app.celery beat --loglevel=info` - Add scheduled jobs using Celery Beat
