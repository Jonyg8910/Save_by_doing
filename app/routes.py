from app import app, db
from app.models import User, Workout
from app.services import save_money_for_workout
from flask import request, jsonify
from werkzeug.security import generate_password_hash
import uuid

@app.route('/register', methods=['POST'])
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

@app.route('/log_workout', methods=['POST'])
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