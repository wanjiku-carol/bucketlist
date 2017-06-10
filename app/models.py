from app import db


class BucketList(db.Model):
    """create the bucket list table"""
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name"""
        self.name = name

    def save(self):
        """add new bucket list to database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """get all bucketlists in a single querry"""
        return BucketList.query.all()

    def delete(self):
        """delete bucketlist from database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """the object instance of the model whenever it queries"""
        return "<BucketList: {}".format(self.name)


class Users(db.Model):
    """create the user table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(self):
        return Users.querry.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """the object instance of the model whenever it queries"""
        return "<Users: {}".format(self.username)
