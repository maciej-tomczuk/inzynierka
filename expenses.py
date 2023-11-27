from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import date
import os

app = Flask(__name__)
db_name = 'expenses.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hashed = db.Column(db.String(120), nullable=False)
    name = db.Column(db.Text, nullable=False)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today())

    @classmethod
    def create(cls, username, password, name):
        user = cls(username=username, password_hashed=password,name=name)
        db.session.add(user)
        db.session.commit()
        return 


@app.route('/')
def hello():
    user = User.create('wiaderekcsij', 'niczy', 'jolxd')
    return 'Hello, World!'

@app.route('/show')
def show():
    users = User.query.all()
    user_list = '\n'.join([f'Username: {user.username}, Name: {user.name}' for user in users])
    return f'{user_list}'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)