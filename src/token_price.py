from tokenize import Token
from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_200_OK, HTTP_409_CONFLICT
from flask_jwt_extended import jwt_required
from src.database import Token_Price_Update, db


token_price = Blueprint("token_price_update",__name__,url_prefix="/api/v1/token/update")

@token_price.post("/<int:token_id>")
@jwt_required()
def handle_token(token_id):
    '''Saves the latest price of a token'''
    token_update = Token_Price_Update.query.filter_by(token_id=token_id).first()
    price = request.get_json().get("price","")
    
    if token_update:
        return jsonify({
            "error": "token_id already exists"
        }), HTTP_409_CONFLICT
    
    #Price is stored as bigint. Move 5 decimal places to get real price
    token_price = Token_Price_Update(token_id=token_id,
                                     price=price)
        
    db.session.add(token_price)
    db.session.commit()
    
    return jsonify({
            "id": token_price.id,
            "price": token_price.price,
            "token_id": token_price.token_id,
            "created_at": token_price.created_at,
            "updated_at": token_price.updated_at
            }),HTTP_200_OK