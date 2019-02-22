from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    details = db.relationship('Detail',backref = 'details',lazy = "dynamic")

    @property
    def password(self):

        raise AttributeError('You cannot read the password attributes')

    @password.setter
    def password(self, password):

        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):

        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'

class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(255))
    user_id = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'

class Detail(UserMixin,db.Model):

    __tablename__ = 'details'
    id = db.Column(db.Integer,primary_key =True)
    email = db.Column(db.String(255),unique = True,index = True)
    model_name = db.Column(db.String(255))
    model_age = db.Column(db.String(255))
    event_venue = db.Column(db.String(255))
    hours_booked = db.Column(db.String(255))
    model_jd = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    def save_detail(self):
        db.session.add(self)
        db.session.commit()
