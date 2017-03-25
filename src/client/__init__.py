# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# APP_TITLE = 'CORBA CHAT'
#
#
# import sys
# import uuid
# from omniORB import CORBA
# import chat, chat__POA
# import CosNaming
# from threading import Thread
#
# from PyQt5.QtWidgets import *
#     # (QMainWindow, QAction, qApp, QApplication, QWidget, QTextEdit,
#     # QPushButton, QInputDialog, QSplitter, QHBoxLayout, QFrame)
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QCoreApplication
# from PyQt5.QtCore import Qt
#
# from PyQt5.QtGui import QIcon
#
# from chat import NameAlreadyUsed
#
# orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
# # getting NameService
# obj = orb.resolve_initial_references('NameService')
# ncRef = obj._narrow(CosNaming.NamingContext)
# # resolving servant name
# obj = ncRef.resolve([CosNaming.NameComponent('chatserver_18721', '')])
# chatserver = obj._narrow(chat.ChatServer)
#
#
# from collections import OrderedDict
# from collections import namedtuple
#
# namedtuple('Talk', 'phone status name')
#
# def fatal_error(message):
#     """
#         Mensagem de erro fatal, que encerra o sistema depois de exibida.
#     :param message:
#     :return:
#     """
#     msg = QMessageBox()
#     msg.setIcon(QMessageBox.Critical)
#     msg.setText(message)
#     msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#     msg.exec_()
#     QtCore.QCoreApplication.instance().quit()
#
#
# class ORBThread (Thread):
#
#     def run(self):
#         # getting reference to POA
#         poa = orb.resolve_initial_references('RootPOA')
#         # getting reference to POA manager
#         manager = poa._get_the_POAManager()
#         # activating manager
#         manager.activate()
#         # starting orb
#         orb.run()
#
#
# class ChatClientImpl(chat__POA.ChatClient):
#
#     def update_talk(self, text, talk_id):
#         print text, talk_id,
#
#
#     def update_contact(self, user, status):
#         print ('<%s> %s' % (user, status))
#
#
#
# class TalkItem(object):
#
#     def __init__(self, talk_id, user_ids, name, is_group=False, user_status=False):
#         self.user_ids = []
#         self.user_ids.append(user_ids)
#         self.is_group = is_group
#         self._messages = []
#         self._name = name
#         self.user_status = user_status
#         self.talk_id = talk_id
#
#     @property
#     def messages(self):
#         return self._messages
#
#     @messages.setter
#     def messages(self, value):
#         self._messages.append(value)
#
#     def __str__(self):
#         if not self.is_group:
#             return 'Group: ' + self._name
#         else:
#             self.name = 'User: ' + self.user_ids  + ' ' + self.user_status
#
#
# class Talk(object):
#
#     lines = OrderedDict()
#
#     def __init__(self, chatserver):
#         self.chatserver = chatserver
#         self.chat_client_impl = ChatClientImpl()
#         self.chat_client_impl_reference = self.chat_client_impl._this()
#         self.orb_thread = ORBThread()
#
#     def auth(self, phone):
#         self.phone = str(phone)
#         self.user_key = str(self.chatserver.auth(self.phone))
#
#     def subscribe(self, secret ):
#         self._secret = str(secret)
#         self._id = self.chatserver.subscribe(
#             self.user_key,
#             self._secret,
#             self.chat_client_impl_reference
#         )
#
#     def unsubscribe(self):
#         print ('Unsubscribing...',
#                self.chatserver.unsubscribe(self.user_key))
#         print (' done')
#         #self.orb_thread.join()
#         orb.destroy()
#
#     def add_contact(self, phone, name=False, is_group=False):
#         user_status = ''
#         talk_id = self.chatserver.add_contact(self.phone, str(phone))
#         if not is_group:
#             # user_status = self.chatserver.user_status(str(phone))
#             user_status = 'online'
#         item = TalkItem(talk_id, phone, name, is_group, user_status)
#         self.lines[phone] = item
#
#     def talk_list(self):
#         return self.lines.keys()
#
#     def __iter__(self):
#         return self.lines
#
#     def __getitem__(self, key):
#         return self.lines[key]
#
#     def search_talk_id(self, talk_id):
#         for item in self.lines:
#             if item.talk_id == talk_id:
#                 return item
#
#     def comment(self, talk_id, text):
#         result = self.chatserver.comment(self.user_key, talk_id, text)
#         if result:
#             return True
#         return False
#
#
#
# class NewGroupWizard(QWidget):
#
#     def __init__(self, chatclient):
#         super(NewGroupWizard, self).__init__()
#         self.chatclient = chatclient
#         self.add_group()
#
#     def add_group(self):
#         phone, ok = QInputDialog.getText(
#             self, APP_TITLE,
#             'Digite o numero do contato')
#         if ok:
#             try:
#                 self.chatclient.add_contact(phone)
#             except NameAlreadyUsed:
#                 fatal_error('Usuário já logado em outro cliente')
#             except:
#                 fatal_error('Servidor não encontrado')
#         return False
#
#
# class NewContactWizard(QWidget):
#
#     def __init__(self, chatclient):
#         super(NewContactWizard, self).__init__()
#         self.chatclient = chatclient
#
#     def add_contact(self):
#         phone, ok = QInputDialog.getText(
#             self, APP_TITLE,
#             'Digite o numero do contato')
#         if ok:
#             # try:
#             result = self.chatclient.add_contact(phone)
#             return result
#             # except NameAlreadyUsed:
#             #     fatal_error('Usuário já logado em outro cliente')
#             # except:
#             #     fatal_error('Servidor não encontrado')
#         return False
#
#
# class LoginWizard(QWidget):
#     #
#     # def __init__(self, chatclient):
#     #     super(LoginWizard, self).__init__()
#     #
#     def login(self, chatclient):
#         phone, ok = QInputDialog.getText(
#             self, APP_TITLE,
#             'To login or register\n\n Please enter your phone, with country code:')
#         if ok:
#             try:
#                 chatclient.auth(phone)
#             except NameAlreadyUsed:
#                 fatal_error('Usuário já logado em outro cliente')
#             except:
#                 fatal_error('Servidor não encontrado')
#             secret, ok = QInputDialog.getText(
#                 self, APP_TITLE, 'Enter the sms code:')
#             if ok:
#                 chatclient.subscribe(secret)
#
#                 return True
#         return False
#
#
# class UiCorbaMainWindow(object):
#
#     def setupUi(self, CorbaMainWindow):
#         CorbaMainWindow.setObjectName("Corba Chat")
#         CorbaMainWindow.resize(1024, 708)
#         self.centralWidget = QtWidgets.QWidget(CorbaMainWindow)
#         self.centralWidget.setObjectName("centralWidget")
#         self.splitter = QtWidgets.QSplitter(self.centralWidget)
#         self.splitter.setGeometry(QtCore.QRect(0, 0, 1024, 650))
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
#         self.splitter.setSizePolicy(sizePolicy)
#         self.splitter.setOrientation(QtCore.Qt.Vertical)
#         self.splitter.setObjectName("splitter")
#
#         # Divisor mensagem e usuários
#         self.chatMessagesLayout = QtWidgets.QWidget(self.splitter)
#         self.chatMessagesLayout.setObjectName("chatMessagesLayout")
#
#         self.boxLayout = QtWidgets.QHBoxLayout(self.chatMessagesLayout)
#         self.boxLayout.setContentsMargins(0, 0, 0, 0)
#         self.boxLayout.setSpacing(6)
#         self.boxLayout.setObjectName("boxLayout")
#
#         self.listWidget = QtWidgets.QListWidget(self.chatMessagesLayout)
#         self.listWidget.setEnabled(True)
#         # self.listWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
#         self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
#         self.listWidget.setObjectName("listWidget")
#         self.boxLayout.addWidget(self.listWidget)
#         # self.listWidget.addItems([
#         #     'Joao',
#         #     'Mileo',
#         #     'Latika',
#         # ])
#
#         self.textEdit = QtWidgets.QTextEdit(self.chatMessagesLayout)
#         self.textEdit.setEnabled(True)
#         self.textEdit.setFocusPolicy(QtCore.Qt.NoFocus)
#         self.textEdit.setReadOnly(True)
#         self.textEdit.setObjectName("textEdit")
#         self.boxLayout.addWidget(self.textEdit)
#
#
#         # Divisor enviar mensagem
#         self.layoutWidget = QtWidgets.QWidget(self.splitter)
#         self.layoutWidget.setObjectName("layoutWidget")
#         self.sendLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
#         self.sendLayout.setContentsMargins(0, 0, 0, 0)
#         self.sendLayout.setSpacing(6)
#         self.sendLayout.setObjectName("sendLayout")
#
#         self.lbl_mensagem = QtWidgets.QLabel(self.layoutWidget)
#         self.lbl_mensagem.setObjectName("label")
#         self.lbl_mensagem.setText("Mensagem:")
#         self.sendLayout.addWidget(self.lbl_mensagem)
#
#         self.edt_message = QtWidgets.QLineEdit(self.layoutWidget)
#         self.edt_message.setObjectName("lineEdit")
#         self.sendLayout.addWidget(self.edt_message)
#         self.edt_message.raise_()
#         self.lbl_mensagem.raise_()
#
#         self.btn_send = QtWidgets.QPushButton(self.layoutWidget)
#         self.btn_send.setText('Enviar')
#         self.btn_send.clicked.connect(CorbaMainWindow.handleSend)
#         self.sendLayout.addWidget(self.btn_send)
#
#         CorbaMainWindow.setCentralWidget(self.centralWidget)
#         self.toolBar = QtWidgets.QToolBar(CorbaMainWindow)
#         self.toolBar.setObjectName("toolBar")
#         CorbaMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
#         self.statusBar = QtWidgets.QStatusBar(CorbaMainWindow)
#         self.statusBar.setObjectName("statusBar")
#         CorbaMainWindow.setStatusBar(self.statusBar)
#
#         self.actionNew_Contact = QtWidgets.QAction(QIcon('images/list-add-user.svg'), 'Exit', CorbaMainWindow)
#         self.actionNew_Contact.setObjectName("actionNew_Contact")
#         self.actionNew_Contact.triggered.connect(CorbaMainWindow.new_contact)
#
#         self.actionNew_Group = QtWidgets.QAction(QIcon('images/meeting-attending.svg'), 'Exit', CorbaMainWindow)
#         self.actionNew_Group.setObjectName("actionNew_Group")
#         self.actionNew_Group.triggered.connect(CorbaMainWindow.new_group)
#
#         self.actionQuit = QtWidgets.QAction(QIcon('images/application-exit.png'), 'Exit', CorbaMainWindow)
#         self.actionQuit.setObjectName("actionQuit")
#         self.actionQuit.triggered.connect(CorbaMainWindow.close)
#
#         self.toolBar.addAction(self.actionNew_Contact)
#         self.toolBar.addAction(self.actionNew_Group)
#         self.toolBar.addAction(self.actionQuit)
#
#
#
#
#         self.retranslateUi(CorbaMainWindow)
#         QtCore.QMetaObject.connectSlotsByName(CorbaMainWindow)
#
#     def retranslateUi(self, CorbaMainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         CorbaMainWindow.setWindowTitle(_translate("CorbaMainWindow", "CorbaMainWindow"))
#         self.toolBar.setWindowTitle(_translate("CorbaMainWindow", "toolBar"))
#         self.actionNew_Contact.setText(_translate("CorbaMainWindow", "New Contact"))
#         self.actionNew_Group.setText(_translate("CorbaMainWindow", "New Group"))
#         self.actionQuit.setText(_translate("CorbaMainWindow", "Quit"))
#
#
# class MainWindow(QMainWindow):
#
#     def __init__(self, chatclient):
#         self.chatclient = chatclient
#         super(MainWindow, self).__init__()
#         self.principal = UiCorbaMainWindow()
#         self.principal.setupUi(self)
#         self.show()
#
#     def new_contact(self):
#         new = NewContactWizard(self.chatclient)
#         new_talk = new.add_contact()
#         self.principal.listWidget.clear()
#         self.principal.listWidget.addItems(self.chatclient.talk_list())
#         self.principal.listWidget.itemClicked.connect(self.item_pressed)
#         # self.principal.listWidget.itemPressed(self.item_pressed)
#
#     def new_group(self):
#         new = NewGroupWizard(self.chatclient)
#
#     def closeEvent(self, event):
#
#         reply = QMessageBox.question(self, 'Message',
#                                      "Are you sure to quit?", QMessageBox.Yes |
#                                      QMessageBox.No, QMessageBox.No)
#         if reply == QMessageBox.Yes:
#             self.chatclient.unsubscribe()
#             event.accept()
#         else:
#             event.ignore()
#
#     def item_pressed(self, item):
#         selected = self.chatclient.lines[item.text()]
#         # self.selected_talk_id = self.chatclient[item.text()].talk_id
#         string = ''
#         for m in selected.messages:
#             string += (str(m) + '\n')
#         self.principal.textEdit.setText(string)
#
#
#     def handleSend(self):
#         # if self.selected_talk_id:
#         selected = self.principal.listWidget.selectedItems()
#         if selected:
#             selected_talk_id = False
#             selected_talk_id = self.chatclient[selected[0].text()].talk_id
#             text = str(self.principal.edt_message.text())
#             if selected_talk_id and text:
#                 result = self.chatclient.comment(
#                     selected_talk_id,
#                     text,
#                 )
#                 return result
#         return False
#
#
# if __name__ == '__main__':
#     # initializing ORB
#     app = QApplication(sys.argv)
#     talk = Talk(chatserver)
#     talk.orb_thread.start()
#     while True:
#         lw = LoginWizard()
#         if lw.login(talk):
#            mw = MainWindow(talk)
#         sys.exit(app.exec_())
