from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))

class Calories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    item = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    is_below_target = db.Column(db.Boolean, default = False)
