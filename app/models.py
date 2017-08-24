# app/models.py
"""This is a representation of a table in a database"""

import os
import re
import jwt
import datetime
from app import db
from flask import jsonify
from flask_bcrypt import Bcrypt


class User(db.Model):
    """This class represents the user table."""

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    bucketlists = db.relationship(
        'Bucketlist',
        backref='users',
        lazy='dynamic'
        )

    def __init__(self, email):
        """initialization"""
        self.email = email
        self.password = ''

    @staticmethod
    def validate_email(email):
        """Method validates an email"""
        address_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if address_matcher.match(email) else False

    def create_password(self, password):
        """Method generates a hashed password"""
        self.password = Bcrypt().generate_password_hash(password).decode()

    def validate_password(self, password):
        """Method confirms that password is correct"""
        return Bcrypt().check_password_hash(self.password, password)

    def gen_token(self):
        token = jwt.encode({
            'id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=30)
        }, os.getenv('SECRET'))
        return jsonify({'token': token.decode('UTF-8')})

    def save(self):
        """Adds a new user to the database """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """Gets all users in a single query """
        return User.query.all()

    def delete(self):
        """Deletes an existing user from the database """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Represents the object instance of the model whenever it queries"""
        return "<User: {}>".format(self.email)


class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    #Should always be plural
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    items = db.relationship(
        'Item',
        backref='bucketlists',
        lazy='dynamic',
        cascade="all,delete",
        )


    def __init__(self, title, user_id):
        """initialization."""
        self.title = title
        self.user_id = user_id


    # def save(self):
    #     """Adds a new bucketlist to the database """
    #     db.session.add(self)
    #     db.session.commit()

    # @staticmethod
    # def get_all(user_id):
    #     """Gets all bucketlists in a single query """
    #     return Bucketlist.query.all(user_id=user_id)

    # def delete(self):
    #     """Deletes an existing bucketlist from the database """
    #     db.session.delete(self)
    #     db.session.commit()

    # def __repr__(self):
    #     """Represents the object instance of the model whenever it queries"""
    #     return "<Bucketlist: {}>".format(self.title)


class Item(db.Model):
    """This class represents the bucketlist item table."""

    #Should always be plural
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, name, bucket_id):
        """initialization."""
        self.name = name
        self.bucket_id = bucket_id

    def save(self):
        """Adds a new bucketlist item to the database """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(bucket_id):
        """Gets all bucketlist items in a single query """
        return Item.query.all(bucket_id=bucket_id)

    def delete(self):
        """Deletes an existing bucketlist item from the database """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Represents the object instance of the model whenever it queries"""
        return "<Item: {}>".format(self.name)
