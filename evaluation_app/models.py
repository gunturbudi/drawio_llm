from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    has_consented = db.Column(db.Boolean(), default=False)

    def __init__(self, username, email, password, is_active, has_consented):
        self.username = username
        self.email = email
        self.password = password
        self.is_active = is_active
        self.has_consented = has_consented

    def is_active(self):
        return self.is_active

    def has_consented(self):
        return self.has_consented
      
    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
class LogAction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    action = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
class Criteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    # Backref 'evaluations' added here for reverse access from Criteria to Evaluations

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_name = db.Column(db.String(100))
    method = db.Column(db.String(50))
    criteria_id = db.Column(db.Integer, db.ForeignKey('criteria.id'))
    score = db.Column(db.Integer)

    criteria = db.relationship('Criteria', backref='evaluations', lazy=True)
    evaluator = db.relationship('User', backref='evaluations', lazy=True)
