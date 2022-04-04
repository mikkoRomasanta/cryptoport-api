from audioop import cross
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from src.database import User, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_cors import cross_origin


auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    '''Register a new user.'''
    username=request.json.get('username','')
    password=request.json.get('password','')
    
    #Validation Start
    if len(password) < 6: #min password length
        return jsonify({"error": "password is too short"}), HTTP_400_BAD_REQUEST
        
    if len(username) < 3: #min username length
        return jsonify({"error": "username is too short"}), HTTP_400_BAD_REQUEST
    
    if " " in username: #no spaces in username
        return jsonify({"error": "invalid username"}), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "username already in use"}), HTTP_409_CONFLICT
    #Validation End
        
    pwd_hash=generate_password_hash(password)
    user = User(username=username,password=pwd_hash)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User created",
                    "user": {
                        "username" : username
                    }
                    }), HTTP_201_CREATED


@auth.post('/login')
@cross_origin()
def login():
    '''Login...'''
    username = request.json.get('username','')
    password = request.json.get('password','')
    
    user=User.query.filter_by(username=username).first()
    
    if user:
        is_pass_correct = check_password_hash(user.password,password)
        
        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)
            
            return jsonify({
                "user": {
                    "refresh": refresh,
                    "access": access,
                    "username": user.username
                }
            }), HTTP_200_OK
            
    return jsonify({"error": "Wrong credentials"}),HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
def me():
    '''Get current logged in user.'''
    user_id = get_jwt_identity()
    
    user = User.query.filter_by(id=user_id).first()
    
    return jsonify({
        "user": user.username
    }), HTTP_200_OK
    
    
@auth.post("/token/refresh")
@jwt_required(refresh=True)
def refresh_user_token():
    '''Refresh access token.'''
    user_id = get_jwt_identity()
    access = create_access_token(identity=user_id)
    
    return jsonify({
        "access": access
    }),HTTP_200_OK
    
    
#Add edit/delete function ?