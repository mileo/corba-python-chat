# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QAction, qApp, QApplication, QWidget, QTextEdit, QListWidgetItem,
    QPushButton, QInputDialog, QSplitter, QHBoxLayout, QFrame, QMessageBox, QDialog
)
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon


APP_TITLE ='123123'


class GroupDialog(object):

    def setupUi(self, Dialog, user_list):
        self._user_list = user_list
        self._to_add = []
        Dialog.setObjectName("Dialog")
        Dialog.resize(734, 589)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 2, 2))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listView = QtWidgets.QListWidget(Dialog)
        self.listView.setGeometry(QtCore.QRect(10, 10, 341, 511))
        self.listView.setObjectName("listView")
        self.listView.addItems(user_list)
        self.listView_2 = QtWidgets.QListWidget(Dialog)
        self.listView_2.setGeometry(QtCore.QRect(360, 10, 361, 511))
        self.listView_2.setObjectName("listView_2")
        self.textEdit = QtWidgets.QLineEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(200, 530, 311, 41))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 530, 161, 41))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(550, 530, 151, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self._create_group)
        self.listView.itemDoubleClicked.connect(self.to_add)
        self.listView_2.itemDoubleClicked.connect(self.to_remove)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Nome do Grupo"))
        self.pushButton.setText(_translate("Dialog", "Criar Grupo"))

    def to_add(self, item):
        text = item.text()
        self._user_list.remove(text)
        self._to_add.append(text)

        self.listView.clear()
        self.listView.addItems(self._user_list)

        self.listView_2.clear()
        self.listView_2.addItems(self._to_add)


    def to_remove(self, item):
        text = item.text()
        self._to_add.remove(text)
        self._user_list.append(text)

        self.listView.clear()
        self.listView.addItems(self._user_list)

        self.listView_2.clear()
        self.listView_2.addItems(self._to_add)


    def _create_group(self, item):
        name = self.textEdit.text()
        to_add = self._to_add
        return name, to_add
