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
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hashed = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(32), nullable=False)

    @classmethod
    def create(cls, username, password, name):
        user = cls(username=username, password_hashed=password,name=name)
        db.session.add(user)
        db.session.commit()
        return 

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

    @classmethod
    def create(cls, group_name, description):
        group = cls(group_name=group_name, description=description)
        db.session.add(group)
        db.session.commit()
        return 

class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    role = db.Column(db.String(50))

    @classmethod
    def create(cls, user_id, group_id, role):
        member = cls(user_id=user_id, group_id=group_id, role=role)
        db.session.add(member)
        db.session.commit()
        return 

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(255))

    @classmethod
    def create(cls, user_id, amount, date, description):
        expense = cls(user_id=user_id, amount=amount, date=date, description=description)
        db.session.add(expense)
        db.session.commit()
        return 

class ExpenseShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    share = db.Column(db.Float, nullable=False)

    @classmethod
    def create(cls, expense_id, user_id, share):
        share = cls(expense_id=expense_id, user_id=user_id, share=share)
        db.session.add(share)
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