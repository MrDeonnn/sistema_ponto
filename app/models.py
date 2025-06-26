from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Usuarios(UserMixin, db.Model): #Tabela dos Usuários
    id = db.Column(db.Integer, primary_key=True)    
    nome = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)  
    senha = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))


with app.app_context():
    db.create_all()



