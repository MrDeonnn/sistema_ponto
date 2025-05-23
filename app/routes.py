from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, current_user, login_user, logout_user
from app.models import Usuarios
from app import app

@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("index.html", user=current_user)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        senha = request.form.get("senha")

        Usuario = Usuarios.query.filter_by(email=email).first()
        if Usuario and Usuario.senha == senha:
            login_user(Usuario)
            return redirect(url_for("home"))
        else:
            return render_template("loginn.html", error="Email ou senha incorretos.")
    return render_template("loginn.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
