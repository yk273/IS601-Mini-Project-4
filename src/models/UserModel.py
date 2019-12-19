# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime
from . import db

class UserModel(db.Model):
    """
    User Model
    """

    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    def __repr(self):
        return '<id {}>'.format(self.id)

    # src/models/UserModel.py
    #####################
    # existing code remain #
    ######################
    from ..app import bcrypt  # add this line

    class UserModel(db.Model):
        """
        User Model
        """

        # table name
        __tablename__ = 'users'

        id = db.Column(db.Integer, primary_key=True)
        blogposts = db.relationship('BlogpostModel', backref='users', lazy=True)

        #####################
        # existing code remain #
        ######################

        # class constructor
        def __init__(self, data):
            """
            Class constructor
            """
            self.name = data.get('name')
            self.email = data.get('email')
            self.password = self.__generate_hash(data.get('password'))  # add this line

        #####################
        # existing code remain #
        ######################

        def update(self, data):
            for key, item in data.items():
                if key == 'password':  # add this new line
                    self.password = self.__generate_hash(value)  # add this new line
                setattr(self, key, item)
            self.modified_at = datetime.datetime.utcnow()
            db.session.commit()

        #####################
        # existing code remain #
        ######################

        # add this new method
        def __generate_hash(self, password):
            return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

        # add this new method
        def check_hash(self, password):
            return bcrypt.check_password_hash(self.password, password)

        #####################
        # existing code remain #
        ######################




class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    blogposts = fields.Nested(BlogpostSchema, many=True)