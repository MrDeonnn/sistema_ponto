from flask import Flask, render_template, request
from app import app

@app.route("/")
def login():
    return render_template("loginn.html")
