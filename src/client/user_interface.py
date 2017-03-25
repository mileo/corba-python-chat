# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QAction, qApp, QApplication, QWidget, QTextEdit, QListWidgetItem,
    QPushButton, QInputDialog, QSplitter, QHBoxLayout, QFrame, QMessageBox
)
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon

APP_TITLE ='123123'
from chat import NameAlreadyUsed

from src.client.group_wizard import GroupDialog


def fatal_error(message):
    """
        Mensagem de erro fatal, que encerra o sistema depois de exibida.
    :param message:
    :return:
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()
    QtCore.QCoreApplication.instance().quit()


class NewGroupWizard(QWidget):

    def __init__(self, chatclient):
        super(NewGroupWizard, self).__init__()
        self.chatclient = chatclient

    def add_group(self):
        phone, ok = QInputDialog.getText(
            self, APP_TITLE,
            'Digite o numero do contato')
        if ok:
            try:
                self.chatclient.add_contact(phone)
            except NameAlreadyUsed:
                fatal_error('Usuário já logado em outro cliente')
            except:
                fatal_error('Servidor não encontrado')
        return False


class NewContactWizard(QWidget):

    def __init__(self, chatclient):
        super(NewContactWizard, self).__init__()
        self.chatclient = chatclient

    def add_contact(self):
        phone, ok = QInputDialog.getText(
            self, APP_TITLE,
            'Digite o numero do contato')
        if ok:
            # try:
            result = self.chatclient.add_contact(phone)
            return result
            # except NameAlreadyUsed:
            #     fatal_error('Usuário já logado em outro cliente')
            # except:
            #     fatal_error('Servidor não encontrado')
        return False


class LoginWizard(QWidget):
    #
    # def __init__(self, chatclient):
    #     super(LoginWizard, self).__init__()
    #
    def logon(self, chatclient):
        phone, ok = QInputDialog.getText(
            self, APP_TITLE,
            'To login or register\n\n Please enter your phone, with country code:')
        if ok:
            try:
                chatclient.auth(phone)
            except NameAlreadyUsed:
                fatal_error('Usuário já logado em outro cliente')
            except:
                fatal_error('Servidor não encontrado')
            secret, ok = QInputDialog.getText(
                self, APP_TITLE, 'Enter the sms code:')
            if ok:
                chatclient.subscribe(secret)

                return True
        return False


class UiCorbaMainWindow(object):

    def setupUi(self, CorbaMainWindow):
        CorbaMainWindow.setObjectName("Corba Chat")
        CorbaMainWindow.resize(1024, 708)
        self.centralWidget = QtWidgets.QWidget(CorbaMainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setGeometry(QtCore.QRect(0, 0, 1024, 650))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        # Divisor mensagem e usuários
        self.chatMessagesLayout = QtWidgets.QWidget(self.splitter)
        self.chatMessagesLayout.setObjectName("chatMessagesLayout")

        self.boxLayout = QtWidgets.QHBoxLayout(self.chatMessagesLayout)
        self.boxLayout.setContentsMargins(0, 0, 0, 0)
        self.boxLayout.setSpacing(6)
        self.boxLayout.setObjectName("boxLayout")

        self.listWidget = QtWidgets.QListWidget(self.chatMessagesLayout)
        self.listWidget.setEnabled(True)
        # self.listWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget.setObjectName("listWidget")
        self.boxLayout.addWidget(self.listWidget)
        self.listWidget.itemClicked.connect(CorbaMainWindow.item_pressed)

        # self.listWidget.addItems([
        #     'Joao',
        #     'Mileo',
        #     'Latika',
        # ])

        self.textEdit = QtWidgets.QTextEdit(self.chatMessagesLayout)
        self.textEdit.setEnabled(True)
        self.textEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.boxLayout.addWidget(self.textEdit)


        # Divisor enviar mensagem
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.sendLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.sendLayout.setContentsMargins(0, 0, 0, 0)
        self.sendLayout.setSpacing(6)
        self.sendLayout.setObjectName("sendLayout")

        self.lbl_mensagem = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_mensagem.setObjectName("label")
        self.lbl_mensagem.setText("Mensagem:")
        self.sendLayout.addWidget(self.lbl_mensagem)

        self.edt_message = QtWidgets.QLineEdit(self.layoutWidget)
        self.edt_message.setObjectName("lineEdit")
        self.sendLayout.addWidget(self.edt_message)
        self.edt_message.raise_()
        self.lbl_mensagem.raise_()

        self.btn_send = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_send.setText('Enviar')
        self.btn_send.clicked.connect(CorbaMainWindow.handleSend)
        self.sendLayout.addWidget(self.btn_send)

        CorbaMainWindow.setCentralWidget(self.centralWidget)
        self.toolBar = QtWidgets.QToolBar(CorbaMainWindow)
        self.toolBar.setObjectName("toolBar")
        CorbaMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(CorbaMainWindow)
        self.statusBar.setObjectName("statusBar")
        CorbaMainWindow.setStatusBar(self.statusBar)

        self.actionNew_Contact = QtWidgets.QAction(QIcon('images/list-add-user.svg'), 'Exit', CorbaMainWindow)
        self.actionNew_Contact.setObjectName("actionNew_Contact")
        self.actionNew_Contact.triggered.connect(CorbaMainWindow.new_contact)

        self.actionNew_Group = QtWidgets.QAction(QIcon('images/meeting-attending.svg'), 'Exit', CorbaMainWindow)
        self.actionNew_Group.setObjectName("actionNew_Group")
        self.actionNew_Group.triggered.connect(CorbaMainWindow.new_group)

        self.actionQuit = QtWidgets.QAction(QIcon('images/application-exit.png'), 'Exit', CorbaMainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(CorbaMainWindow.close)

        self.toolBar.addAction(self.actionNew_Contact)
        self.toolBar.addAction(self.actionNew_Group)
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(CorbaMainWindow)
        QtCore.QMetaObject.connectSlotsByName(CorbaMainWindow)

    def retranslateUi(self, CorbaMainWindow):
        _translate = QtCore.QCoreApplication.translate
        CorbaMainWindow.setWindowTitle(_translate("CorbaMainWindow", "CorbaMainWindow"))
        self.toolBar.setWindowTitle(_translate("CorbaMainWindow", "toolBar"))
        self.actionNew_Contact.setText(_translate("CorbaMainWindow", "New Contact"))
        self.actionNew_Group.setText(_translate("CorbaMainWindow", "New Group"))
        self.actionQuit.setText(_translate("CorbaMainWindow", "Quit"))


class MainWindow(QMainWindow):

    def __init__(self, chatclient):
        self.chatclient = chatclient
        super(MainWindow, self).__init__()
        self.principal = UiCorbaMainWindow()
        self.principal.setupUi(self)

    def display(self):
        self.show()

    def new_contact(self):
        new = NewContactWizard(self.chatclient)
        new_talk = new.add_contact()
        self.update_view()
        #self.principal.listWidget.itemPressed(self.item_pressed)

    def update_view(self, talk_id=False):
        self.principal.listWidget.clear()
        # for item in self.chatclient.lines:
        #     if self.chatclient[item].user_status:
        #         item = QListWidgetItem(''.join(self.chatclient[item].user_ids))
        #         item.setIcon(QIcon('images/user-avaliable.png'))
        #         self.principal.listWidget.addItem(item)
        #     else:
        #         self.principal.listWidget.addItem(''.join(self.chatclient[item].user_ids))
        #     if talk_id:
        #         self.principal.edt_message.setText('')

        self.principal.listWidget.addItems(self.chatclient._talk_list())

        if talk_id:
            self.principal.edt_message.setText('')

    def new_group(self):
        group = GroupDialog()
        d = QtWidgets.QDialog()
        group.setupUi(d, self.chatclient._talk_list())
        d.exec_()
        pass

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.chatclient.unsubscribe()
            event.accept()
        else:
            event.ignore()

    def item_pressed(self, item):
        phone = item.text().split(' ')[3]
        selected = self.chatclient.lines[phone]
        self.selected_talk_id = self.chatclient[phone].talk_id
        string = ''
        for m in selected.messages:
            string += (str(m) + '\n')
        self.principal.textEdit.setText(string)

    def handleSend(self):
        # if self.selected_talk_id:
        selected = self.principal.listWidget.selectedItems()
        if selected:
            selected_talk_id = False
            phone = selected[0].text().split(' ')[3]
            selected_talk_id = self.chatclient[phone].talk_id
            text = str(self.principal.edt_message.text())
            if selected_talk_id and text:
                result = self.chatclient.comment(
                    selected_talk_id,
                    text,
                )
                return result
        return False


def init():
    app = QApplication(sys.argv)
    return app

