from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Thought {self.id}>"

@app.route('/')
def index():
    thoughts = Thought.query.order_by(Thought.date_created).all()
    random.shuffle(thoughts)
    return render_template('index.html', thoughts=thoughts)

@app.route('/new', methods=['POST'])
def new():
    if request.method == "POST":
        thought = request.form['thought']
        new_thought = Thought(content=thought)

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
