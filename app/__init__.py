from flask import Flask 
from config import Config 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail 


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
bootstrap = Bootstrap(app)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'vlad.shelemakha0302@gmail.com',
    MAIL_PASSWORD = "'njvjzgjxnf",
))


mail = Mail(app)

from app import models, auth, post 
login.login_view = 'auth.login'
app.register_blueprint(auth.bp)
app.register_blueprint(post.bp)


if __name__=='__main__':
	app.run(debug=True)