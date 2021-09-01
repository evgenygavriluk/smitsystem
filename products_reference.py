# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'products_reference.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProductsReference(object):
    def setupUi(self, ProductsReference):
        ProductsReference.setObjectName("ProductsReference")
        ProductsReference.resize(637, 484)
        self.productTable = QtWidgets.QTableWidget(ProductsReference)
        self.productTable.setGeometry(QtCore.QRect(10, 90, 621, 381))
        self.productTable.setColumnCount(3)
        self.productTable.setObjectName("productTable")
        self.productTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.productTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.productTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.productTable.setHorizontalHeaderItem(2, item)
        self.groupBox = QtWidgets.QGroupBox(ProductsReference)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 621, 71))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.addNewProduct = QtWidgets.QToolButton(self.groupBox)
        self.addNewProduct.setGeometry(QtCore.QRect(10, 10, 50, 50))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("venv/icons/new-product.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addNewProduct.setIcon(icon)
        self.addNewProduct.setIconSize(QtCore.QSize(40, 40))
        self.addNewProduct.setObjectName("addNewProduct")
        self.editProduct = QtWidgets.QToolButton(self.groupBox)
        self.editProduct.setGeometry(QtCore.QRect(70, 10, 50, 50))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("venv/icons/edit-product.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editProduct.setIcon(icon1)
        self.editProduct.setIconSize(QtCore.QSize(40, 40))
        self.editProduct.setObjectName("editProduct")

        self.retranslateUi(ProductsReference)
        QtCore.QMetaObject.connectSlotsByName(ProductsReference)

    def retranslateUi(self, ProductsReference):
        _translate = QtCore.QCoreApplication.translate
        ProductsReference.setWindowTitle(_translate("ProductsReference", "Справочник производимой продукции"))
        item = self.productTable.horizontalHeaderItem(0)
        item.setText(_translate("ProductsReference", "Код"))
        item = self.productTable.horizontalHeaderItem(1)
        item.setText(_translate("ProductsReference", "Наименование"))
        item = self.productTable.horizontalHeaderItem(2)
        item.setText(_translate("ProductsReference", "Вес"))
        self.addNewProduct.setText(_translate("ProductsReference", "..."))
        self.editProduct.setText(_translate("ProductsReference", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProductsReference = QtWidgets.QWidget()
    ui = Ui_ProductsReference()
    ui.setupUi(ProductsReference)
    ProductsReference.show()
    sys.exit(app.exec_())