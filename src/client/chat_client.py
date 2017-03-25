# -*- coding: utf-8 -*-
from threading import Thread
import sys
import uuid

import CosNaming
from omniORB import CORBA

from src.client.user_interface import init, LoginWizard, MainWindow

import chat, chat__POA
from chat import NameAlreadyUsed


orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
# getting NameService
obj = orb.resolve_initial_references('NameService')
ncRef = obj._narrow(CosNaming.NamingContext)
# resolving servant name
obj = ncRef.resolve([CosNaming.NameComponent('chatserver_18721', '')])
server = obj._narrow(chat.ChatServer)


APP_TITLE = 'CORBA CHAT'

class ORBThread (Thread):

    def run(self):
        # getting reference to POA
        poa = orb.resolve_initial_references('RootPOA')
        # getting reference to POA manager
        manager = poa._get_the_POAManager()
        # activating manager
        manager.activate()
        # starting orb
        orb.run()


from collections import OrderedDict


class ChatClientImpl(chat__POA.ChatClient):

    lines = OrderedDict()

    def __init__(self, server):
        self._server = server
        self._client_reference = self._this()
        self.lw = LoginWizard()
        self.mw = MainWindow(self)

    def _add_contact(self, talk_id, phone, name, is_group=False, user_status=False):
        item = ChatClientLine(talk_id, phone, name, is_group, user_status)
        self.lines[phone] = item
        print item
        return item

    def _talk_list(self):
        user_list = []
        for item in self.lines:
            user_list.append(str('ID: {0} Phone: {1} Status: {2}'.format(
                self.lines[item].talk_id,
                ''.join(self.lines[item].user_ids),
                self.lines[item].user_status,
            )))
        return user_list

    def _search_talk_id(self, talk_id):
        for item in self.lines:
            if self.lines[item].talk_id == str(talk_id):
                return self.lines[item]
        return False

    def _refresh_ui(self, talk_id=False):
        self.mw.update_view(talk_id)

    def auth(self, phone):
        """
            Realiza a solicitação de autenticação do usuário
        :param phone:
        :return:
        """
        self.phone = str(phone)
        self.user_key = str(self._server.auth(self.phone))

    def subscribe(self, secret):
        """
            Inscreve o usuário no servidor
        :param secret:
        :return:
        """
        self._secret = str(secret)
        self._id = self._server.subscribe(
            self.user_key,
            self._secret,
            self._client_reference
        )

    def unsubscribe(self):
        result = self._server.unsubscribe(self.user_key)
        # self.orb_thread.join()
        orb.destroy()

    def add_contact(self, phone, name=False, is_group=False):
        user_status = ''
        talk_id = self._server.add_contact(self.phone, str(phone))
        if not is_group:
            # user_status = self.chatserver.user_status(str(phone))
            user_status = 'online'
        item = self._add_contact(talk_id, phone, name, is_group, user_status)
        self._refresh_ui()

    def comment(self, talk_id, text):
        result = self._server.comment(self.user_key, talk_id, text)
        if result:
            self._refresh_ui(talk_id)
            return True
        return False

    # Metodos da interface do cliente

    def update_talk(self, text, talk_id):
        item = self._search_talk_id(talk_id)
        if item:
            item.messages = text
            self._refresh_ui()
            print talk_id, text
            return 'ok'

    def update_contact(self, talk_id, phone, name, online):
        print talk_id, phone, name, online
        item = self._add_contact(talk_id, phone, name, False, online)
        self._refresh_ui()
        return 'ok'

    def __iter__(self):
        return self.lines

    def __getitem__(self, key):
        return self.lines[key]


class ChatClientLine(object):

    def __init__(self, talk_id, user_ids, name, is_group=False, user_status=False):
        self.user_ids = []
        self.user_ids.append(user_ids)
        self.is_group = is_group
        self._messages = []
        self._name = name
        self.user_status = user_status
        self.talk_id = str(talk_id)

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        self._messages.append(value)

    def __str__(self):
        if self.is_group:
            return str('Group: {0}'.format(self._name))
        else:
            return str('User: {0} {1}'.format(self.user_ids, self.user_status))


def run():
    # initializing ORB
    app = init()
    client = ChatClientImpl(server)
    orb_tread = ORBThread()
    orb_tread.start()
    while True:
        if client.lw.logon(client):
            client.mw.display()
        sys.exit(app.exec_())
