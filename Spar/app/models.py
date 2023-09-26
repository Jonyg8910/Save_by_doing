from datetime import datetime
from app import db
from app.services import save_money_for_workout
from flask import request, jsonify
from werkzeug.security import generate_password_hash
import uuid

class User:
    def __init__(db.Model):
        id = db.Column(db.String(36), primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        email = db.Column(db.String(50), nullable=False)
        password = db.Column(db.String(80), nullable=False)
        workouts = db.relationship('Workout', backref='user', lazy=True)
    
    def register():
        data = request.json
        
        #Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'Email already registered'}), 400
        
        #Hash password
        hashed_password = generate_password_hash(data['password'], method='sha256')

        #Create a new user 
        new_user = User(id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201


class Workout:
    def __init__(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def log_workout():
        data = request.json

        # Ensure all required fields are provided
        if not data.get('user_id'):
            return jsonify({'message': 'Missing fields'}), 400

        # Create a new Workout object
        new_workout = Workout(user_id=data['user_id'])
        db.session.add(new_workout)
        
        # Get the user's current details
        user = User.query.filter_by(id=data['user_id']).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Call the save_money() method to update the user's balances
        savings_result = save_money_for_workout(user)
        if not savings_result:
            db.session.rollback()
            return jsonify({'message': 'Error saving money. Maybe insufficient funds.'}), 500

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({'message': 'Error logging workout'}), 500

        return jsonify({'message': 'Workout logged successfully', 'total_savings': savings_result}), 201
