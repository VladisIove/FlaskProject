import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = True 
	POSTS_PER_PAGE=5
	UPLOAD_FOLDER = os.path.join(basedir, 'app/uploads')