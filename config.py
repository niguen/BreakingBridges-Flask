import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG')
    PORT= int(os.environ.get('PORT', 3001))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    if os.environ.get('DATABASE_FILE'):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(__file__).parent / os.environ.get('DATABASE_FILE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False