from ..models.db import db
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv


load_dotenv()

USERNAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASS_WORD')

class User:
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password
    def get_id(self):
        return str(self.id)
    def is_active(self):
        return True 
    def is_authenticated(self):
        return True
class UserService:
    @staticmethod
    def load_user(user_id):
    # Validate user credentials using USERNAME and PASSWORD
        if user_id == USERNAME:
            return User(user_id=USERNAME, username=USERNAME, password=PASSWORD)
        return None
                
