from flask import request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity, create_access_token)

from models import db, User

from flask import Blueprint

auth_route = Blueprint('authorization',__name__)

jwt = JWTManager()

# initializing the flask-jwt extensionto use jwt functionality
def init_jwt(app):
    jwt.init_app(app)
    #this secret key will be used to encode-decode and generate tokens
    #can be used to sign tokens with user identity, and verify them later. 
    #This same key will be used to unhash the token and decode it when received
    app.config['SECRET_KEY'] = 'secret_key'


def user_loader_callback(identity):
    return User.query.filter_by(username=identity).first()

def unauthorized_loader_callback(error):
    return jsonify({
        'message': 'Unauthorized access'
    }), 401

@auth_route.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']

    user = User.query.filter_by(username = username).first()
    if user:
        return jsonify({
            'message':'Username exists'
        }),400
    
    new_user = User(username=username, password = password, role=role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': f'{new_user.username} registered successfully',
    }), 201


@auth_route.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if not user or user.password!= password: 
        return jsonify({
            'message': 'Invalid username or password'
        }), 401
    

    access_token = create_access_token(identity=user.username)
    return jsonify({
        'access_token': access_token
    }), 200


