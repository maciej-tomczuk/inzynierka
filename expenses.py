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
                "amount": self.amount,
                "date": self.date,
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
    data = request.get_json()
    username = data.get('username')
    password = data.get('password_hashed')

    user = User.query.filter_by(username=username).first()
    if user and password == user.password_hashed:
        return user.serialize(), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['GET'])
def get_users():
    users_list = []
    users = User.query.all()
    for user in users:
        users_list.append(user.serialize())
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
        user =  User.query.filter_by(username=username).first()
        return user.serialize()
    else:
        return jsonify({'error':'Invalid credentials'}), 401

@app.route('/user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    data = request.json
    password_hashed = data.get('password_hashed')
    name = data.get('name')
    user = User.query.get(user_id)

    if user:
        user.password_hashed = password_hashed
        user.name = name
        print(user)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 401
    
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/group', methods=['GET'])
def get_groups():
    group_list = []
    groups = Group.query.all()
    for group in groups:
            group_list.append(group.serialize())
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
    
@app.route('/group/<int:group_id>', methods=['POST'])
def update_group(group_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    group = Group.query.get(group_id)

    if group:
        group.name = name
        group.description = description
        db.session.commit()
        return jsonify({'message': 'Group updated successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 401
    
@app.route('/group/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    Group.query.filter(Group.id == group_id).delete()
    GroupMember.query.filter_by(group_id=group_id).delete()
    db.session.commit()
    return jsonify({'message': 'Group deleted successfully'})
    
@app.route('/member/<int:group_id>', methods=['GET'])
def get_members(group_id):
    member_list = []
    members = GroupMember.query.filter_by(group_id=group_id).all()
    for member in members:
            member_list.append(member.serialize())
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

@app.route('/member/<int:member_id>', methods=['POST'])
def update_member(member_id):
    data = request.json
    role = data.get('role')
    member = GroupMember.query.get(member_id)

    if member:
        member.name = role
        db.session.commit()
        return jsonify({'message': 'Group member updated successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 401
    
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    GroupMember.query.filter(GroupMember.id == member_id).delete()
    db.session.commit()
    return jsonify({'message': 'Member removed from group successfully'})

@app.route('/expense', methods=['GET'])
def get_expenses():
    expense_list = []
    expenses = Expense.query.all()
    for expense in expenses:
            expense_list.append(expense.serialize())
    return jsonify(expense_list)

@app.route('/expense/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    expense = Expense.query.get(expense_id)
    return jsonify(expense.serialize())

@app.route('/expense/g/<int:group_id>', methods=['GET'])
def get_expense_by_group(group_id):
    expense_list = []
    expenses = Expense.query.filter_by(group_id = group_id)
    for expense in expenses:
            expense_list.append(expense.serialize())
    return jsonify(expense_list)


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
    
@app.route('/expense/<int:expense_id>', methods=['POST'])
def update_expense(expense_id):
    data = request.json
    amount = data.get('amount')
    description = data.get('description')
    expense = Expense.query.get(expense_id)

    if expense:
        expense.amount = amount
        expense.description = description
        db.session.commit()
        return jsonify({'message': 'Expense updated successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 401
    
@app.route('/expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    Expense.query.filter(Expense.id == expense_id).delete()
    ExpenseShare.query.filter_by(expense_id=expense_id).delete()
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'})
    
@app.route('/share/<int:expense_id>', methods=['GET'])
def get_shares(expense_id):
    share_list = []
    shares = ExpenseShare.query.filter_by(expense_id=expense_id).all()
    for share in shares:
            share_list.append(share.serialize())
    return json.dumps(share_list)

@app.route('/share/u/<int:user_id>', methods=['GET'])
def get_shares_by_user(user_id):
    share_list = []
    shares = ExpenseShare.query.filter_by(user_id=user_id).all()
    for share in shares:
            share_list.append(share.serialize())
    return json.dumps(share_list)

@app.route('/share', methods=['POST'])
def add_share():
    data = request.json
    user_id = data.get('user_id')
    expense_id = data.get('expense_id')
    share = data.get('share')
    shareobj = ExpenseShare.create(expense_id, user_id, share)

    if not User.query.get(user_id):
        return jsonify({'error':'User does not exist'}), 404
    if not Expense.query.get(expense_id):
        return jsonify({'error':'Expense does not exist'}), 404
    if shareobj:
        db.session.add(shareobj)
        db.session.commit()
        return jsonify({'message': 'Share added successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 404
    
@app.route('/share/<int:share_id>', methods=['POST'])
def update_share(share_id):
    data = request.json
    share = data.get('share')
    shareobj = ExpenseShare.query.get(share_id)

    if shareobj:
        shareobj.share = share
        db.session.commit()
        return jsonify({'message': 'Share updated successfully'})
    else:
        return jsonify({'error':'Invalid credentials'}), 401
    
@app.route('/share/<int:share_id>', methods=['DELETE'])
def delete_share(share_id):
    ExpenseShare.query.filter(ExpenseShare.id == share_id).delete()
    db.session.commit()
    return jsonify({'message': 'User removed from expense successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)