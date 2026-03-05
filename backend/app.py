from flask import Flask, redirect, url_for
from flask_cors import CORS
import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db
from routes.analyze import analyze_bp
from routes.history import history_bp
from routes.interview import interview_bp
from routes.auth import auth_bp
from routes.ai_assistant import ai_assistant_bp
from middleware.auth_middleware import is_authenticated

# Import all models so SQLAlchemy knows about them
from models.user import User
from models.session import SpeechSession

def create_app():
    # Set template folder to the backend/templates directory
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    
    # Configure CORS for React frontend
    CORS(app, 
         origins=['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175', 'http://127.0.0.1:5173', 'http://127.0.0.1:5174', 'http://127.0.0.1:5175'],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Configure session and security
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    
    # Configure upload settings
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['UPLOAD_FOLDER'] = upload_folder
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    
    # Initialize database
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Root route - redirect to landing page or dashboard based on login status
    @app.route('/')
    def root():
        if is_authenticated():
            return redirect(url_for('analyze.index'))
        else:
            return redirect(url_for('auth.landing_page'))
    
    # Register blueprints
    app.register_blueprint(analyze_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_assistant_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)