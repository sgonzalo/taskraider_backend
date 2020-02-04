from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Login %r>' % self.username
    def serialize(self):
        return {
            "email": self.email,
            "password": self.password
        }

class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Signup %r>' % self.username
    def serialize(self):
        return {
            "email": self.email,
            "password": self.password
        }

class User(db.Model):
    __tablename__= "user"
    profile = relationship("UserProfile")
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.full_name
    
    def serialize(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
            "password": self.password,
            "id": self.id
        }

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.String(250), unique=False, nullable=False)
    contact_info = db.Column(db.String(250), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return '<UserProfile %r>' % self.full_name
    
    def serialize(self):
        return {
            "skills": self.skills,
            "contact_info": self.contact_info,
            "work_history": self.contact_info,
            "id": self.id
        }
        
class Company(db.Model):
    __tablename__= "comapny"
    id = db.Column(db.Integer, primary_key=True)
    #profile = db.relationship("CompanyProfile")
    full_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Company %r>' % self.full_name
    
    def serialize(self):
        return {
            "full_name": self.full_name,
            "email": self.email,
            #"profile": self.profile.serialize() if self.profile is not None else None,
            "password": self.password,
            "id": self.id 
        }

class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_info = db.Column(db.String(500), unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'))

    def __repr__(self):
        return '<CompanyProfile %r>' % self.full_name
    
    def serialize(self):
        return {
            "company_info": self.skills,
            "id": self.id
        }

# class JobPosting(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     job_title = db.Column(db.String(250), unique=True, nullable=False)
#     job_description= db.Column(db.String(500), unique=True, nullable=False)
#     zip_code = db.Column(db.String(5), unique=True, nullable=False)
#     job_date = db.Column(db.String(10), unique=True, nullable=False)
#     skills_needed = db.Column(db.String(500), unique=True, nullable=False)
#     hours_expected = db.Column(db.String(50), unique=True, nullable=False)
#     payment = db.Column(db.String(250), unique=True, nullable=False)
#     employer_id = Column(Integer, ForeignKey('jobposting.id'))
#     #createjobposting_id = Column(Integer, ForeignKey('createjobposting.id'))

#     def __repr__(self):
#         return '<JobPosting %r>' % self.full_name
    
#     def serialize(self):
#         return {
#             "job_title": self.job_title,
#             "job_description": self.job_description,
#             "zip_code": self.zip_code,
#             "job_date": self.job_date,
#             "skills_needed": self.skills_needed,
#             "hours_expected": self.hours_expected,
#             "payment": self.payment,
#             "id": self.id
#         }


