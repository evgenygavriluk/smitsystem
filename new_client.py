# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_client.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewClient(object):
    def setupUi(self, NewClient):
        NewClient.setObjectName("NewClient")
        NewClient.resize(552, 504)
        self.groupBox = QtWidgets.QGroupBox(NewClient)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 531, 441))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 160, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.label_2.setObjectName("label_2")
        self.newClientINN = QtWidgets.QLineEdit(self.groupBox)
        self.newClientINN.setGeometry(QtCore.QRect(130, 150, 391, 31))
        self.newClientINN.setObjectName("newClientINN")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 200, 55, 16))
        self.label_3.setObjectName("label_3")
        self.newClientCity = QtWidgets.QLineEdit(self.groupBox)
        self.newClientCity.setGeometry(QtCore.QRect(130, 190, 391, 31))
        self.newClientCity.setObjectName("newClientCity")
        self.newClientShortName = QtWidgets.QLineEdit(self.groupBox)
        self.newClientShortName.setGeometry(QtCore.QRect(130, 230, 391, 31))
        self.newClientShortName.setObjectName("newClientShortName")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 230, 111, 31))
        self.label_4.setObjectName("label_4")
        self.newClientAbout = QtWidgets.QPlainTextEdit(self.groupBox)
        self.newClientAbout.setGeometry(QtCore.QRect(130, 270, 391, 161))
        self.newClientAbout.setObjectName("newClientAbout")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 280, 111, 51))
        self.label_6.setObjectName("label_6")
        self.newClientName = QtWidgets.QPlainTextEdit(self.groupBox)
        self.newClientName.setGeometry(QtCore.QRect(130, 40, 391, 101))
        self.newClientName.setObjectName("newClientName")
        self.createNewClient = QtWidgets.QPushButton(NewClient)
        self.createNewClient.setGeometry(QtCore.QRect(230, 460, 93, 28))
        self.createNewClient.setObjectName("createNewClient")

        self.retranslateUi(NewClient)
        QtCore.QMetaObject.connectSlotsByName(NewClient)

    def retranslateUi(self, NewClient):
        _translate = QtCore.QCoreApplication.translate
        NewClient.setWindowTitle(_translate("NewClient", "Новый контрагент"))
        self.groupBox.setTitle(_translate("NewClient", "Новый клиент"))
        self.label.setText(_translate("NewClient", "ИНН"))
        self.label_2.setText(_translate("NewClient", "Наименование"))
        self.label_3.setText(_translate("NewClient", "Город"))
        self.label_4.setText(_translate("NewClient", "Сокращенное\n"
"наименование"))
        self.label_6.setText(_translate("NewClient", "Дополнительная\n"
"информация"))
        self.createNewClient.setText(_translate("NewClient", "Создать"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewClient = QtWidgets.QWidget()
    ui = Ui_NewClient()
    ui.setupUi(NewClient)
    NewClient.show()
    sys.exit(app.exec_())
