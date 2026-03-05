from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database import db
from models.user import User
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[\+]?[1-9][\d]{0,15}$'
    return re.match(pattern, phone.replace(' ', '')) is not None

def validate_password(password):
    """Validate password strength"""
    return len(password) >= 6

def validate_name(name):
    """Validate name length"""
    return len(name.strip()) >= 2

@auth_bp.route('/landing')
def landing_page():
    """Render the landing page"""
    return render_template('landing.html')

@auth_bp.route('/auth')
def auth_page():
    """Render the authentication page"""
    return render_template('auth.html')

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    """Handle user signup"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'phone', 'password', 'confirmPassword']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate data
        if not validate_name(data['firstName']):
            return jsonify({'error': 'First name must be at least 2 characters'}), 400
            
        if not validate_name(data['lastName']):
            return jsonify({'error': 'Last name must be at least 2 characters'}), 400
            
        if not validate_email(data['email']):
            return jsonify({'error': 'Please enter a valid email address'}), 400
            
        if not validate_phone(data['phone']):
            return jsonify({'error': 'Please enter a valid phone number'}), 400
            
        if not validate_password(data['password']):
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
            
        if data['password'] != data['confirmPassword']:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email'].lower()).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            first_name=data['firstName'].strip(),
            last_name=data['lastName'].strip(),
            email=data['email'].lower().strip(),
            phone=data['phone'].strip()
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

@auth_bp.route('/api/signin', methods=['POST'])
def signin():
    """Handle user signin"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email'].lower().strip()).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Store user in session
        session['user_id'] = user.id
        session['user_email'] = user.email
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed. Please try again.'}), 500

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/api/user', methods=['GET'])
def get_current_user():
    """Get current logged in user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@auth_bp.route('/dashboard')
def dashboard():
    """Render dashboard page (requires authentication)"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.auth_page'))
    
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return redirect(url_for('auth.auth_page'))
    
    return render_template('dashboard.html', user=user)