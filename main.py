from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QDate, QDateTime

# Импорт классов из классов интерфейса
from main_window import *
from new_order import *
from new_product import *
from products_reference import *
from all_orders import *
from clients_reference import *
from new_client import *

import pymysql as MySQLdb # Импорт mysql
import re # Импорт методов работы с регулярными выражениями
import logging # Импорт методов для логирования при отладке

logging.basicConfig(level=logging.DEBUG, format = ' %(asctime)s - %(levelname)s - %(message)s')

# Вывод сообщения об ошибке во всплывающем окне
def error(message):
    error = QtWidgets.QMessageBox()
    error.setWindowTitle("Ошибка ввода данных")
    error.setText(message)
    error.setIcon(QtWidgets.QMessageBox.Warning)
    error.setStandardButtons(QtWidgets.QMessageBox.Close)
    # error.setInformativeText() # Дополнительный текст
    # error.setDetailedText() # Расширенное описание ошибки в раскрывающемся списке
    error.exec_()

# проверка строки на число
def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

# Соединение с MySQL
def dbconnect():
   try:
       db = MySQLdb.connect(host="localhost", user="root", passwd="latrom", db="smit", cursorclass=MySQLdb.cursors.DictCursor)
       logging.debug('Соединение с БД установлено')
   except MySQLdb.Error as e:
       error("Ошибка соединения с БД %d: %s" % (e.args[0], e.args[1]))
       sys.exit()
   return db


# Главное окно
class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Обработчики нажатий кнопок в главном окне
        self.ui.toolButtonNewOrder.clicked.connect(self.newOrderOpen) # Нажатие на кнопку Новый заказ
        self.ui.toolButtonAllOrders.clicked.connect(self.allOrdersOpen) # Нажатие на кнопку Все заказы

        # Обработчики нажатия меню
        self.ui.menuNewOrder.triggered.connect(self.newOrderOpen)  # Заказы -> Создать новый заказ
        self.ui.menuAllOrders.triggered.connect(self.allOrdersOpen)  # Заказы -> Создать новый заказ

        self.ui.menuProducts.triggered.connect(self.productsReferenceOpen)  # Справочники -> Производимая продукция
        self.ui.menuClients.triggered.connect(self.clientsReferenceOpen)  # Справочники -> Контрагенты


    # Открытие окна Добавление нового заказа
    def newOrderOpen(self):
        global newOrder
        newOrder = NewOrder(self)
        newOrder.show()

    # Открытие окна Все заказы
    def allOrdersOpen(self):
        global allOrders
        allOrders = AllOrders(self)
        allOrders.show()

    # Открытие окна Справочник производимой продукции
    def productsReferenceOpen(self):
        global prodRef
        prodRef = ProductsReference(self)
        prodRef.show()

    # Открытие окна Справочник контрагентов
    def clientsReferenceOpen(self):
        global clientRef
        clientRef = ClientsReference(self)
        clientRef.show()

# Класс окна Создание нового заказа
class NewOrder(QtWidgets.QWidget):
    def __init__(self, parent=MyWin, editStatus = [False, -1, -1]):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = Ui_NewOrder()
        self.ui.setupUi(self)
        self.setWindowModality(2)
        self.table_index = 0
        self.invalid_elements = list() # Есть ли некорректные данные в таблице? False - нет, True - есть
        # Определяем режим использования - для создания или для редактирования
        self.editStatus, self.editCell, self.editID = editStatus

        # Если окно для редактирования заявки, то меняем название заголовка окна и кнопки Создать на Изменить
        if self.editStatus == True:
            self.setWindowTitle('Редактирование заявки')
            self.ui.getOrder.setText('Изменить')
            print("!!!!! проверка = ", self.editCell)


        # Загружаем данные из таблицы для выпадающего списка Контрагенты
        try:
            cursor.execute("SELECT * FROM clients_reference")
            self.products = cursor.fetchall()
        except:
            error("Ошибка получения данных из БД в модуле загрузки данных о продукции для выпадающего списка")
            sys.exit()

        # Заполняем выпадающий список Наименование данными
        self.ui.partnersList.addItem('')  # Первый элемент пустой
        for r in self.products:
            self.ui.partnersList.addItem(r['name'])


        # Загружаем данные из таблицы для выпадающего списка Наименование
        try:
            cursor.execute("SELECT * FROM products_reference")
            self.products = cursor.fetchall()
        except:
            error("Ошибка получения данных из БД в модуле загрузки данных о продукции для выпадающего списка")
            sys.exit()

        # Заполняем выпадающий список Наименование данными
        self.ui.comboBox.addItem('') # Первый элемент пустой
        for r in self.products:
            self.ui.comboBox.addItem(r['name'])

        # Заполняем словарь patterns данными о продукте {'Регулярное выражение':'Заводское наименование'}
        self.patterns = dict()
        for r in self.products:
            self.patterns.setdefault(r['regexp'], r['name'])
        logging.debug('Словарь регулярных выражений patterns = %s%%' % (self.patterns))

        # Устанавливаем дату отгрузки
        if self.editStatus == False:
            self.ui.dateEdit.setDate(QDate.currentDate()) # Текущая дата

        # кнопка удалить в ячейках таблицы
        self.del_row = QtWidgets.QPushButton()
        self.del_row.setText("Удалить")
        self.del_row.clicked.connect(self.delRow) # При нажатии запускаем метод delRow

        #Обработчики нажатий кнопок в окне Создание нового заказа
        self.ui.textfieldToTable.clicked.connect(self.addFromTextFieldToTable)  # Нажатие на кнопку Перенести в таблицу
        self.ui.clearTextfield.clicked.connect(self.textfieldClear)  # Нажатие на кнопку Очистить поле

        self.ui.clipboardToTable.clicked.connect(self.addFromClipboardToTable)  # Нажатие на кнопку Вставить из буфера обмена
        self.ui.clearTable.clicked.connect(self.tableClear)  # Нажатие на кнопку Очистить таблицу
        
        self.ui.addelemToTable.clicked.connect(self.addFromComboBoxToTable)  # Нажатие на кнопку Добавить элемент
        self.ui.getOrder.clicked.connect(self.addOrder)  # Нажатие на кнопку принять заказ
        self.ui.addProduct.clicked.connect(self.addProd)  # Нажатие на кнопку + добавить продукт
        self.ui.addPartner.clicked.connect(self.addClient)  # Нажатие на кнопку + добавить контрагента

        self.ui.newOrderTable.doubleClicked.connect(self.check_change) # Проверка изменений в ячейке

    # Добавить продукт
    def addProd(self):
        global newProduct
        newProduct = NewProduct(self)
        newProduct.show()
        
    # Добавить клиента
    def addClient(self):
        global newClient
        newClient = NewClient(self)
        newClient.show()    

    # Очищаем текстовое поле
    def textfieldClear(self):
        self.ui.textfieldOrder.clear()

    # очищаем таблицу
    def tableClear(self):
        logging.debug("Очищаем таблицу")
        self.ui.newOrderTable.clear()
        self.ui.newOrderTable.setRowCount(0);
        self.ui.newOrderTable.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Товар'))
        self.ui.newOrderTable.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Количество'))
        self.ui.newOrderTable.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Удалить'))
        self.table_index = 0
        self.invalid_elements.clear()

    # Добавляем все данные из текстового поля в таблицу
    def addFromTextFieldToTable(self):
        text = self.ui.textfieldOrder.toPlainText()
        self.checkData(text)
    
    # Добавляем данные из комбо-бокса Наименование-количество в таблицу
    def addFromComboBoxToTable(self):
        if True in self.invalid_elements:
            error('В таблице есть неизвестные элементы, перед добавлением требуется исправить')
        else:
            err = ''
            # кнопка удалить в ячейках таблицы
            del_row = QtWidgets.QPushButton()
            del_row.setText("Удалить")
            del_row.clicked.connect(self.delRow)  # При нажатии запускаем метод delRow

            if self.ui.comboBox.currentText() == '':
                err +='Не выбран элемент\n'
            if self.ui.spinBox.value() == 0:
                err +='Не указано количество\n'
            if err != '':
                error(err)
            else:
                # Если все правильно, добавляем элемент в таблицу
                numsOfProd = self.ui.spinBox.value()

                self.add_status = False # Флаг, есть ли элемент в таблице, чтобы просто добавить количество

                # Проверяем, если таблица пустая, то сразу добавляем запись
                if self.table_index > 0:
                    i = 0
                    while i < self.table_index:
                        # Если такая запись существует, то добавляем количество
                        if self.ui.newOrderTable.item(i,0).text() == self.ui.comboBox.currentText():
                            self.ui.newOrderTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(numsOfProd+int(self.ui.newOrderTable.item(i,1).text()))))
                            self.ui.newOrderTable.setCellWidget(i, 2, del_row)
                            self.add_status = True
                        i +=1
                    if not self.add_status:
                       # Если нет, то вносим новую запись
                        logging.debug('self.table_index = '+str(self.table_index))
                        self.ui.newOrderTable.setRowCount(i+1)  # добавляем строку в таблицу
                        self.ui.newOrderTable.setItem(self.table_index, 0, QtWidgets.QTableWidgetItem(self.ui.comboBox.currentText()))
                        self.ui.newOrderTable.setItem(self.table_index, 1, QtWidgets.QTableWidgetItem(str(numsOfProd)))
                        self.ui.newOrderTable.setCellWidget(self.table_index, 2, del_row)
                        self.table_index += 1
                        self.invalid_elements.append(False)
                else:
                    # Если нет, то вносим новую запись
                    self.ui.newOrderTable.setRowCount(self.table_index+1)  # добавляем строку в таблицу
                    self.ui.newOrderTable.setItem(self.table_index, 0, QtWidgets.QTableWidgetItem(self.ui.comboBox.currentText()))
                    self.ui.newOrderTable.setItem(self.table_index, 1, QtWidgets.QTableWidgetItem(str(numsOfProd)))
                    self.ui.newOrderTable.setCellWidget(self.table_index, 2, del_row)
                    self.table_index += 1
                    self.invalid_elements.append(False)
        logging.debug('invalid_elements = %s%%' % (self.invalid_elements))
        self.ui.newOrderTable.resizeColumnsToContents()

    # Добавляем данные из буфера обмена в таблицу
    def addFromClipboardToTable(self):
        self.invalid_elements.clear()
        clipboard = QtWidgets.QApplication.clipboard()
        text = clipboard.text()
        self.checkData(text)

    # Проверка корректности данных и добавление их в таблицу
    def checkData(self, text):
        text = text.strip('\n')

        if len(text) == 0:
            error("Нет данных для записи в таблицу")
        else:
            table = [t for t in text.split('\t')]

            # Удаляем пустые ячейки
            newtable = []
            for cell in table:
                if cell != '':
                    cell = cell.strip('\n')  # Удаляем символ \n
                    newtable.append(cell)
            logging.debug("newtable = %s%%" % newtable)

            # Проверяем, все ли строки соответствуют шаблону "Наименование, Количество"
            dataok = True
            if len(newtable) % 2 != 0:
                error('Недостаточно данных для переноса в таблицу')
                dataok = False
            else:
                i = 0
                while i < len(newtable):
                    logging.debug(str(newtable[i])+' '+str(newtable[i + 1]))
                    if newtable[i] == '' or newtable[i + 1] == '' or not newtable[i + 1].isdigit():

                        error('Недостаточно данных для переноса в таблицу в строке {}'.format(i + 1))
                        dataok = False
                        break
                    i += 2
            if dataok:
                logging.debug('Данные полные')
                self.table_index = 0
                self.ui.newOrderTable.setRowCount(int(len(newtable) / 2))  # Сколько строк будет в таблице

                # Заполняем таблицу данными
                i = 0
                while i < len(newtable):
                    # Проверка соответствия введенного названия с заводским
                    # checkRegEx(newtable[i]) возвращает заводское наименование или Не удалось идентифицировать элемент
                    logging.debug("Передаем в checkRegEx %s%%" % (newtable[i]))

                    # кнопка удалить в ячейках таблицы
                    del_row = QtWidgets.QPushButton()
                    del_row.setText("Удалить")
                    del_row.clicked.connect(self.delRow)  # При нажатии запускаем метод delRow

                    insert_name = self.checkRegEx(newtable[i])
                    self.ui.newOrderTable.setItem(self.table_index, 0, QtWidgets.QTableWidgetItem(insert_name))
                    #self.ui.newOrderTable.setItem(self.table_index, 0, QtWidgets.QTableWidgetItem(newtable[i])) # Если заменить строку на предыдущую, то надпись будет заменена, но это не удобно
                    self.ui.newOrderTable.setItem(self.table_index, 1, QtWidgets.QTableWidgetItem(newtable[i + 1]))
                    self.ui.newOrderTable.setCellWidget(self.table_index, 2, del_row)

                    if insert_name == 'Не удалось идентифицировать элемент':
                        self.ui.newOrderTable.item(self.table_index, 0).setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
                        self.invalid_elements.append(True)
                    else:
                        self.invalid_elements.append(False)
                    i += 2
                    self.table_index += 1

                self.ui.newOrderTable.resizeColumnsToContents()
                logging.debug('Таблица заполнена')
                logging.debug('invalid_elements = %s%%' % (self.invalid_elements))

    # Удаляем строку из таблицы
    def delRow(self):
        button = self.sender()
        row = self.ui.newOrderTable.indexAt(button.pos()).row()
        self.ui.newOrderTable.removeRow(row)
        self.table_index -=1
        self.invalid_elements.pop(row)
        logging.debug('invalid_elements = %s%%' % (self.invalid_elements))

    # Подключаем слот проверки изменений внутри ячейки
    def check_change(self):
        self.ui.newOrderTable.cellChanged.connect(self.check_cell)  # Проверка изменений в ячейке
        logging.debug('Слот включен')

    # Проверяем, соответствуют ли измененные в ячейке данные, данным в регулярных выражениях
    # Если Да, то изменяем цвет ячейки на белый и указываем корректное название
    def check_cell(self):
        logging.debug("Ячейку изменили")
        self.ui.newOrderTable.cellChanged.disconnect(self.check_cell)  # Отключаем сигнал, чтобы он не дублировался трижды

        cell = self.ui.newOrderTable.currentItem()
        if cell.column() == 0: #Проверяем ячейку только если она в колонке 0 (Название продукта)
            insert_name = self.checkRegEx(cell.text())
            logging.debug(cell.text())
            if insert_name !='Не удалось идентифицировать элемент':
                self.ui.newOrderTable.currentItem().setText(insert_name)
                self.ui.newOrderTable.currentItem().setBackground(QtGui.QBrush(QtGui.QColor(Qt.white)))
                self.invalid_elements[cell.row()] = False # Данные соответствуют регуляркам
            else:
                #Если раскомментировать, то текст пропадет, но это не удобно
                #self.ui.newOrderTable.currentItem().setText('Не удалось идентифицировать элемент')
                self.ui.newOrderTable.currentItem().setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
                self.invalid_elements[cell.row()] = True # Есть несоответствующие регуляркам данные
        logging.debug('invalid_elements = %s%%' % (self.invalid_elements))

    # Проверка данных на соответствие регулярным выражениям
    def checkRegEx(self, elem):
        key = 0
        for k in self.patterns.keys():
            print('k = ', k, 'key =', key, 'text lower = ', elem.lower(), re.search(k, elem.lower()))
            if re.search(str(k), str(elem.lower())):
                key += 1
                return self.patterns[k]
        if key == 0:
            return 'Не удалось идентифицировать элемент'

    # Сохраняем заявку в БД
    def addOrder(self):
        # Блок проверок
        err = ''
        print('self.ui.dateEdit.text() = ', self.ui.dateEdit.text())
        inputedDate = QDate.fromString(self.ui.dateEdit.text(),"dd.MM.yyyy")
        currentDate = QDate.currentDate()

        if True in self.invalid_elements:
            err += 'В заказе есть неизвестные элементы. Исправьте\n'
        if self.ui.partnersList.currentText() == '':
            err += 'Не выбран контрагент\n'
        if inputedDate < currentDate:
            err += 'Дата отгрузки меньше, чем текущая дата\n'
        if self.ui.newOrderTable.rowCount() <1:
            err += 'Нет продуктов для сохранения заявки'

        if len(err) >0:
            print('inputedDate = ', inputedDate.toString())
            print('currentDate = ', currentDate.toString())
            error(err)
        # Если все проверки пройдены, сохраняем
        else:
            # Сохраняем запись о заявке в таблицу orders

            # Определяем id клиента
            client_name = self.ui.partnersList.currentText()

            try:
                cursor.execute("SELECT * FROM clients_reference WHERE name='" + client_name + "'")
                res = cursor.fetchall()
            except:
                print("Error")
                sys.exit()

            client_id = res[0]['id']
            document_number = self.ui.lineEdit.text()
            more = self.ui.textEdit.toPlainText()

            if self.editStatus == False: # Если не редактирование, то сохраняем новую запись в таблицу orders
                try:
                    # (partner_id, make_date, document_number, more, status)
                    query = "INSERT INTO orders (partner_id, make_date, document_number, more, status) VALUES ({}, '{}', '{}', '{}', '1')".format(client_id, inputedDate.toString('dd.MM.yyyy'), document_number, more)

                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                except db.Error as e:
                    error("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit()

                order_id = cursor.lastrowid
                print('id последней записи в таблицу orders = ', order_id)
            else:
                try:
                    # (partner_id, make_date, document_number, more, status)
                    query = "UPDATE orders SET partner_id = {}, make_date = '{}', document_number = '{}', more = '{}' WHERE id = {}".format(client_id, inputedDate.toString('dd.MM.yyyy'), document_number, more, self.editID)
                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                except db.Error as e:
                    error("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit()


            # Cохраняем список продукции
            print('Строк в таблице = ',self.ui.newOrderTable.rowCount())

            rows = 0
            while rows < self.ui.newOrderTable.rowCount():
                # Читаем строку в таблице
                product_name = self.ui.newOrderTable.item(rows, 0).text()
                product_count = self.ui.newOrderTable.item(rows, 1).text()

                # Получаем id продукта
                try:
                    cursor.execute("SELECT * FROM products_reference WHERE name='"+product_name+"'")
                    res = cursor.fetchall()
                except:
                    print("Error")
                    sys.exit()

                product_code = res[0]['code']
                print(product_code, product_name, product_count)
                # Сохраняем запись в таблицу products_in_orders
                # (order_id, product_code, col, client_id)
                try:
                    query = "INSERT INTO products_in_orders (order_id, product_code, col, client_id) VALUES ({}, '{}', {}, {})".format(order_id, product_code,
                                                                                           product_count, client_id)
                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                except db.Error as e:
                    error("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit()
                rows+=1

            # Если список сохранен успешно
            error('Заказ принят!')
            self.hide()

# Класс окна Обработка заявки (редактирование и отправка в производство)
class AllOrders(QtWidgets.QWidget):
    def __init__(self, parent=MyWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = Ui_AllOrders()
        self.ui.setupUi(self)
        self.setWindowModality(2)
        self.init()

        # Обработчики нажатий кнопок в окне Все заявке
        self.ui.newOrder.clicked.connect(self.newOrder)  # Нажатие на кнопку Новая заявка
        self.ui.editOrder.clicked.connect(self.editOrder)  # Нажатие на кнопку Редактировать заявку
        self.ui.toFactory.clicked.connect(self.toFactory)  # Нажатие на кнопку В производство
        self.ui.stopOrder.clicked.connect(self.stopOrder)  # Нажатие на кнопку Остановить заявку

    def init(self):
        # Читаем из таблицы orders данные для заполнения таблицы справочника
        try:
            cursor.execute("SELECT * FROM orders ORDER BY id DESC")
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()

        if len(res) > 0:
            self.table_index = 0
            self.table_rows = len(res)
            self.ui.ordersTable.setRowCount(self.table_rows)  # Строк в таблице

            for row in res:
                print(row['date'], type(row['partner_id']), row['make_date'])
                # Получаем данные о контрагенте
                q = "SELECT * FROM clients_reference WHERE id = " + str(row['partner_id'])
                print(q)
                try:
                    #q = "SELECT * FROM clients_reference WHERE id = "+row['partner_id']
                   # print(q)
                    cursor.execute(q)
                    cl = cursor.fetchall()
                except:
                    print("Error")
                    sys.exit()

                self.ui.ordersTable.setItem(self.table_index, 0, QtWidgets.QTableWidgetItem(QDate(row['date']).toString("dd.MM.yyyy")))
                self.ui.ordersTable.setItem(self.table_index, 1, QtWidgets.QTableWidgetItem(QDateTime(row['date']).time().toString("hh:mm:ss")))
                self.ui.ordersTable.setItem(self.table_index, 2, QtWidgets.QTableWidgetItem(cl[0]['name']))
                self.ui.ordersTable.setItem(self.table_index, 3, QtWidgets.QTableWidgetItem(cl[0]['city']))

                self.table_index += 1

            # Запрет редактирования всей таблицы чтобы не было желания изменить внутри текст
            self.ui.ordersTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            # Подгоняем столбцы под размер содержимого
            self.ui.ordersTable.resizeColumnsToContents()

    def newOrder(self):
        global newOrder
        newOrder = NewOrder(self)
        newOrder.show()

    def editOrder(self):
        cell = self.ui.ordersTable.currentItem()
        print('Выделена строка ', cell.row())

        # Загружаем данные из таблицы для выбранной заявки

        # Формируем дату+время для datetime
        dt1 = self.ui.ordersTable.item(cell.row(), 0).text() + ' ' + self.ui.ordersTable.item(cell.row(), 1).text()
        dt2 = QDateTime.fromString(dt1, 'dd.MM.yyyy hh:mm:ss')
        find_data = dt2.toString('yyyy-MM-dd hh:mm:ss')
        print('datetime ', find_data)
        
        try:
            cursor.execute("SELECT * FROM orders WHERE date = '" + find_data+"'")
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()
        print('res = ', res)

        editOrder = NewOrder(self, [True, cell.row(), res[0]['id']])

        # Устанавливаем значения полей в объекте editOrder
        editOrder.ui.partnersList.setCurrentIndex(int(res[0]['partner_id'])) # Список контрагентов
        editOrder.ui.dateEdit.setDate(QDate.fromString(res[0]['make_date'],'dd.MM.yyyy')) # Предполагаемая дата отгрузки
        print(QDate.fromString(res[0]['make_date'],'dd.MM.yyyy'))
        editOrder.ui.lineEdit.setText(str(res[0]['document_number'])) # Номер документа
        editOrder.ui.textEdit.setPlainText(res[0]['more']) # Примечание

        # Заполняем таблицу данными о продукции из заявки
        query = "SELECT * FROM products_in_orders WHERE order_id = " + str(res[0]['id'])
        print(query)
        try:
            cursor.execute(query)
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()

        print('res = ', res)
        text = ''
        for r in res:
            # Определяем название продукта из справочника
            query = "SELECT * FROM products_reference WHERE code = '" + str(r['product_code']+"'")
            print(query)
            try:
                cursor.execute(query)
                query = cursor.fetchall()
            except:
                print("Error")
                sys.exit()

            text+=query[0]['name']+'\t'+str(r["col"])+'\t'

        print(text)

        editOrder.checkData(text)
        editOrder.show()



    def toFactory(self):
        pass

    def stopOrder(self):
        pass







# Класс окна Справочник производимой продукции
class ProductsReference(QtWidgets.QWidget):
    def __init__(self, parent=MyWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = Ui_ProductsReference()
        self.ui.setupUi(self)
        self.setWindowModality(2)
        self.init()

        # Обработчики нажатий кнопок в Справочнике производимой продукции
        self.ui.addNewProduct.clicked.connect(self.newProductOpen) # Нажатие на кнопку Новый продукт
        self.ui.editProduct.clicked.connect(self.editProduct) # Нажатие на кнопку Редактировать

    def init(self):
        # Читаем из таблицы products_reference данные для заполнения таблицы справочника
        try:
            cursor.execute("SELECT * FROM products_reference")
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()

        if len(res) > 0:
            self.table_index = 0
            self.table_rows = len(res)
            self.ui.productTable.setRowCount(self.table_rows)  # Строк в таблице

            for row in res:
                print(row['code'], row['name'], row['weight'], row['regexp'], row['make'])
                self.ui.productTable.setItem(self.table_index, 0, QtWidgets.QTableWidgetItem(row['code']))
                self.ui.productTable.setItem(self.table_index, 1, QtWidgets.QTableWidgetItem(row['name']))
                self.ui.productTable.setItem(self.table_index, 2, QtWidgets.QTableWidgetItem(str(row['weight'])))

                self.table_index += 1

            # Запрет редактирования всей таблицы чтобы не было желания изменить внутри текст
            self.ui.productTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            # Подгоняем столбцы под размер содержимого
            self.ui.productTable.resizeColumnsToContents()



    def editProduct(self):
        print('Нажали кнопку')
        cell = self.ui.productTable.currentItem()
        print('Выделена строка ', cell.row())
        cod = self.ui.productTable.item(cell.row(), 0).text()
        print('Код ', cod)
        editProd = NewProduct(self, [True, cell.row()] )

        # Устанавливаем значения полей в объекте editProd
        # Загружаем данные из таблицы для выбранного продукта
        try:
            cursor.execute("SELECT * FROM products_reference WHERE code = '"+cod+"'")
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()
        print('res = ', res)
     
        editProd.ui.newProductName.setText(res[0]['name'])
        editProd.ui.newProductCode.setText(res[0]['code'])
        editProd.ui.newProductWeight.setText(str(res[0]['weight']))
        editProd.ui.newProductRegExp.setText(res[0]['regexp'])
        editProd.ui.newProductAbout.setPlainText(res[0]['about'])
        editProd.ui.newProductType.setCurrentIndex(int(res[0]['type']))
   
        editProd.show()

    def newProductOpen(self):
        global newProduct
        newProduct = NewProduct(self)
        newProduct.show()


# Класс окна Создание нового продукта
# Также используется для редактирования продукта

class NewProduct(QtWidgets.QWidget):
    def __init__(self, parent=ProductsReference, editStatus = [False, -1]):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = Ui_NewProduct()
        self.ui.setupUi(self)
        self.setWindowModality(2)
        # Определяем режим использования - для создания или для редактирования
        self.editStatus, self.editCell = editStatus

        # Если окно для редактирования, то меняем название заголовка окна и кнопки Создать на Изменить
        if self.editStatus == True:
            self.setWindowTitle('Редактирование информации о продукте')
            self.ui.createNewProduct.setText('Изменить')
            # А также запрещаем редактирование некоторых полей
            # это делается для того, чтобы уникальное поле Код и Регулярное выражение никто случайно не сбил
            self.ui.newProductCode.setDisabled(True)
            self.ui.newProductRegExp.setDisabled(True)

        logging.debug('editStatus = %s%%' % self.editStatus)
        logging.debug('editCell = %s%%' % self.editCell)
        # Обработчики нажатий кнопок в окне Создание нового продукта
        self.ui.createNewProduct.clicked.connect(self.createNewProduct) # Нажатие на кнопку Создать
        
    def createNewProduct(self):
        productname     = self.ui.newProductName.text().strip()
        productcode     = self.ui.newProductCode.text().strip()
        productweight   = self.ui.newProductWeight.text().strip()
        productregexp   = self.ui.newProductRegExp.text().strip()
        productabout    = self.ui.newProductAbout.toPlainText().strip()
        producttypetext = self.ui.newProductType.currentText()

        # Можно заменить на получение текущего индекса, но сейчас сделано для наглядности
        if producttypetext != '':
            if producttypetext == 'Клей':
                producttype = 1
            elif producttypetext == 'Состав для механизированного нанесения':
                producttype = 2
            elif producttypetext == 'Финишный состав':
                producttype = 3
            elif producttypetext == 'Выравнивающий состав':
                producttype = 4
        else:
            producttype = 0

        # Проверка корректности заполнения всех полей формы
        err = ''
        # Загружаем данные из таблицы для проверки значений на уникальность
        try:
            cursor.execute("SELECT * FROM products_reference")
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()

        if len(productname) == 0:
            err += 'Имя продукта должно быть заполнено\n'
        if len(productcode) == 0:
            err += 'Поле Код продукта должно быть заполнено\n'
        if len(productweight) == 0:
            err += 'Поле Вес должно быть заполнено\n'
        if is_digit(productweight)!= True:
            err += 'Поле Вес должно быть числом\n'
        if is_digit(productweight)== True and float(productweight) > 50:
           err += 'В поле Вес слишком большая величина\n'
        if len(productregexp) == 0:
            err += 'Поле RegExp должно быть заполнено\n'
        if len(productabout) == 0:
            err += 'Поле Описание назначения продукта должно быть заполнено\n'
        if producttypetext == '':
            err += 'Поле Вид не выбрано\n'

        # Проверяем уникальность вводимых значений с данными из базы
        for r in res:
            print(r)
            print(r.values())
            if productname in r.values() and self.editStatus == False:
                err += 'Имя продукта не уникально\n'
            if not self.editStatus:
                if productregexp in r.values():
                    err += 'Регулярное выражение не уникально\n'
                if productcode in r.values():
                    err += 'Код продукта не уникален\n'

        logging.debug(err)
        if len(err) != 0:
            error(err)
        else:
            if not self.editStatus:
                # Если статус - новый
                # Записываем в таблицу products_reference новый продукт
                try:
                    # (code, name, weight, regexp, make)
                    query = "INSERT INTO products_reference VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '1')".format(productcode, productname, productweight, productregexp, producttype, productabout)
                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                except db.Error as e:
                    error("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit()
            else:
                # Если статус - редактирование
                # Обновляем таблицу products_reference
                try:
                    # (code, name, weight, regexp, make)
                    query = "UPDATE products_reference SET name = '{}', weight = {}, type = {}, about = '{}' WHERE code = '{}'".format(productname, productweight, producttype, productabout, productcode)
                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                except db.Error as e:
                    error("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit()

            if self.editStatus == False: # Если новая запись, а не редактирование
                # Если открывали окно добавления продукта из Справочника, то
                # добавляем в таблицу Справочник производимой продукции новую запись
                try:
                    prodRef.init()  # Обновление окна Справочник продукции (Заменили нижние 5 строк кода)
                    '''logging.debug('table_rows = %s%%' % prodRef.table_rows)
                    prodRef.ui.productTable.setRowCount(prodRef.table_rows+1)  # Добавляем строку в таблицу
                    prodRef.ui.productTable.setItem(prodRef.table_index, 0, QtWidgets.QTableWidgetItem(productcode))
                    prodRef.ui.productTable.setItem(prodRef.table_index, 1, QtWidgets.QTableWidgetItem(productname))
                    prodRef.ui.productTable.setItem(prodRef.table_index, 2, QtWidgets.QTableWidgetItem(str(productweight)))'''
                except:
                    logging.debug('Добавление продукта было из окна нового заказа')

                # Если открывали окно добавления продукта из окна Создание новой заявки, то
                # добавляем новую регулярку в массив patterns и новое значение в выпадающий список окна Новая заявка
                try:
                    newOrder.patterns.setdefault(productregexp, productname)
                    newOrder.ui.comboBox.addItem(productname)
                    logging.debug('patterns %s%%' % newOrder.patterns)
                except:
                    logging.debug('Добавление продукта было из справочника, а не окна нового заказа')

            else: # Если редактирование
                # то в таблице Справочник продуктов обновляем название на случай, если оно менялось
                prodRef.ui.productTable.setItem(self.editCell, 1, QtWidgets.QTableWidgetItem(productname))

            # Закрываем окно Создание нового продукта
            self.hide()


# Класс окна Справочник контрагентов
class ClientsReference(QtWidgets.QWidget):
    def __init__(self, parent=MyWin):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = Ui_ClientsReference()
        self.ui.setupUi(self)
        self.setWindowModality(2)
        self.init()

        # Обработчики нажатий кнопок в Справочнике производимой продукции
        self.ui.addNewClient.clicked.connect(self.newClientOpen)  # Нажатие на кнопку Новый продукт
        self.ui.editClient.clicked.connect(self.editClient)  # Нажатие на кнопку Редактировать

    def init(self):
        # Читаем из таблицы clients_reference данные для заполнения таблицы справочника
        try:
            cursor.execute("SELECT * FROM clients_reference")
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()

        if len(res) > 0:
            self.table_index = 0
            self.table_rows = len(res)
            self.ui.clientTable.setRowCount(self.table_rows)  # Строк в таблице

            for row in res:
                print(row['id'], row['name'], row['inn'], row['city'], row['short_name'], row['info'])
                self.ui.clientTable.setItem(self.table_index, 0, QtWidgets.QTableWidgetItem(row['inn']))
                self.ui.clientTable.setItem(self.table_index, 1, QtWidgets.QTableWidgetItem(row['name']))
                self.ui.clientTable.setItem(self.table_index, 2, QtWidgets.QTableWidgetItem(str(row['city'])))
                self.table_index += 1

            # Запрет редактирования всей таблицы чтобы не было желания изменить внутри текст
            self.ui.clientTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            # Подгоняем столбцы под размер содержимого
            self.ui.clientTable.resizeColumnsToContents()


    def editClient(self):
        print('Нажали кнопку')
        cell = self.ui.clientTable.currentItem()
        print('Выделена строка ', cell.row())
        inn = self.ui.clientTable.item(cell.row(), 0).text()
        print('ИНН ', inn)
        editClient = NewClient(self, [True, cell.row()])

        # Устанавливаем значения полей в объекте editClient
        # Загружаем данные из таблицы для выбранного продукта
        try:
            cursor.execute("SELECT * FROM clients_reference WHERE inn LIKE '" + inn+"'")
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()
        print('res = ', res)

        editClient.ui.newClientName.setPlainText(res[0]['name'])
        editClient.ui.newClientINN.setText(res[0]['inn'])
        editClient.ui.newClientCity.setText(str(res[0]['city']))
        editClient.ui.newClientShortName.setText(res[0]['short_name'])
        editClient.ui.newClientAbout.setPlainText(res[0]['info'])

        editClient.show()

    def newClientOpen(self):
        global newClient
        newClient = NewClient(self)
        newClient.show()

class NewClient(QtWidgets.QWidget):
    def __init__(self, parent=ProductsReference, editStatus = [False, -1]):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = Ui_NewClient()
        self.ui.setupUi(self)
        self.setWindowModality(2)
        # Определяем режим использования - для создания или для редактирования
        self.editStatus, self.editCell = editStatus

        # Если окно для редактирования, то меняем название заголовка окна и кнопки Создать на Изменить
        if self.editStatus == True:
            self.setWindowTitle('Редактирование информации о клиенте')
            self.ui.createNewClient.setText('Изменить')
            # А также запрещаем редактирование некоторых полей
            # это делается для того, чтобы уникальное поле Код и Регулярное выражение никто случайно не сбил
            self.ui.newClientINN.setDisabled(True)

        logging.debug('editStatus = %s%%' % self.editStatus)
        logging.debug('editCell = %s%%' % self.editCell)
        # Обработчики нажатий кнопок в окне Создание нового продукта
        self.ui.createNewClient.clicked.connect(self.createNewClient)  # Нажатие на кнопку Создать

    def createNewClient(self):
        clientname = self.ui.newClientName.toPlainText().strip()
        clientinn = self.ui.newClientINN.text().strip()
        clientcity = self.ui.newClientCity.text().strip()
        clientshortname = self.ui.newClientShortName.text().strip()
        clientabout = self.ui.newClientAbout.toPlainText().strip()

        # Проверка корректности заполнения всех полей формы
        err = ''
        # Загружаем данные из таблицы для проверки значений на уникальность
        try:
            cursor.execute("SELECT * FROM clients_reference")
            res = cursor.fetchall()
        except:
            print("Error")
            sys.exit()

        if len(clientname) == 0:
            err += 'Наименование клиента должно быть заполнено\n'
        if len(clientinn) == 0:
            err += 'Поле ИНН клиента должно быть заполнено\n'
        if len(clientcity) == 0:
            err += 'Поле Город должно быть заполнено\n'
        if len(clientinn) < 10:
            err += 'ИНН юрлица состоит из 10 знаков\n'

        # Проверяем уникальность вводимых значений с данными из базы
        for r in res:
            print(r)
            print(r.values())
            if not self.editStatus:
                if clientinn in r.values():
                    err += 'ИНН клиента не уникален\n'

        logging.debug(err)
        if len(err) != 0:
            error(err)
        else:
            if not self.editStatus:
                # Если статус - новый
                # Записываем в таблицу clients_reference нового клиента
                try:
                    # (name, inn, city, short_name, info)
                    query = "INSERT INTO clients_reference (name, inn, city, short_name, info) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                        clientname, clientinn, clientcity, clientshortname, clientabout)
                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                except db.Error as e:
                    error("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit()
            else:
                # Если статус - редактирование
                # Обновляем таблицу products_reference
                try:
                    # (name, city, shortname, info)
                    query = "UPDATE clients_reference SET name = '{}', city = '{}', short_name = '{}', info = '{}' WHERE inn = '{}'".format(
                        clientname, clientcity, clientshortname, clientabout, clientinn)
                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                except db.Error as e:
                    error("Error %d: %s" % (e.args[0], e.args[1]))
                    sys.exit()

            if self.editStatus == False:  # Если новая запись, а не редактирование
                # Если открывали окно добавления клиента из Справочника, то
                # добавляем в таблицу Справочник контрагентов новую запись
                try:
                    clientRef.init() # Обновляем таблицу в справочнике контрагентов
                    '''logging.debug('table_rows = %s%%' % clientRef.table_rows)
                    clientRef.ui.clientTable.setRowCount(clientRef.table_rows + 1)  # Добавляем строку в таблицу
                    clientRef.ui.clientTable.setItem(clientRef.table_index, 0, QtWidgets.QTableWidgetItem(clientinn))
                    clientRef.ui.clientTable.setItem(clientRef.table_index, 1, QtWidgets.QTableWidgetItem(clientname))
                    clientRef.ui.clientTable.setItem(clientRef.table_index, 2, QtWidgets.QTableWidgetItem(str(clientcity)))'''
                except:
                    logging.debug('Добавление клиента было из окна нового заказа')
                # Если открывали окно добавления клиента из окна Создание новой заявки, то
                # добавляем новое значение в выпадающий список окна Новая заявка
                try:
                    newOrder.ui.partnersList.addItem(clientname)
                except:
                    logging.debug('Добавление клиента было из справочника, а не окна нового заказа')

            else:  # Если редактирование
                # то в таблице Справочник продуктов обновляем название и город на случай, если они менялись
                clientRef.ui.clientTable.setItem(self.editCell, 1, QtWidgets.QTableWidgetItem(clientname))
                clientRef.ui.clientTable.setItem(self.editCell, 2, QtWidgets.QTableWidgetItem(clientcity))
            # Закрываем окно Создание нового продукта
            self.hide()

if __name__ == "__main__":
    import sys
    db = dbconnect()
    cursor = db.cursor()

    app = QtWidgets.QApplication([])
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())