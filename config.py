import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path='.env', override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('FLASK_DEBUG')
    PORT= int(os.environ.get('PORT', 3001))
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username= os.environ.get('DB_USERNAME'),
    password= os.environ.get('DB_PASSWORD'),
    hostname= os.environ.get('DB_HOSTNAME'),
    databasename= os.environ.get('DB_DATABASE')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 299


