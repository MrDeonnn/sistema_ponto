from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, current_user, login_user, logout_user
from app.models import Usuarios, db
from app import app

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("funcionario"))
    else:
        return redirect(url_for("login"))               

@app.route("/funcionario")
def funcionario():
    if current_user.is_authenticated and current_user.admin:
        return redirect(url_for("admin"))

    if current_user.is_authenticated:
        return render_template("index.html", user=current_user)
    else:
        return redirect(url_for("login"))

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated and current_user.admin:
        if request.method == 'POST':
            nome = request.form.get("nome")
            email = request.form.get("email")
            senha = request.form.get("senha")
            admin = request.form.get("admin")

            if request.form.get("admin"):
                admin = True
            else:
                admin = False

            # Verifica se o usuário já existe
            if Usuarios.query.filter_by(email=email).first():
                return render_template("admin.html", user=current_user, error="Usuário já existe.")

            
            # Verifica se a Senha é Válida
            if len(senha) < 6:
                return render_template("admin.html", user=current_user, error="A senha deve ter pelo menos 6 caracteres.")
            
            # Verifica se o nome é válido
            if len(nome) < 3:
                return render_template("admin.html", user=current_user, error="O nome deve ter pelo menos 3 caracteres.")

            novo_usuario = Usuarios(nome=nome, email=email, senha=senha, admin=admin)
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for("admin"))
        
        return render_template("admin.html", user=current_user)
    else:
        return redirect(url_for("home"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        senha = request.form.get("senha")

        Usuario = Usuarios.query.filter_by(email=email).first()
        if Usuario and Usuario.senha == senha:
            login_user(Usuario)
            return redirect(url_for("funcionario"))
        else:   
            return render_template("loginn.html", error="Email ou senha incorretos.")
    return render_template("loginn.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

