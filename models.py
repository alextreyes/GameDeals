"""Game deals models"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    @classmethod
    def signup(cls, username, password, profile_pic="/static/images/default-pic.png"):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        existing_user = cls.query.filter(cls.username == username).first()
        if existing_user:
            return None  # Username already exists, return None

        user = User(
            username=username,
            password=hashed_pwd,
            profile_pic=profile_pic,
    )

        db.session.add(user)
        db.session.commit()  
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class UserList(db.Model):
    __tablename__ = 'user_lists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    list_name = db.Column(db.String(255), nullable=False)
    user = db.relationship('User', backref=db.backref('lists', cascade='all,delete'))

    def __repr__(self):
        return '<UserList {}>'.format(self.list_name)
    
class UserListGame(db.Model):
    __tablename__ = 'user_list_games'
    list_id = db.Column(db.Integer, db.ForeignKey('user_lists.id'), primary_key=True)
    game_id = db.Column(db.Integer, primary_key=True)
    user_list = db.relationship('UserList', backref=db.backref('games', cascade='all,delete'))

    def __repr__(self):
        return '<UserListGame(list_id={}, game_id={})>'.format(self.list_id, self.game_id)
    
class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('user_lists.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('likes', cascade='all,delete'))

    def __repr__(self):
        return '<Like(user_id={}, list_id={})>'.format(self.user_id, self.list_id)

