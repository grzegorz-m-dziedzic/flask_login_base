from app import db, login_manager
from passlib.hash import pbkdf2_sha256 as hash_alg
from flask_login import UserMixin
# from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_json(self):
        return {
            'username': self.username,
            'email': self.email
        }

    @staticmethod
    def hash_password(password):
        return hash_alg.encrypt(password)

    def verify_password(self, pwd_hash):
        return hash_alg.verify(pwd_hash, self.password_hash)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
