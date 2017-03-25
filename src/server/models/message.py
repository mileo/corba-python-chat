# coding: utf-8
from src.server import app, db


class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    talk_id = db.Column(db.Integer, db.ForeignKey('talk.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship('User', backref=db.backref('messages', lazy='dynamic'))
    date_start = db.Column(db.DateTime)
    message = db.Column(db.Text())

    def __str__(self):
        return self.message[:30] + ' ...'
