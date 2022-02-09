from flask import Flask
import os
from src.auth import auth
import src.constants
from src.token import token
from src.database import db
from flask_jwt_extended import JWTManager
import datetime


def create_app():
    '''Setup app variables'''
    app=Flask(__name__,instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(seconds=1300),
    )

    db.app=app
    db.init_app(app)
    
    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(token)
        
    return app