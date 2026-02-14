"""
Vulnerable Web Application - Code Review Lab
WARNING: This application contains intentional security vulnerabilities
for educational purposes only. DO NOT deploy to production!
"""

from flask import Flask, request, render_template, render_template_string, redirect, url_for, make_response
import sqlite3
import pickle
import base64
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev_secret_123'


def get_db_connection():
    """Helper function to get database connection"""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    """Homepage with navigation"""
    return render_template('home.html')


@app.route('/greet')
def greet():
    """Greeting page demonstrating SSTI vulnerability"""
    name = request.args.get('name', '')
    if name:
        return render_template_string(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Greeting Result - Vulnerable Web App</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🔓 Vulnerable Web Application</h1>
            <p class="subtitle">Code Review Laboratory - Educational Purposes Only</p>
        </header>
        
        <div class="warning-banner">
            ⚠️ WARNING: This application contains intentional security vulnerabilities. Do NOT deploy to production!
        </div>
        
        <div class="content">
            <h2>💬 Personalized Greeting</h2>
            
            <div class="alert alert-success" style="margin-bottom: 2rem;">
                <strong>✅ Success:</strong> Your greeting has been generated!
            </div>
            
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem; border-radius: 12px; text-align: center; margin: 2rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                <h1 style="color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    Hello {name}! 👋
                </h1>
            </div>
            
            <div style="background: var(--light-bg); padding: 2rem; border-radius: 12px; margin: 2rem 0;">
                <h3 style="margin-bottom: 1rem; color: var(--primary-color);">📝 Request Details</h3>
                <div style="display: grid; grid-template-columns: auto 1fr; gap: 1rem;">
                    <strong style="color: var(--text-secondary);">Input Received:</strong>
                    <code style="background: white; padding: 0.5rem; border-radius: 4px; border: 1px solid var(--border-color);">{name}</code>
                    
                    <strong style="color: var(--text-secondary);">Vulnerability:</strong>
                    <span style="color: var(--danger-color); font-weight: 600;">SSTI (Server-Side Template Injection)</span>
                    
                    <strong style="color: var(--text-secondary);">Status:</strong>
                    <span style="color: var(--success-color); font-weight: 600;">Template Rendered</span>
                </div>
            </div>
            
            <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
                <a href="/greet" class="btn btn-primary">Try Another Name</a>
                <a href="/" class="btn btn-secondary">Back to Home</a>
                <a href="/vulnerabilities" class="btn btn-secondary">Learn About SSTI</a>
            </div>
        </div>
        
        <footer>
            <p>&copy; 2026 Code Review Lab | For Educational and Training Purposes Only</p>
        </footer>
    </div>
</body>
</html>
        ''')  # VULN #2: SSTI vulnerability maintained
    else:
        return render_template('greet.html')


@app.route('/users')
def list_users():
    """List all users from database"""
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, email FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)


@app.route('/user/<user_id>')
def get_user(user_id):
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    
    try:
        result = conn.execute(query).fetchone()
        conn.close()
        
        if result:
            user_data = dict(result)
            return render_template('user_detail.html', user=user_data)
        else:
            return render_template('user_detail.html', user=None, error="User not found")
    except Exception as e:
        conn.close()
        return render_template('user_detail.html', user=None, error=f"Database error: {str(e)}")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', error="No file selected")
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('upload.html', error="No file selected")
        file.save(f'uploads/{file.filename}')
        
        return render_template('upload.html', success=f"File '{file.filename}' uploaded successfully!")
    
    return render_template('upload.html')


@app.route('/session/save')
def save_session():
    data = {'user': 'guest', 'role': 'user', 'timestamp': '2026-02-14'}
    pickled = base64.b64encode(pickle.dumps(data)).decode()
    
    response = make_response(render_template('session.html', action='saved', data=str(data)))
    response.set_cookie('session_data', pickled)
    return response


@app.route('/session/load')
def load_session():
    data_cookie = request.cookies.get('session_data')
    
    if not data_cookie:
        return render_template('session.html', action='load_failed', error="No session data found")
    
    try:
        data = pickle.loads(base64.b64decode(data_cookie))
        return render_template('session.html', action='loaded', data=str(data))
    except Exception as e:
        return render_template('session.html', action='load_failed', error=str(e))


@app.route('/command', methods=['GET', 'POST'])
def run_command():
    output = None
    error = None
    
    if request.method == 'POST':
        cmd = request.form.get('cmd', '')
        
        if cmd:
            try:
                output = os.popen(cmd).read()
            except Exception as e:
                error = str(e)
    
    return render_template('command.html', output=output, error=error)


@app.route('/vulnerabilities')
def vulnerabilities():
    return render_template('vulnerabilities.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, host='127.0.0.1', port=5000)
