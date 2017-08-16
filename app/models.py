# app/models.py
"""This is a representation of a table in a database"""

from app import db


class User(db.Model):
    """This class represents the user table."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))


    def __init__(self, email, password):
        """initialization"""
        self.email = email
        self.password = password

    def save(self):
        """Adds a new user to the database """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Gets all users in a single query """
        return User.query.all()

    def delete(self):
        """Deletes an existing user from the database """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Represents the object instance of the model whenever it queries"""
        return "<Bucketlist: {}>".format(self.email)


class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    #Should always be plural
    __tablename__ = 'bucketlists'

    bucket_id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255))
    intro = db.Column(db.String(255))
    # FOREIGN KEY (user_id)
    # REFERENCES Users(user_id)
    # ON DELETE CASCADE

    def __init__(self, title, intro):
        """initialization."""
        self.title = title
        self.intro = intro

    def save(self):
        """Adds a new bucketlist to the database """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Gets all bucketlists in a single query """
        return Bucketlist.query.all()

    def delete(self):
        """Deletes an existing bucketlist from the database """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Represents the object instance of the model whenever it queries"""
        return "<Bucketlist: {}>".format(self.name)


class Item(db.Model):
    """This class represents the bucketlist item table."""

    #Should always be plural
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)

    item_name = db.Column(db.String(255))
    # FOREIGN KEY (bucket_id)
    # REFERENCES Bucketlist(bucket_id)
    # ON DELETE CASCADE

    def __init__(self, item_name):
        """initialization."""
        self.item_name = item_name

    def save(self):
        """Adds a new bucketlist item to the database """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Gets all bucketlist items in a single query """
        return Item.query.all()

    def delete(self):
        """Deletes an existing bucketlist item from the database """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Represents the object instance of the model whenever it queries"""
        return "<Bucketlist: {}>".format(self.name)
