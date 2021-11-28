from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), nullable=False)
    profilepic = db.Column(db.String(200))
    about = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    adm = db.Column(db.Boolean(), default=0)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    details = db.Column(db.TEXT)
    documents = db.Column(db.TEXT)
    tasks = db.Column(db.TEXT)
    photos = db.Column(db.TEXT)

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(200))
    location = db.Column(db.TEXT)
    documents = db.Column(db.TEXT)
    asname = db.Column(db.TEXT)
    picture = db.Column(db.TEXT)

