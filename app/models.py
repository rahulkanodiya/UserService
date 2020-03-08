from app import db
from flask import url_for

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}  Id {}>'.format(self.username, self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            '_link': url_for('api.user', id=self.id)
        }
        return data

    def from_dict(self, data):
        for field in ['username', 'email']:
            setattr(self, field, data[field])
