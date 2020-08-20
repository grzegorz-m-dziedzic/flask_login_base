from app import app, db
from models import User
from flask import jsonify, request, redirect, url_for
from flask_login import login_user, login_required, logout_user


@app.route('/', methods=['GET'])
def index():
    return 'it works', 200


@app.route('/users', methods=['GET'])
def users():
    return jsonify([u.to_json() for u in User.query.all()]), 200


@app.route('/register', methods=['POST'])
def register():
    content = request.json
    username = content['username']
    email = content['email']
    password = content['password']

    user = User.query.filter_by(username=username).first()
    if user:
        return 'Already exists', 200
    else:
        user = User(username=username, email=email, password_hash=User.hash_password(password))
        db.session.add(user)
        db.session.commit()
        return 'User registered', 200


@app.route('/login', methods=['POST'])
def login():
    content = request.json
    username = content['username']
    password = content['password']
    user = User.query.filter_by(username=username).first()
    if user:
        if user.verify_password(password):
            login_user(user)
            return 'Logged in', 200
    return 'Wrong data', 200


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return 'Logged out', 200


@app.route('/private', methods=['GET'])
@login_required
def private():
    return 'User is logged in'
