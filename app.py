from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, current_user
from blueprints.models import db, users
from blueprints.auth import auth as auth_blueprint 
import os, base64
from datetime import datetime
import humanize
import random


app = Flask(__name__)
folderPath = os.path.dirname(os.path.abspath(__file__))
app.config["FOLDER_PATH"] = folderPath
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + folderPath + "/master.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
   return users.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    emit('message', message, broadcast=True)


app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    socketio.run(app)