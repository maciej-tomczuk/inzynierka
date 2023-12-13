from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy.sql import text, exists
from datetime import datetime as sysdate
import json

app = Flask(__name__)
db_name = 'expenses.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hashed = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    members = db.relationship('GroupMember', backref='user')
    expenses = db.relationship('Expense', backref='owner')
    share = db.relationship('ExpenseShare', backref='owed_by')

    @classmethod
    def create(cls, username, password, name):
        user = cls(username=username, password_hashed=password,name=name)
        return user
    
    def serialize(self):
        return {"id":  self.id,
                "username": self.username,
                "password_hashed": self.password_hashed,
                "name":  self.name}

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String(255))
    members = db.relationship('GroupMember', backref='group')
    expenses = db.relationship('Expense', backref='in_group')

    @classmethod
    def create(cls, group_name, description):
        group = cls(group_name=group_name, description=description)
        return group
    
    def serialize(self):
        return {"id":  self.id,
                "group_name": self.group_name,
                "description": self.description}

class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    role = db.Column(db.String(50))

    @classmethod
    def create(cls, user_id, group_id, role):
        member = cls(user_id=user_id, group_id=group_id, role=role)
        return member
    
    def serialize(self):
        return {"id":  self.id,
                "user_id": self.user_id,
                "group_id": self.group_id,
                "role": self.role}

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(255))
    shares = db.relationship('ExpenseShare', backref='expense')

    @classmethod
    def create(cls, user_id, group_id, amount, description):
        expense = cls(user_id=user_id, group_id=group_id, amount=amount, date=sysdate.today(), description=description)
        return expense
    
    def serialize(self):
        return {"id":  self.id,
                "user_id": self.user_id,
                "group_id": self.group_id,
                "amount": self.date,
                "date": self.date.isoformat(),
                "description": self.description}

class ExpenseShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    share = db.Column(db.Float, nullable=False)

    @classmethod
    def create(cls, expense_id, user_id, share):
        share = cls(expense_id=expense_id, user_id=user_id, share=share)
        return share
    
    def serialize(self):
        return {"id":  self.id,
                "expense_id": self.expense_id,
                "user_id": self.user_id,
                "share": self.share}

@app.route('/')
def start():
    return 'Expenses app'

@app.route('/login', methods=['POST'])
def login():
    data =request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and password == user.password_hashed:
        return jsonify({'user': username}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['GET'])
def get_users():
    users_list = []
    users = User.query.all()
    for user in users:
        users_list.append({
            'id' : user.id,
            'username' : user.username,
            'name' : user.name
        })
    return json.dumps(users_list)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize())

@app.route('/user', methods=['POST'])
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
        return jsonify({'error':'Invalid credentials'}), 401

@app.route('/group', methods=['GET'])
def get_groups():
    group_list = []
    groups = Group.query.all()
    for group in groups:
            group_list.append({
                'id' : group.id,
                'group_name' : group.group_name,
                'description' : group.description
            })
    return json.dumps(group_list)

@app.route('/group/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group = Group.query.get(group_id)
    return jsonify(group.serialize())

@app.route('/group', methods=['POST'])
def create_group():
    data = request.json
    group_name = data.get('group_name')
    description = data.get('description')
    group = Group.create(group_name, description)

    if group:
        db.session.add(group)
        db.session.commit()
        return jsonify({'message': 'Group created successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 401
    
@app.route('/member/<int:group_id>', methods=['GET'])
def get_members(group_id):
    member_list = []
    members = GroupMember.query.filter_by(group_id=group_id).all()
    for member in members:
            member_list.append({
                'id' : member.id,
                'user_name' : member.user.name,
                'role' : member.role
            })
    return json.dumps(member_list)

@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    user_id = data.get('user_id')
    group_id = data.get('group_id')
    role = data.get('role')
    member = GroupMember.create(user_id, group_id, role)

    if not User.query.get(user_id):
        return jsonify({'error':'User does not exist'}), 404
    if not Group.query.get(group_id):
        return jsonify({'error':'Group does not exist'}), 404
    if member:
        db.session.add(member)
        db.session.commit()
        return jsonify({'message': 'Member added successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 404
    
@app.route('/expense', methods=['GET'])
def get_expenses():
    expense_list = []
    expenses = Expense.query.all()
    for expense in expenses:
            expense_list.append({
                'id' : expense.id,
                'owner' : expense.owner.name,
                'group' : expense.in_group.group_name,
                'amount' : expense.amount,
                'description' : expense.description,
                'date' : expense.date.isoformat()
            })
    return json.dumps(expense_list)

@app.route('/expense/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    expense = Expense.query.get(expense_id)
    return jsonify(expense.serialize())

@app.route('/expense', methods=['POST'])
def create_expense():
    data = request.json
    user_id = data.get('user_id')
    group_id = data.get('group_id')
    amount = data.get('amount')
    description = data.get('description')
    expense = Expense.create(user_id, group_id, amount, description)
    
    if not User.query.get(user_id):
        return jsonify({'error':'User does not exist'}), 404
    if not Group.query.get(group_id):
        return jsonify({'error':'Group does not exist'}), 404
    if expense:
        db.session.add(expense)
        db.session.commit()
        return jsonify({'message': 'Expense created successfully'})
    else:
        return jsonify({'error':'Unexpected error'}), 401
    
@app.route('/share/<int:expense_id>', methods=['GET'])
def get_shares(expense_id):
    share_list = []
    shares = ExpenseShare.query.filter_by(expense_id=expense_id).all()
    for share in shares:
            share_list.append({
                'id' : share.id,
                'owed_by' : share.owed_by.name,
                'expense_id' : share.expense.id,
                'share' : share.share
            })
    return json.dumps(share_list)

@app.route('/share', methods=['POST'])
def add_share():
    data = request.json
    user_id = data.get('user_id')
    expense_id = data.get('expense_id')
    share = data.get('share')
    share = ExpenseShare.create(user_id, expense_id, share)

    if not User.query.get(user_id):
        return jsonify({'error':'User does not exist'}), 404
    if not Expense.query.get(expense_id):
        return jsonify({'error':'Expense does not exist'}), 404
    if share:
        db.session.add(share)
        db.session.commit()
        return jsonify({'message': 'Share added successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)