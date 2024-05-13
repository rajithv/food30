from app import db
from app import db

# Association table for the many-to-many relationship
user_food = db.Table('user_food',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('food_id', db.Integer, db.ForeignKey('foods.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    foods = db.relationship('Food', secondary=user_food, backref=db.backref('users', lazy=True), lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name


class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Food %r>' % self.name
