# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_order.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewOrder(object):
    def setupUi(self, NewOrder):
        NewOrder.setObjectName("NewOrder")
        NewOrder.resize(1041, 647)
        self.newOrderTable = QtWidgets.QTableWidget(NewOrder)
        self.newOrderTable.setGeometry(QtCore.QRect(450, 70, 581, 311))
        self.newOrderTable.setObjectName("newOrderTable")
        self.newOrderTable.setColumnCount(3)
        self.newOrderTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.newOrderTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.newOrderTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.newOrderTable.setHorizontalHeaderItem(2, item)
        self.getOrder = QtWidgets.QPushButton(NewOrder)
        self.getOrder.setGeometry(QtCore.QRect(450, 600, 121, 28))
        self.getOrder.setObjectName("getOrder")
        self.clearTable = QtWidgets.QPushButton(NewOrder)
        self.clearTable.setGeometry(QtCore.QRect(890, 390, 141, 31))
        self.clearTable.setObjectName("clearTable")
        self.groupBox = QtWidgets.QGroupBox(NewOrder)
        self.groupBox.setGeometry(QtCore.QRect(10, 310, 431, 131))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.label_3.setObjectName("label_3")
        self.addelemToTable = QtWidgets.QPushButton(self.groupBox)
        self.addelemToTable.setGeometry(QtCore.QRect(280, 80, 141, 31))
        self.addelemToTable.setObjectName("addelemToTable")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 91, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(50, 20, 371, 31))
        self.comboBox.setObjectName("comboBox")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setGeometry(QtCore.QRect(10, 80, 151, 31))
        self.spinBox.setMaximum(999999)
        self.spinBox.setObjectName("spinBox")
        self.addProduct = QtWidgets.QToolButton(self.groupBox)
        self.addProduct.setGeometry(QtCore.QRect(10, 20, 31, 31))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("venv/icons/new-order-plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addProduct.setIcon(icon)
        self.addProduct.setObjectName("addProduct")
        self.clipboardToTable = QtWidgets.QPushButton(NewOrder)
        self.clipboardToTable.setGeometry(QtCore.QRect(450, 390, 181, 31))
        self.clipboardToTable.setObjectName("clipboardToTable")
        self.groupBox_2 = QtWidgets.QGroupBox(NewOrder)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 50, 431, 261))
        self.groupBox_2.setObjectName("groupBox_2")
        self.textfieldOrder = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.textfieldOrder.setGeometry(QtCore.QRect(10, 20, 411, 191))
        self.textfieldOrder.setObjectName("textfieldOrder")
        self.textfieldToTable = QtWidgets.QPushButton(self.groupBox_2)
        self.textfieldToTable.setGeometry(QtCore.QRect(280, 220, 141, 28))
        self.textfieldToTable.setObjectName("textfieldToTable")
        self.clearTextfield = QtWidgets.QPushButton(self.groupBox_2)
        self.clearTextfield.setGeometry(QtCore.QRect(10, 220, 111, 28))
        self.clearTextfield.setObjectName("clearTextfield")
        self.label = QtWidgets.QLabel(NewOrder)
        self.label.setGeometry(QtCore.QRect(450, 20, 55, 16))
        self.label.setObjectName("label")
        self.partnersList = QtWidgets.QComboBox(NewOrder)
        self.partnersList.setGeometry(QtCore.QRect(550, 10, 481, 31))
        self.partnersList.setObjectName("partnersList")
        self.addPartner = QtWidgets.QToolButton(NewOrder)
        self.addPartner.setGeometry(QtCore.QRect(510, 10, 31, 31))
        self.addPartner.setIcon(icon)
        self.addPartner.setObjectName("addPartner")
        self.lineEdit = QtWidgets.QLineEdit(NewOrder)
        self.lineEdit.setGeometry(QtCore.QRect(230, 490, 211, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.textEdit = QtWidgets.QTextEdit(NewOrder)
        self.textEdit.setGeometry(QtCore.QRect(450, 490, 581, 91))
        self.textEdit.setObjectName("textEdit")
        self.dateEdit = QtWidgets.QDateEdit(NewOrder)
        self.dateEdit.setGeometry(QtCore.QRect(20, 490, 191, 31))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.label_4 = QtWidgets.QLabel(NewOrder)
        self.label_4.setGeometry(QtCore.QRect(20, 470, 201, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(NewOrder)
        self.label_5.setGeometry(QtCore.QRect(230, 470, 191, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(NewOrder)
        self.label_6.setGeometry(QtCore.QRect(450, 470, 81, 16))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(NewOrder)
        QtCore.QMetaObject.connectSlotsByName(NewOrder)

    def retranslateUi(self, NewOrder):
        _translate = QtCore.QCoreApplication.translate
        NewOrder.setWindowTitle(_translate("NewOrder", "Оформление нового заказа"))
        item = self.newOrderTable.horizontalHeaderItem(0)
        item.setText(_translate("NewOrder", "Товар"))
        item = self.newOrderTable.horizontalHeaderItem(1)
        item.setText(_translate("NewOrder", "Количество"))
        item = self.newOrderTable.horizontalHeaderItem(2)
        item.setText(_translate("NewOrder", "Удаление"))
        self.getOrder.setText(_translate("NewOrder", "Принять заказ"))
        self.clearTable.setText(_translate("NewOrder", "Очистить таблицу"))
        self.label_3.setText(_translate("NewOrder", "Количество"))
        self.addelemToTable.setText(_translate("NewOrder", "Добавить элемент"))
        self.label_2.setText(_translate("NewOrder", "Наименование"))
        self.addProduct.setToolTip(_translate("NewOrder", "Добавить новый продукт"))
        self.addProduct.setText(_translate("NewOrder", "..."))
        self.clipboardToTable.setText(_translate("NewOrder", "Вставить из буфера обмена"))
        self.groupBox_2.setTitle(_translate("NewOrder", "Вставьте элементы из таблицы Excel"))
        self.textfieldToTable.setText(_translate("NewOrder", "Перенести в таблицу"))
        self.clearTextfield.setText(_translate("NewOrder", "Очистить поле"))
        self.label.setText(_translate("NewOrder", "Заказчик"))
        self.addPartner.setText(_translate("NewOrder", "..."))
        self.label_4.setText(_translate("NewOrder", "Предполагаемая дата отгрузки"))
        self.label_5.setText(_translate("NewOrder", "Номер платежного документа"))
        self.label_6.setText(_translate("NewOrder", "Примечание"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewOrder = QtWidgets.QWidget()
    ui = Ui_NewOrder()
    ui.setupUi(NewOrder)
    NewOrder.show()
    sys.exit(app.exec_())