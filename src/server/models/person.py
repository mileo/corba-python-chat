# coding: utf-8
from src.server import app, db


talk_people_table = db.Table(
    'talk_people', db.Model.metadata,
    db.Column('talk_id', db.Integer, db.ForeignKey('talk.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
)


class Person(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    phone = db.Column(db.String(120), unique=True)
    online = db.Column(db.Boolean)
    talks = db.relationship('Talk', secondary=talk_people_table)

    def __str__(self):
        if self.online:
            return self.nickname + " (online)"
        return self.nickname + " (offline)"
