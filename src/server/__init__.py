# coding: utf-8

import thread
import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin
from flask_admin.contrib import sqla

# Create application
app = Flask(__name__,
            template_folder='./templates',
            )

from src.server import config

db = SQLAlchemy(app)

from src.server.models.user import User, talk_users_table
from src.server.models.talk import Talk
from src.server.models.message import Message
from src.server.api.corba import ChatServerImpl


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Go to Admin!</a>'


# Customized User model admin
class UserAdmin(sqla.ModelView):

    form_excluded_columns = ['messages']


class TalkMessage(sqla.ModelView):

    inline_models = (Message,)

# Create admin
admin = admin.Admin(app, name='Corba Chat', template_mode='bootstrap3')
# Add views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(TalkMessage(Talk, db.session))
admin.add_view(sqla.ModelView(Message, db.session))


#API
from src.server.api import rest
from src.server.api import corba


if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        db.drop_all()
        db.create_all()
        db.session.commit()
    # Start app
    app_run = app.run
    kwargs = {
        'debug' : True
    }
    thread.start_new_thread(app_run,**kwargs)
    thread.start_new_thread(corba.orb.run,())
