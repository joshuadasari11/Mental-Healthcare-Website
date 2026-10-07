import os
import sqlite3
from flask import Flask, request, jsonify, session, send_from_directory, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'super-secret-key-change-this-in-production' # For sessions
DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Session login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # If the file exists in the directory, serve it
    if os.path.exists(path):
        return send_from_directory('.', path)
    # If it's a route that doesn't correspond to a file, return 404
    return send_from_directory('.', 'index.html'), 404

# APIs
@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.json or request.form
        name = data.get('name')
        email = data.get('email')
        mobile_number = data.get('mobile_number')
        address = data.get('address')
        message = data.get('message', '')

        if not name or not email or not mobile_number or not address:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, mobile_number, address, message) VALUES (?, ?, ?, ?, ?)",
            (name, email, mobile_number, address, message)
        )
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Inquiry submitted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.json or request.form
        email = data.get('email')

        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
            conn.commit()
        except sqlite3.IntegrityError:
            # Already subscribed
            return jsonify({'success': True, 'message': 'You are already subscribed!'})
        finally:
            conn.close()

        return jsonify({'success': True, 'message': 'Subscribed successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json or request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return jsonify({'success': True, 'message': 'Logged in successfully', 'redirect': '/admin.html'})
        
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/signup-status', methods=['GET'])
def signup_status():
    try:
        conn = get_db_connection()
        count = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()['count']
        conn.close()
        return jsonify({'success': True, 'signup_allowed': count < 2})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json or request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400

        conn = get_db_connection()
        # Enforce maximum of 2 admins
        count = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()['count']
        if count >= 2:
            conn.close()
            return jsonify({'success': False, 'message': 'Administrator account limit reached (maximum 2 admins).'}), 403

        existing = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            conn.close()
            return jsonify({'success': False, 'message': 'Username already exists'}), 400

        hashed_password = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hashed_password, 'admin')
        )
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'User registered successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully', 'redirect': '/login.html'})

@app.route('/api/admin/dashboard-data', methods=['GET'])
@login_required
def dashboard_data():
    try:
        conn = get_db_connection()
        
        # Get contacts
        contacts_rows = conn.execute("SELECT * FROM contacts ORDER BY created_at DESC").fetchall()
        contacts = [dict(row) for row in contacts_rows]
        
        # Get subscribers
        subscribers_rows = conn.execute("SELECT * FROM subscribers ORDER BY created_at DESC").fetchall()
        subscribers = [dict(row) for row in subscribers_rows]
        
        # Get users count
        users_count = conn.execute("SELECT COUNT(*) as count FROM users").fetchone()['count']
        
        conn.close()

        return jsonify({
            'success': True,
            'stats': {
                'total_contacts': len(contacts),
                'total_subscribers': len(subscribers),
                'total_users': users_count
            },
            'contacts': contacts,
            'subscribers': subscribers
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/delete-contact', methods=['POST'])
@login_required
def delete_contact():
    try:
        data = request.json
        contact_id = data.get('id')
        if not contact_id:
            return jsonify({'success': False, 'message': 'Contact ID is required'}), 400

        conn = get_db_connection()
        conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Contact deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/delete-subscriber', methods=['POST'])
@login_required
def delete_subscriber():
    try:
        data = request.json
        subscriber_id = data.get('id')
        if not subscriber_id:
            return jsonify({'success': False, 'message': 'Subscriber ID is required'}), 400

        conn = get_db_connection()
        conn.execute("DELETE FROM subscribers WHERE id = ?", (subscriber_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Subscriber deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # Ensure database is initialized
    import init_db
    init_db.init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
