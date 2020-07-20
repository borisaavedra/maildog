from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

db = SQLAlchemy()

usersemails = db.Table("usersemails",
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("email_id", db.Integer, db.ForeignKey("emails.id"), primary_key=True)
)


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    emails = db.relationship('Emails', backref='users', lazy=True)
    templates = db.relationship('Templates', backref='users', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


emailstypes = db.Table("emailstypes",
    db.Column("emails_id", db.Integer, db.ForeignKey("emails.id"), primary_key=True),
    db.Column("types_id", db.Integer, db.ForeignKey("types.id"), primary_key=True)
)


class Templates(db.Model):
    __tablename__ = "templates"
    id = db.Column(db.Integer, primary_key=True)
    template = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)


class Emails(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)

    def __repr__(self):
        return f"<Email {self.email}>"


class Types(db.Model):
    __tablename__ = "types"
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100), nullable=False, default=(1, 2, 3))


class Codes(db.Model):
    __tablename__ = "codes"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    