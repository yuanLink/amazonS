# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(461, 341)
        self.testName = QtWidgets.QLabel(Dialog)
        self.testName.setGeometry(QtCore.QRect(140, 30, 171, 41))
        self.testName.setObjectName("testName")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 80, 101, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 180, 121, 21))
        self.label_2.setObjectName("label_2")
        self.UrlText = QtWidgets.QTextEdit(Dialog)
        self.UrlText.setGeometry(QtCore.QRect(80, 110, 331, 61))
        self.UrlText.setObjectName("UrlText")
        self.KeywordText = QtWidgets.QTextEdit(Dialog)
        self.KeywordText.setGeometry(QtCore.QRect(80, 200, 331, 81))
        self.KeywordText.setObjectName("KeywordText")
        self.takeButton = QtWidgets.QPushButton(Dialog)
        self.takeButton.setGeometry(QtCore.QRect(70, 300, 75, 23))
        self.takeButton.setObjectName("takeButton")
        self.cleanButton = QtWidgets.QPushButton(Dialog)
        self.cleanButton.setGeometry(QtCore.QRect(310, 300, 75, 23))
        self.cleanButton.setObjectName("cleanButton")

        self.retranslateUi(Dialog)
        self.cleanButton.clicked.connect(self.KeywordText.clear)
        self.cleanButton.clicked.connect(self.UrlText.clear)
        self.takeButton.clicked.connect(Dialog.submitRequest)
        self.UrlText.textChanged.connect(Dialog.updateUi)
        self.KeywordText.textChanged.connect(Dialog.updateUi)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Amazon Spider"))
        self.testName.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">amazon spider 1</span></p></body></html>"))
        self.label.setText(_translate("Dialog", "输入需要爬的网址"))
        self.label_2.setText(_translate("Dialog", "输入此时查询的关键字"))
        self.takeButton.setText(_translate("Dialog", "提交"))
        self.cleanButton.setText(_translate("Dialog", "清除"))

