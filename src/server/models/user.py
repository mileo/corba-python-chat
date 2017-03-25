# coding: utf-8
from src.server import app, db

talk_users_table = db.Table(
    'talk_users', db.Model.metadata,
    db.Column('talk_id', db.Integer, db.ForeignKey('talk.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    phone = db.Column(db.String(120), unique=True)
    online = db.Column(db.Boolean)
    talks = db.relationship('Talk', secondary=talk_users_table)
    key = db.Column(db.String(36))

    def __str__(self):
        return self.phone or ''

