from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     def __repr__(self):
#         return '<Person %r>' % self.username
#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Employee %r>' % self.full_name
    
    def serialize(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
            "password": self.password,
            "id": self.id
        }