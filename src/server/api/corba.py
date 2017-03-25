# coding: utf-8
import sys
from omniORB import CORBA
import thread
import CosNaming
import uuid
import chat
import chat__POA
from src.server.models.message import Message
from src.server.models.user import User
from src.server.models.talk import Talk
from src.server import app, db
from random import randint

from datetime import date, datetime


def secret():
    range_start = 10**(4-1)
    range_end = (10**4)-1
    return randint(range_start, range_end)



class ChatServerImpl (chat__POA.ChatServer):
    def __init__(self):
        self.phones = set()
        self.clients = {}
        self.id_to_auth = {}

    def auth(self, phone):
        """
            # TODO: send an sms to the user, or call.
        :param phone:
        :return: Esta função apenas deve retornar uma
          resposta confirmando a mensagem recebida.

          A autenticação deve ser feita via SMS ou Ligação.
        """
        if phone in self.phones:
            raise chat.NameAlreadyUsed()
        id = str(uuid.uuid4())
        # my_secret = secret()
        my_secret = '1234'
        self.id_to_auth[id] = {
            'phone': phone,
            'secret': my_secret,
        }
        print id, '|', phone, '|', my_secret
        return id

    def subscribe(self, key, secret, client):
        """
            Após recebido o sms ou o codigo via telefone o
            usuário deve enviar o mesmo ao servidor para validar
            sua autenticação.
        :param phone: 
        :param client: 
        :return: 
        """
        if not str(self.id_to_auth[key]['secret']) == str(secret):
            raise chat.IncorrectSecret()
        phone = self.id_to_auth[key]['phone']
        if phone in self.phones:
            raise chat.NameAlreadyUsed()

        # Verifica se o usuário já esta cadastrado no DB.
        user = User.query.filter_by(phone=phone).first()
        if user is None:
            # Create a new author
            user = User(phone=phone, key=key)
            db.session.add(user)

        user.online = True
        self.phones.add(phone)
        db.session.commit()
        print 'subscribe:', phone, '->', key
        self.clients[key] = (phone, client)

        user_talks = [t for t in user.talks if len(t.users) == 2]
        groups = [g for g in user.talks if len(g.users)> 2]

        for talk in user_talks:
            for user_item in talk.users:
                if user_item != user:
                    if user_item.online:
                        status = 'online'
                    else:
                        status = 'offline'
                    result1 = client.update_contact(
                        str(talk.id),
                        str(user_item.phone),
                        str(user_item.nickname or ''),
                        str(status),
                    )
            for m in talk.messages:
                result2 = client.update_talk(
                    self._format_message(
                        m.sender.phone,
                        m.sender.id,
                        m.message
                    ), str(talk.id))
        return key

    def _format_message(self, phone, user_id, text):
        return str('{0} ({1}) said: {2}'.format(phone, user_id, text))

    def unsubscribe(self, user_id):
        print 'unsubscribe:', user_id
        try:
            phone, c = self.clients[user_id]
        except:
            raise chat.UnknownID()
        user = User.query.filter_by(phone=phone).first()
        user.online = False
        db.session.commit()
        self.phones.remove(phone)
        # notificar contatos que vc não esta mais online

        user_talks = [t for t in user.talks if len(t.users) == 2]
        groups = [g for g in user.talks if len(g.users) > 2]

        for talk in user_talks:
            for user_item in talk.users:
                if user_item != user:
                    if user_item.online:
                        status = 'online'
                    else:
                        status = 'offline'
                    result1 = c.update_contact(
                        str(talk.id),
                        str(user_item.phone),
                        str(user_item.nickname or ''),
                        str(status),
                    )
        del self.clients[user_id]

    def comment(self, user_key, talk_id, text):
        try:
            phone, c = self.clients[user_key]
        except:
            raise chat.UnknownID()

        user = User.query.filter_by(phone=phone).first()
        talk = Talk.query.get(int(talk_id))

        if user is None:
            return False

        message = Message(
            message=text,
            sender=user,
        )
        talk.messages.append(message)
        db.session.add(message)
        db.session.commit()
        print 'comment:', text, 'by', user_key, '[%s]' % phone
        try:
            for i, (n, to) in self.clients.iteritems():
                result = to.update_talk(self._format_message(user.phone, user.id, text), str(talk_id))
        except:
            print 'except'
        return 'ok'

    def add_contact(self, user_phone, contact_phone):
        """

        :param id:
        :param user:
        :return:
        """
        # TODO: add user
        user_id = User.query.filter_by(phone=user_phone).first()
        contact_id = User.query.filter_by(phone=contact_phone).first()
        if contact_id is None:
            contact_id = User(phone=contact_phone)
            db.session.add(contact_id)
        talk = Talk(
            name=contact_phone,
            # date_start=datetime.now(),
            users=[contact_id, user_id]
        )
        db.session.add(talk)
        db.session.commit()
        return str(talk.id)

    # def create_group(self, user_id, name):
    #     """
    #     :param id:
    #     :param name:
    #     :return: group id
    #     """
    #     # TODO: Criar grupo
    #     user = User.query.filter_by(phone=user_id).first()
    #     group = Talk(
    #         name=name,
    #         date_start=datetime.now(),
    #         admin_id=user_id,
    #         users=[user_id],
    #     )
    #     db.session.add(group)
    #     db.session.commit()
    #     return 'group_id'
    #
    # def add_user_group(self, user_id, group_od, adduser):
    #     """
    #
    #     :param id:
    #     :param user:
    #     :return:
    #     """
    #     # TODO: add user
    #     group = self._is_group_admin(user_id, group_id)
    #     if group:
    #         pass
    #         # adicionar usuário ao grupo
    #     return 'ok'
    #
    # def remove_user_group(self, user_id, group_id, deluser):
    #     """
    #
    #     :param id:
    #     :param user:
    #     :return:
    #     """
    #     # TODO: Remover do grupo
    #     group = self._is_group_admin(user_id, group_id)
    #     if group:
    #         pass
    #         # remover usuário ao grupo
    #     return 'ok'




# initializing ORB
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# getting referenec to POA
poa = orb.resolve_initial_references('RootPOA')
# getting reference to POA manager
manager = poa._get_the_POAManager()
# activating manager
manager.activate()

# getting NameService
obj = orb.resolve_initial_references('NameService')
ncRef = obj._narrow(CosNaming.NamingContext)

# creating servant
cs = ChatServerImpl()
# connecting servant to ORB
chatserver = cs._this()
# binding servant reference to NameService
ncRef.rebind([CosNaming.NameComponent('chatserver_18721', '')], chatserver)
