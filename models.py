from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()

class Participant(db.Model):

    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(120), nullable=False)
    invtitationSent = db.Column(db.Boolean, nullable=False, default=False)