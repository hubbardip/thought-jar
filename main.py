from flask import Flask, request, redirect, render_template, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Thought {self.id}>"

@app.route('login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password.'
    return render_template('login.html', error=error)

@app.route('/')
def index():
    thoughts = Thought.query.order_by(Thought.date_created).all()
    return render_template('index.html', thoughts=thoughts)

@app.route('/new', methods=['POST'])
def new():
    if request.method == "POST":
        thought = request.form['name']
        new_thought = Thought(content=thought)

        try:
            db.session.add(new_thought)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding thought'

@app.route('/viewall', methods=['GET'])
def view_all():
    thoughts = Thought.query.order_by(Thought.date_created).all()
    return render_template('all_thoughts.html', thoughts=thoughts)

@app.route('/getrandom', methods=['GET'])
def get_random():
    rand = random.randrange(0, Thought.query(Thought).count()) 
    thought = Thought.query(Thought)[rand].content
    return render_template('random_thought.html', content = thought)

if __name__ == "__main__":
    app.run()
