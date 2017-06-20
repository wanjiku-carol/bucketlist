import jwt
from flask import current_app
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

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
        "initialize user table with username, email, and password"
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """Checks the password against it's
        hash to validates the user's password"""
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save user to database"""
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generates the access token"""
        try:
            # create payload that expires after 5 minutes
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=180),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create byte string token using payload and SECRET key

            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            # return an error in string format if an erro occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the authorization header"""
        try:
            # try to decode token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # return an error message when the token is expired
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # return error message when token is invalid
            return "Invalid token. Please register or login"


class BucketList(db.Model):
    """create the bucket list table"""
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    items = db.relationship(
        'BucketlistItems', order_by='BucketlistItems.id',
        cascade="all, delete-orphan")

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


class BucketlistItems(db.Model):
    """create bucketlist item table"""
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))

    def __init__(self, name, done, bucketlist_id):
        self.name = name
        self.done = done
        self.bucketlist_id = bucketlist_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(bucketlist_id):
        """get all items in a bucketlist"""
        return BucketlistItems.query.filter_by(bucketlist_id=bucketlist_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """the object instance of the model whenever it queries"""
        return "<Item: {}".format(self.name)
