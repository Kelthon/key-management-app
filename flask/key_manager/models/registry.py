'''
    Model de resgistro de movimentação das chaves

    Resposavel

    O model dos registros possui os campos de id do registro, id do usuário,
    data de emprestimo, data de devolução, id da chave emprestada, informações
    de quem pegou a chave: nome, e-mail.
'''
from datetime import datetime
from key_manager.models import *

class Registry(db.Model):
    __tablename__ = 'registries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    key_loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    key_return_date = db.Column(db.DateTime, nullable=True)
    key_id = db.Column(db.Integer, db.ForeignKey('keys.id'), nullable=False)
    holder_name = db.Column(db.String(100), nullable=False)
    holder_email = db.Column(db.String(100), nullable=True)
    
    def __repr__(self) -> str:
        return '<Registry %r>' % self.date
    