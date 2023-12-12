import flask
import importlib
import os

from utils.config import Config

app = flask.Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)
Config.check()


from flask import Flask, request,render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')




    return render_template('register.html')

# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         user = User.query.filter_by(email=email).first()
        
#         if user and user.check_password(password):
#             session['email'] = user.email
#             return redirect('/dashboard')
#         else:
#             return render_template('login.html',error='Invalid user')

#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     if session['email']:
#         user = User.query.filter_by(email=session['email']).first()
#         return render_template('dashboard.html',user=user)
    

# @blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Handle registration
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']

#         # Assuming you have a User model with attributes 'name', 'email', and 'password'
#         new_user = User(name=name, email=email, password=password)

#         # Add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()

#         return redirect('/login')

#     # If the request method is GET, render the registration form
#     return flask.render_template('register.html')  

for route_file in os.listdir("routes"):
    if route_file.endswith(".py"):
        lib = importlib.import_module(f"routes.{route_file[:-3]}")
        app.register_blueprint(lib.blueprint)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5800)
