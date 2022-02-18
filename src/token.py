from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Token, db


token = Blueprint("token",__name__,url_prefix="/api/v1/token")

@token.route("/",methods=['POST','GET'])
@jwt_required()
def handle_token():
    '''POST a new token or GET all token from user.'''
    current_user = get_jwt_identity()
    
    if request.method == 'POST':
        symbol = request.get_json().get("symbol","")
        contract = request.get_json().get("contract","")
        chain = request.get_json().get("chain","")
        
        # Validation Start
        # Symbol validation
        if not symbol or type(symbol) is not str or " " in symbol:
            return jsonify({
                "error": "invalid symbol"
            }), HTTP_400_BAD_REQUEST
        
        elif len(symbol) > 6:
            return jsonify({
                "error": "symbol too long"
            }), HTTP_400_BAD_REQUEST
        
        elif Token.query.filter_by(symbol=symbol.lower(),user_id=current_user,status=1).first():
            return jsonify({
                "error": "symbol already exists"
            }), HTTP_409_CONFLICT
        
        # Contract validation
        if not contract or type(contract) is not str:
            return jsonify({
                "error": "invalid contract"
            }), HTTP_400_BAD_REQUEST
              
        elif len(contract) > 99:
            return jsonify({
                "error": "contract too long"
            }), HTTP_400_BAD_REQUEST
            
        elif Token.query.filter_by(contract=contract,user_id=current_user,status=1).first():
            return jsonify({
                "error": "contract already exists"
            }), HTTP_409_CONFLICT
        
        # Chain validation
        if not chain or type(chain) is not str:
            return jsonify({
                "error": "invalid chain"
            }), HTTP_400_BAD_REQUEST
              
        elif len(chain) > 6:
            return jsonify({
                "error": "chain too long"
            }), HTTP_400_BAD_REQUEST
    
        #Validation End
            
        token = Token(symbol=symbol.lower(), contract=contract, chain=chain.lower(), user_id=current_user)
        db.session.add(token)
        db.session.commit()
        
        return jsonify({
            "id": token.id,
            "symbol": token.symbol,
            "contract": token.contract,
            "chain": token.chain,
            "user_id": token.user_id,
            "created_at": token.created_at,
            "updated_at": token.updated_at
        }),HTTP_201_CREATED
    
    else: 
        # Pagination meta info
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5,type=int)
        
        tokens = Token.query.filter_by(user_id=current_user,status=1).paginate(page=page,per_page=per_page)
        
        data = []
        
        for token in tokens.items:
            data.append({
               "id": token.id,
                "symbol": token.symbol,
                "contract": token.contract,
                "chain": token.chain,
                "user_id": token.user_id,
                "status": token.status,
                "created_at": token.created_at,
                "updated_at": token.updated_at 
            })
            
        meta = {
            "page": tokens.page,
            "pages": tokens.pages,
            "total_count": tokens.total,
            "prev_page": tokens.prev_num,
            "next_page": tokens.next_num,
            "has_next": tokens.has_next,
            "has_prev": tokens.has_prev,
        }
        
        return jsonify({"data":data, "meta":meta}), HTTP_200_OK
    

@token.get("/<string:symbol>")
@jwt_required()
def get_token(symbol):
    '''Get a specific token.'''
    current_user = get_jwt_identity()
    
    token = Token.query.filter_by(user_id=current_user,symbol=symbol.lower(),status=1).first()
    
    if not token:
        return jsonify({"message": "Token not found"}), HTTP_404_NOT_FOUND
    
    return jsonify({
        "id": token.id,
        "symbol": token.symbol,
        "contract": token.contract,
        "chain": token.chain,
        "user_id": token.user_id,
        "status": token.status,
        "created_at": token.created_at,
        "updated_at": token.updated_at
    }), HTTP_200_OK
    

@token.delete("/<string:symbol>")
@jwt_required()
def delete_token(symbol):
    '''Delete a token. Change status to false.'''
    current_user = get_jwt_identity()
    
    token = Token.query.filter_by(user_id=current_user,symbol=symbol.lower(),status=1).first()
    
    if not token:
        return jsonify({"error": "Token not found"}), HTTP_404_NOT_FOUND
    
    token.status = 0
    db.session.commit()
    
    return jsonify({"message": f"{symbol} deleted"}), HTTP_200_OK


@token.put("/<string:symbol>")
@token.patch("/<string:symbol>")
@jwt_required()
def edit_token(symbol): 
    '''Edit a token.'''
    current_user = get_jwt_identity()
    
    token = Token.query.filter_by(user_id=current_user,symbol=symbol.lower(),status=1).first()
    
    if not token:
        return jsonify({"error": "Token not found"}), HTTP_404_NOT_FOUND

    new_symbol = request.get_json().get("symbol","")
    new_contract = request.get_json().get("contract","")
    new_chain = request.get_json().get("chain","")
    
    # Validation Start
    # Symbol validation
    if not new_symbol:
        pass
        
    elif type(new_symbol) is not str or " " in new_symbol:
        return jsonify({
            "error": "invalid symbol"
        }), HTTP_400_BAD_REQUEST
    
    elif len(new_symbol) > 6:
        return jsonify({
            "error": "symbol too long"
        }), HTTP_400_BAD_REQUEST
    
    elif Token.query.filter_by(symbol=new_symbol.lower(),user_id=current_user,status=1).first():
        return jsonify({
            "error": "symbol already exists"
        }), HTTP_409_CONFLICT
        
    else:
        token.symbol = new_symbol.lower()
    
    # Contract validation
    if not new_contract:
        pass
    
    elif type(new_contract) is not str:
        return jsonify({
            "error": "invalid contract"
        }), HTTP_400_BAD_REQUEST
            
    elif len(new_contract) > 99:
        return jsonify({
            "error": "contract too long"
        }), HTTP_400_BAD_REQUEST
        
    elif Token.query.filter_by(contract=new_contract,user_id=current_user,status=1).first():
        return jsonify({
            "error": "contract already exists"
        }), HTTP_409_CONFLICT
        
    else:
        token.contract = new_contract
    
    # Chain validation
    if not new_chain:
        pass
    
    elif type(new_chain) is not str:
        return jsonify({
            "error": "invalid chain"
        }), HTTP_400_BAD_REQUEST
            
    elif len(new_chain) > 6:
        return jsonify({
            "error": "chain too long"
        }), HTTP_400_BAD_REQUEST
        
    else:
        token.chain = new_chain

    #Validation End
    
    db.session.commit()
    
    return jsonify({
            "id": token.id,
            "symbol": token.symbol,
            "contract": token.contract,
            "chain": token.chain,
            "created_at": token.created_at,
            "updated_at": token.updated_at
        }),HTTP_200_OK
    
    
@token.get('/all')
@jwt_required()
def get_all_token():
    '''Get tokens from all users.'''  
    tokens = Token.query.filter_by(status=1)
    
    data = []
    
    for token in tokens:
        data.append({
            "id": token.id,
            "symbol": token.symbol,
            "contract": token.contract,
            "chain": token.chain,
            "user_id": token.user_id,
            "status": token.status,
            "created_at": token.created_at,
            "updated_at": token.updated_at 
        })
            
    return jsonify({"data":data}), HTTP_200_OK