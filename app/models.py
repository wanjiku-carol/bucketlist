from flask_bcrypt import Bcrypt

from app import db


class User(db.Model):
    """create the user table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    bucketlists = db.relationship(
        'BucketList', order_by='BucketList.id', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        "initialaize user table with username, email, and password"
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """Checks the password against it's
        hash to validates the user's password"""
        return Bcrypt().check_password_hash(self.password, password)


class BucketList(db.Model):
    """create the bucket list table"""
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, created_by):
        """initialize with name"""
        self.name = name
        self.created_by = created_by

    def save(self):
        """add new or update existing bucketlist to database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """get all bucketlists for a single user"""
        return BucketList.query.filter_by(created_by=user_id)

    def delete(self):
        """delete bucketlist from database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """the object instance of the model whenever it queries"""
        return "<BucketList: {}".format(self.name)
