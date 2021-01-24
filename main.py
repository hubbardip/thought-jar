from flask import Flask, request, redirect, render_template, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    thoughts = db.relationship('Thought', backref='user', lazy=True)

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Thought {self.id}>"

@app.route('/')
def index():
    thoughts = Thought.query.order_by(Thought.date_created).all()
    random.shuffle(thoughts)
    return render_template('index.html', thoughts=thoughts)

@app.route('signup', methods=['POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user is None:
            try:
                new_user = User(username=username,password=request.form['password'])
                db.session.add(new_user)
                db.session.commit()
                session['user']=new_user
                return redirect('/')
            except:
                return 'Error adding user.'
        else:
            error = 'Duplicate Username.'
    return render_template('signup.html', error=error)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user is None:
            if user.password == session['password']:
                session['logged_in'] = True
                session['user'] = user
                return redirect(url_for('index'))
            else:
                error = 'Invalid password.'
        else:
            error = 'Invalid username.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session['logged_in']=False
    return redirect(url_for('index'))

@app.route('/new', methods=['POST'])
def new():
    if request.method == "POST":
        thought = request.form['thought']
        new_thought = Thought(content=thought,user=session['user'])

        try:
            db.session.add(new_thought)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding thought'

@app.route('/show')
def view_all():
    thoughts = Thought.query.order_by(Thought.date_created).all()
    return render_template('show.html', thoughts=thoughts)

@app.route("/delete/<int:id>")
def delete(id):
    to_delete = Thought.query.get_or_404(id)

    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Error deleting thought"


if __name__ == "__main__":
    app.run(debug=True)
