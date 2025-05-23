from flask import Flask

app = Flask(__name__)

from app.models import *


from app.routes import *
