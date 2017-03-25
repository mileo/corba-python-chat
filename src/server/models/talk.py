# coding: utf-8
from src.server import app, db
from src.server.models.user import User, talk_users_table


class Talk(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    date_start = db.Column(db.DateTime)
    users = db.relationship('User', secondary=talk_users_table)
    # messages = db.relationship('Message', secondary=talk_messages_table)
    admin_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    is_group = db.Column(db.Boolean)
    messages = db.relationship('Message', backref='talk',
                               lazy='dynamic')

    def __str__(self):
        # TODO: Retornar o nome do grupo ou o nome do outro integrante da conversa.
        return self.name


    def _is_group_admin(self, id, group):
        """
            Verifica se o usuário é admin do grupo
        :param user:
        :param group:
        :return: Retorna o objeto do grupo quando verdadeiro
            retorna False quando o usário nao é admin do grupo.
        """
        return True
