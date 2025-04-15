from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
from pymongo.errors import ConfigurationError
import bcrypt
from functools import wraps
import uuid
import datetime
import os

# Create Blueprint
auth = Blueprint('auth', __name__)

# MongoDB Connection for user authentication
client = MongoClient("mongodb+srv://tejaschavan1110:uQe4SlyVi6H5ExIH@cluster0.os2upfz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['url_checker_db']
users_collection = db['users']
sessions_collection = db['sessions']

# MongoDB Connection for tokens
try:
    MONGO_URI = "mongodb+srv://tejaschavan1110:sQbJc2WGV7nFaANX@cluster0.kepqz.mongodb.net/?retryWrites=true&w=majority"
    token_client = MongoClient(MONGO_URI)
    token_db = token_client['terabox_bot']
    tokens_collection = token_db['users']
    
    # Test the connection
    token_client.admin.command('ping')
    print("Token MongoDB connection successful")
    use_mongodb = True
except Exception as e:
    print(f"Token MongoDB connection failed: {e}")
    print("Using in-memory token storage instead")
    use_mongodb = False
    # In-memory token storage as fallback
    memory_tokens = {}

# MongoDB Connection for user tokens storage
try:
    USER_TOKENS_URI = "mongodb+srv://tejaschavan1110:ftEzykJghoR9t8ux@cluster0.gogjux3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    user_tokens_client = MongoClient(USER_TOKENS_URI)
    user_tokens_db = user_tokens_client['user_tokens_db']
    user_tokens_collection = user_tokens_db['user_tokens']
    
    # Test the connection
    user_tokens_client.admin.command('ping')
    print("User Tokens MongoDB connection successful")
    use_user_tokens_db = True
except Exception as e:
    print(f"User Tokens MongoDB connection failed: {e}")
    print("Using main database for user tokens instead")
    use_user_tokens_db = False
    # Use main database as fallback
    user_tokens_collection = db['user_tokens']

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or 'session_id' not in session:
            return redirect(url_for('auth.login'))
        
        # Check if the current session is still valid
        current_session = sessions_collection.find_one({
            'username': session['username'],
            'session_id': session['session_id'],
            'active': True
        })
        
        if not current_session:
            # Session has been invalidated
            session.clear()
            return redirect(url_for('auth.login', session_expired=True))
        
        # Check if user has a stored token and it's not in session
        if 'token' not in session:
            # Try to get stored token for this user
            stored_token_doc = user_tokens_collection.find_one({
                'username': session['username']
            })
            
            if stored_token_doc and 'token' in stored_token_doc:
                # Verify if the stored token is valid
                if use_mongodb:
                    token_doc = tokens_collection.find_one({'token': stored_token_doc['token']})
                    is_valid = token_doc and token_doc.get('token_expiration', datetime.datetime.min) > datetime.datetime.now()
                
                    if is_valid:
                        # Token is valid, add to session
                        session['token'] = stored_token_doc['token']
                        print(f"Auto-loaded token for user {session['username']}")
            
        return f(*args, **kwargs)
    return decorated_function

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            return jsonify({
                'error': 'Token required', 
                'code': 'NO_TOKEN',
                'message': 'You need to provide a token to use this feature'
            }), 401
        
        token = session['token']
        
        # Check if token exists and is valid
        if use_mongodb:
            user_doc = tokens_collection.find_one({'token': token})
            is_valid = user_doc and user_doc.get('token_expiration', datetime.datetime.min) > datetime.datetime.now()
            
            if user_doc and not is_valid:
                # Token exists but expired
                expiry_date = user_doc.get('token_expiration')
                
                # Format expiry date message
                if expiry_date:
                    expiry_str = expiry_date.strftime('%d %b %Y at %H:%M')
                    expiry_message = f"Your token expired on {expiry_str}"
                else:
                    expiry_message = "Your token has expired"
                
                # Token expired, remove from session and storage
                session.pop('token', None)
                
                # Also remove from user storage if it exists
                if 'username' in session:
                    user_tokens_collection.update_one(
                        {'username': session['username']},
                        {'$unset': {'token': ""}}
                    )
                
                return jsonify({
                    'error': 'Token expired', 
                    'code': 'EXPIRED_TOKEN',
                    'message': expiry_message
                }), 401
            
            elif not user_doc:
                # Token not found
                session.pop('token', None)
                
                # Also remove from user storage if it exists
                if 'username' in session:
                    user_tokens_collection.update_one(
                        {'username': session['username']},
                        {'$unset': {'token': ""}}
                    )
                
                return jsonify({
                    'error': 'Invalid token', 
                    'code': 'INVALID_TOKEN',
                    'message': 'Your token is not valid. Please get a new token from the Telegram bot.'
                }), 401
        else:
            user_doc = memory_tokens.get(token)
            is_valid = user_doc and user_doc.get('token_expiration', datetime.datetime.min) > datetime.datetime.now()
            
            if user_doc and not is_valid:
                # Token exists but expired
                expiry_date = user_doc.get('token_expiration')
                
                # Format expiry date message
                if expiry_date:
                    expiry_str = expiry_date.strftime('%d %b %Y at %H:%M')
                    expiry_message = f"Your token expired on {expiry_str}"
                else:
                    expiry_message = "Your token has expired"
                
                # Token expired, remove from session
                session.pop('token', None)
                
                # Also remove from user storage if it exists
                if 'username' in session:
                    user_tokens_collection.update_one(
                        {'username': session['username']},
                        {'$unset': {'token': ""}}
                    )
                
                return jsonify({
                    'error': 'Token expired', 
                    'code': 'EXPIRED_TOKEN',
                    'message': expiry_message
                }), 401
            
            elif not user_doc:
                # Token not found
                session.pop('token', None)
                
                # Also remove from user storage if it exists
                if 'username' in session:
                    user_tokens_collection.update_one(
                        {'username': session['username']},
                        {'$unset': {'token': ""}}
                    )
                
                return jsonify({
                    'error': 'Invalid token', 
                    'code': 'INVALID_TOKEN',
                    'message': 'Your token is not valid. Please get a new token from the Telegram bot.'
                }), 401
        
        if not is_valid:
            # Token not found or expired, remove from session
            session.pop('token', None)
            
            # Also remove from user storage if it exists
            if 'username' in session:
                user_tokens_collection.update_one(
                    {'username': session['username']},
                    {'$unset': {'token': ""}}
                )
            
            return jsonify({
                'error': 'Invalid or expired token', 
                'code': 'INVALID_TOKEN',
                'message': 'Your token is not valid or has expired. Please get a new token from the Telegram bot.'
            }), 401
            
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session and 'session_id' in session:
            # Verify the session is still valid
            current_session = sessions_collection.find_one({
                'username': session['username'],
                'session_id': session['session_id'],
                'active': True
            })
            
            if current_session:
                return redirect(url_for('home'))
            else:
                session.clear()
        
        return render_template('login.html')
    
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = users_collection.find_one({'username': username})
        
        if not user:
            return jsonify({'message': 'Username not found'}), 401
        
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # Invalidate any existing sessions for this user
            sessions_collection.update_many(
                {'username': username, 'active': True},
                {'$set': {'active': False, 'ended_at': datetime.datetime.now()}}
            )
            
            # Create new session
            session_id = str(uuid.uuid4())
            user_agent = request.headers.get('User-Agent', 'Unknown Device')
            ip_address = request.remote_addr
            
            new_session = {
                'username': username,
                'session_id': session_id,
                'user_agent': user_agent,
                'ip_address': ip_address,
                'created_at': datetime.datetime.now(),
                'active': True
            }
            
            sessions_collection.insert_one(new_session)
            
            # Set session variables
            session['username'] = username
            session['session_id'] = session_id
            
            # Check if user has a stored token
            stored_token_doc = user_tokens_collection.find_one({
                'username': username
            })
            
            if stored_token_doc and 'token' in stored_token_doc:
                # Verify if the stored token is valid
                token_expired = False
                token_expiry_date = None
                
                if use_mongodb:
                    token_doc = tokens_collection.find_one({'token': stored_token_doc['token']})
                    is_valid = token_doc and token_doc.get('token_expiration', datetime.datetime.min) > datetime.datetime.now()
                    
                    if token_doc and not is_valid:
                        token_expired = True
                        token_expiry_date = token_doc.get('token_expiration')
                
                    if is_valid:
                        # Token is valid, add to session
                        session['token'] = stored_token_doc['token']
                    elif token_expired:
                        # Token exists but expired, remove from user storage
                        user_tokens_collection.update_one(
                            {'username': username},
                            {'$unset': {'token': ""}}
                        )
                        
                        # Add flag to indicate token expiry to frontend
                        return jsonify({
                            'message': 'Login successful', 
                            'token_expired': True,
                            'expiry_date': token_expiry_date.isoformat() if token_expiry_date else None
                        }), 200
            
            return jsonify({'message': 'Login successful'}), 200
        
        return jsonify({'message': 'Invalid password'}), 401

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('home'))
        return render_template('signup.html')
    
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Check if username already exists
        if users_collection.find_one({'username': username}):
            return jsonify({'message': 'Username already exists'}), 400
        
        # Check if email already exists
        if users_collection.find_one({'email': email}):
            return jsonify({'message': 'Email already exists'}), 400
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        user = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        
        users_collection.insert_one(user)
        
        return jsonify({'message': 'User created successfully'}), 201

@auth.route('/logout')
def logout():
    if 'username' in session and 'session_id' in session:
        # Mark the current session as inactive
        sessions_collection.update_one(
            {'username': session['username'], 'session_id': session['session_id']},
            {'$set': {'active': False, 'ended_at': datetime.datetime.now()}}
        )
    
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/validate-token', methods=['POST'])
@login_required
def validate_token():
    """Validate if a user has an active token"""
    token = session.get('token')
    
    if not token:
        return jsonify({'has_token': False}), 200
    
    # Check if token exists and is valid
    if use_mongodb:
        user_doc = tokens_collection.find_one({'token': token})
        is_valid = user_doc and user_doc.get('token_expiration', datetime.datetime.min) > datetime.datetime.now()
        
        if is_valid:
            expires_at = user_doc.get('token_expiration')
            return jsonify({
                'has_token': True,
                'expires_at': expires_at.isoformat() if expires_at else None
            }), 200
    else:
        user_doc = memory_tokens.get(token)
        is_valid = user_doc and user_doc.get('token_expiration', datetime.datetime.min) > datetime.datetime.now()
        
        if is_valid:
            expires_at = user_doc.get('token_expiration')
            return jsonify({
                'has_token': True,
                'expires_at': expires_at.isoformat() if expires_at else None
            }), 200
    
    # Token not found or expired, remove from session
    if 'token' in session:
        session.pop('token')
        
        # Also remove from user storage if it exists
        if 'username' in session:
            user_tokens_collection.update_one(
                {'username': session['username']},
                {'$unset': {'token': ""}}
            )
    
    return jsonify({'has_token': False}), 200

@auth.route('/external-token', methods=['GET'])
def get_external_token_page():
    """Page for external token acquisition"""
    return render_template('get_token.html')

@auth.route('/token-login', methods=['POST'])
@login_required
def token_login():
    """Verify an external token from the Telegram bot"""
    token = request.form.get('token')
    username = session.get('username')
    
    if not token:
        return render_template('get_token.html', error='Please enter a token')
    
    if not username:
        return redirect(url_for('auth.login'))
    
    # Check if token exists and is valid
    if use_mongodb:
        user_doc = tokens_collection.find_one({'token': token})
        is_valid = user_doc and user_doc.get('token_expiration', datetime.datetime.min) > datetime.datetime.now()
    else:
        user_doc = memory_tokens.get(token)
        is_valid = user_doc and user_doc.get('token_expiration', datetime.datetime.min) > datetime.datetime.now()
    
    if is_valid:
        # Store the token in the session
        session['token'] = token
        
        # Store the token in the user's account
        user_tokens_collection.update_one(
            {'username': username},
            {'$set': {
                'username': username,
                'token': token,
                'updated_at': datetime.datetime.now()
            }},
            upsert=True
        )
        
        return redirect(url_for('home'))
    else:
        return render_template('get_token.html', error='Invalid or expired token. Please get a new token from Telegram bot.')

@auth.route('/clear-token', methods=['POST'])
@login_required
def clear_token():
    """Clear the stored token for a user"""
    username = session.get('username')
    
    if not username:
        return jsonify({'message': 'Not authenticated'}), 401
    
    # Remove token from session
    if 'token' in session:
        session.pop('token')
    
    # Remove token from user storage
    user_tokens_collection.update_one(
        {'username': username},
        {'$unset': {'token': ""}}
    )
    
    return jsonify({'message': 'Token cleared successfully'}), 200 