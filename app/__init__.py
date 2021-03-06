from flask import Flask 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from config import config

from flask.ext.login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    #mail.init_app(app)
    #moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    from .todo import todo as todo_blueprint
    from .pic import pic as pic_blueprint
    from .auth import auth as auth_blueprint 
    
    app.register_blueprint(todo_blueprint)
    app.register_blueprint(pic_blueprint)
    app.register_blueprint(auth_blueprint)
    
    return app