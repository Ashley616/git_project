from mysqldb import *
from flask import Blueprint, json, request, render_template, session, flash, jsonify
from flask_jwt_extended import (create_access_token, current_user, jwt_required, JWTManager, create_refresh_token)
from mysqldb import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

JWT_EXPIRE_TIME = timedelta(minutes=30)
bp = Blueprint('user', __name__, url_defaults='')

''''
user part
'''


@bp.route('/register', methods=['GET','POST'])
def register():
    username = request.json['username']
    if username == '':
        return jsonify("username is required."), 400

    password = request.json['password']
    if password == "":
        return jsonify("password is required."), 400

    confirm_password = request.json['confirm_password']
    if confirm_password == '':
        return jsonify("confirm password is required."), 400

    email = request.json['email']
    if email == '':
        return jsonify("email is required."), 400

    role = request.json['role']
    if role == '':
        return jsonify("role is required."), 400

    if password != confirm_password:
        return jsonify("Different password"), 400

    if User.query.filter_by(name=username).first() is not None:
        return jsonify("User name is already exist"), 401

    if User.query.filter_by(email=email).first() is not None:
        return jsonify("Email has been registered."), 401

    user = User()
    user.name = username
    user.password = generate_password_hash(password)
    user.email = email
    user.role = role
    #user.role_id = 2
    db.session.add(user)
    db.session.commit()
    user = {"id": user.id, "name": user.name, "password": user.password,"email": user.email, "role": user.role}
    return jsonify(user),200


@bp.route('/login', methods=["POST"])
def login():
    email = request.json['username']
    password = request.json['password']

    if(email == '' or password ==''):
        return jsonify("invalid input"), 400

    user_in_db = User.query.filter_by(email=email).first()

    if (user_in_db is None) or not check_password_hash(user_in_db.password, password):
        return jsonify("invalid username or password"), 401

    user_in_db = {"id": user_in_db.id, "name": user_in_db.name, "password": user_in_db.password,
                   "email": user_in_db.email}

    return jsonify(user_in_db), 200


@bp.route('/reset', methods=['POST'])
def reset():
    email = request.json["email"]
    if email == '':
        return jsonify("email is required."), 400

    user_in_db = User.query.filter_by(email=email).first()

    if(user_in_db == None):
        return jsonify("email error."), 400

    password = request.json['password']
    if password == "":
        return jsonify("password is required."), 400

    c_password = request.json['c_password']
    if c_password == '':
        return jsonify("confirm password is required."), 400

    if password != c_password:
        return jsonify("Different password"), 400

    user_in_db.password = generate_password_hash(password)
    db.session.commit()

    user = {"id": user_in_db.id, "name": user_in_db.name, "password": user_in_db.password}
    return jsonify(user), 200


@bp.route('/myinfo', methods=['GET'])

@jwt_required()
def myinfo():
    userID = dict(current_user)["id"]
    info = User.query.filter_by(id=userID).first()
    return jsonify(info), 200
