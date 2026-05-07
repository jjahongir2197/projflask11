from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'

db = SQLAlchemy(app)

# ================= MODEL =================

class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return self.username

# ================= ROUTES =================

@app.route('/')
def home():

    messages = Message.query.order_by(
        Message.created_at.desc()
    ).all()

    return render_template(
        'chat.html',
        messages=messages
    )

@app.route('/send', methods=['POST'])
def send_message():

    username = request.form['username']
    text = request.form['text']

    message = Message(
        username=username,
        text=text
    )

    db.session.add(message)
    db.session.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete_message(id):

    message = Message.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    return redirect('/')

# ================= MAIN =================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
