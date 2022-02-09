from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    token = db.relationship('Token', backref="user")
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    
    def __repr__(self) -> str:
        return 'User>>> {self.username}'
    
    
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(6), nullable=False)
    price = db.Column(db.BigInteger, nullable=False)
    contract = db.Column(db.String(99), nullable=False)
    chain = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Boolean, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    token_update = db.relationship('Token_Price_Update', backref="token")
    
    def __repr__(self) -> str:
        return 'Token>>> {self.symbol}'
        
    
class Token_Price_Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.BigInteger, nullable=False)
    token_id = db.Column(db.Integer, db.ForeignKey('token.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    def __repr__(self) -> str:
        return 'Token_Price>>> {self.id}'