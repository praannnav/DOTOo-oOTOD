from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class userdata(db.Model):

    username = db.Column(db.String(120))
    emailid = db.Column(db.String(200), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(200), nullable=False)

    todos = db.relationship('todo', backref='userdata', lazy=True)

class todo(db.Model):
    emaild=db.Column(db.String(200), db.ForeignKey('userdata.emailid'))
    taskId=db.Column(db.Integer(),primary_key=True)
    task=db.Column(db.String(200),nullable=False)
    time=db.Column(db.String(200),nullable=False)