from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    workouts = db.relationship('Workout', backref='user', lazy=True)
    bank_balance = db.Column(db.Integer, default=0)
    savings_balance = db.Column(db.Integer, default=0)
    
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)