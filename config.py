import os
from flask import Flask

face = Flask(__name__)
face.config['SECRET_KEY'] = 'MyKey'
basedir = os.path.abspath(os.path.dirname(__file__))
