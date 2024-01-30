from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from .routes import main
from .services.user_service import  User
from flask_login import LoginManager
from sqlalchemy.exc import SQLAlchemyError
from .models.data_model import db
from flask_migrate import Migrate
from functools import wraps
from flask_pymongo import PyMongo



def create_app():
    app = Flask(__name__)
    login_manager = LoginManager(app)

    # Load biến môi trường từ file .env
    load_dotenv()

    # Cấu hình SQLAlchemy trực tiếp
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    # Cấu hình token
    app.config['SECRET_KEY'] = f"{os.getenv('SECRET_KEY')}"

    

    # Cấu hình SQLAlchemy cho models
    db.init_app(app)

    
    
    @login_manager.user_loader
    def load_user(user_id):
        username = os.getenv('USER_NAME')
        password = os.getenv('PASS_WORD')
        user_name = str(username)
        print(user_id + ' userId')
        print( user_name + ' userId')
        # Validate user credentials
        if user_id == username:
            print('User have')
            return User(user_id=username, username=username, password=password)

        return None

    migrate = Migrate(app, db)

    app.register_blueprint(main)

    

    return app
