from flask import Flask 
from config import Config 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
bootstrap = Bootstrap(app)


from app import models, auth, post 
login.login_view = 'auth.login'
app.register_blueprint(auth.bp)
app.register_blueprint(post.bp)


if __name__=='__main__':
	app.run(debug=True)