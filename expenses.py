from flask import Flask, request, jsonify
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
def start():
    return 'Expenses app'

@app.route('/login', methods=['POST'])
def login():
    data =request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and password == user.password:
        return jsonify({'user': username}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.__dict__ for user in users]})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.__dict__)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password_hashed = data.get('password_hashed')
    name = data.get('name')

    user = User.create(username, password_hashed, name)
    
    if user:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}, 401)

@app.route('/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    return jsonify({'groups': [group.__dict__ for group in groups]})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)