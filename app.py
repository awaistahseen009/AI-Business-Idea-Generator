from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
from asgiref.wsgi import WsgiToAsgi

# Load environment variables
load_dotenv()

# Import blueprints
from routes.auth import auth_bp
from routes.ideas import ideas_bp


app = Flask(__name__)
    
    # Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['WTF_CSRF_ENABLED'] = os.getenv('WTF_CSRF_ENABLED', 'True').lower() == 'true'
    
    # Initialize CSRF protection
csrf = CSRFProtect(app)
    
    # Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(ideas_bp, url_prefix='/ideas')
    
    # Main routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('ideas.dashboard'))
    return render_template('index.html')
    
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('ideas.dashboard'))
    
    # Create upload folder if it doesn't exist
upload_folder = app.config['UPLOAD_FOLDER']
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)


# ASGI wrapper so Uvicorn can serve this Flask app: `uvicorn app:asgi_app`
asgi_app = WsgiToAsgi(app)


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
