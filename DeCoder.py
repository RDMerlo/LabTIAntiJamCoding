#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Подключаемые модули

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import sys
# импорт сгенерированной фармы
from QtFormDeCoder import Ui_MainWindow
# и функционала
import InterferenceProofCoding as ipc

# Функции

def attention0():
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle('Информация')
    msg.setText('Нажмите кнопку "Шаг 1: Установка параметров"!')
    msg.setDetailedText('Установка параметров кодирования.')
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()
    pass

def attention1(tParam):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle('Информация')
    msg.setText('Параметр ' + tParam + ' должен быть натуральным числом!')
    msg.setDetailedText('Целое число, большее 0.')
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()
    pass

def attention2(tParam):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle('Информация')
    msg.setText('"Элемент строки ' + tParam +' - бит!')
    msg.setDetailedText('Цифра 0 или 1.')
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()
    pass

# Классы
class cWindow(QtWidgets.QMainWindow):

    def __init__(self):
        # Дополнительные настройки формы
        super(cWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(ipc.listMethod)
        self.ui.comboBox.setCurrentIndex(ipc.nMethodHamming)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        self.ui.tableWidget1.setRowCount(1)
        self.ui.tableWidget1.setColumnCount(0)
        self.ui.tableWidget2.setRowCount(1)
        self.ui.tableWidget2.setColumnCount(0)
        self.ui.tableWidget3.setRowCount(1)
        self.ui.tableWidget3.setColumnCount(0)
        # подключение сигнала к слоту comboBox
        self.ui.comboBox.currentIndexChanged.connect(self.selectionChange)
        # подключение клик-сигнала к слоту btn1Clicked
        self.ui.pushButton1.clicked.connect(self.btn1Clicked)
        # подключение клик-сигнала к слоту btn2Clicked
        self.ui.pushButton2.clicked.connect(self.btn2Clicked)
        # подключение клик-сигнала к слоту btn3Clicked
        self.cCode = None
        pass

    def selectionChange(self):
        nMethod = self.ui.comboBox.currentIndex()
        # Если выбран Код Хэмминга
        if nMethod == ipc.nMethodHamming:
            self.ui.label3.setText('r = ')
            self.ui.label.setText('Матрица M (n x r)')
        # Если выбран Квазисовершенный код
        elif nMethod == ipc.nMethodQuasiPerfect:
            self.ui.label3.setText('k = ')
            self.ui.label.setText('Матрица M (n x k)')
        pass

    def btn1Clicked(self):
        # Прочитаем выбранный метод кодирования
        nMethod = self.ui.comboBox.currentIndex()
        # Если выбран Код Хэмминга
        if nMethod == ipc.nMethodHamming:
            tParam = 'r'
            lE = self.ui.lineEdit3
        # Если выбран Квазисовершенный код
        elif nMethod == ipc.nMethodQuasiPerfect:
            tParam = 'm'
            lE = self.ui.lineEdit1
        # Прочитаем параметр tParam
        try:
            iParam = int(lE.text().strip())
            if iParam < 1:
                attention1(tParam)
                iParam = 1
        except ValueError:
            attention1(tParam)
            # Если выбран Код Хэмминга
            if nMethod == ipc.nMethodHamming:
                iParam = 3 # Значение по умолчанию
            # Если выбран Квазисовершенный код
            elif nMethod == ipc.nMethodQuasiPerfect:
                iParam = 9 # Значение по умолчанию
        # Установка параметров кодирования
        # Если выбран Код Хэмминга
        if nMethod == ipc.nMethodHamming:
            self.cCode = ipc.clsCode(nMethod, rk=iParam)
        # Если выбран Квазисовершенный код
        elif nMethod == ipc.nMethodQuasiPerfect:
            self.cCode = ipc.clsCode(nMethod, m=iParam)
        # Запишем параметры кодирования
        self.ui.lineEdit1.setText(str(self.cCode.m))
        self.ui.lineEdit2.setText(str(self.cCode.n))
        self.ui.lineEdit3.setText(str(self.cCode.rk))
        # Запишем матрицу M
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setColumnCount(self.cCode.rk)
        self.ui.tableWidget.setRowCount(self.cCode.n)
        for i in range(self.cCode.n):
            for k in range(self.cCode.rk):
                cellInfo = QtWidgets.QTableWidgetItem(str(self.cCode.M[i,k]))
                cellInfo.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ui.tableWidget.setItem(i, self.cCode.rk-(k+1), cellInfo)
        # Очистим строкy b + e
        self.ui.tableWidget1.clearContents()
        self.ui.tableWidget1.setColumnCount(self.cCode.n)
        for k in range(self.cCode.n):
            cellInfo = QtWidgets.QTableWidgetItem('')
            cellInfo.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget1.setItem(0, k, cellInfo)
        # Очистим позицию ошибки (b + e) x M
        self.ui.lineEdit.setText('')
        # Очистим строкy b
        self.ui.tableWidget2.clearContents()
        self.ui.tableWidget2.setColumnCount(self.cCode.n)
        for k in range(self.cCode.n):
            cellInfo = QtWidgets.QTableWidgetItem('')
            cellInfo.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget2.setItem(0, k, cellInfo)
        # Очистим строкy a
        self.ui.tableWidget3.clearContents()
        self.ui.tableWidget3.setColumnCount(self.cCode.m)
        for k in range(self.cCode.m):
            cellInfo = QtWidgets.QTableWidgetItem('')
            cellInfo.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget3.setItem(0, k, cellInfo)
        pass

    def btn2Clicked(self):
        # Если установка параметров кодирования не произведена
        if self.cCode == None:
            attention0()
            return
        # Прочитаем строку c = b + e
        c = []
        for k in range(self.cCode.n):
            try:
                i = int(self.ui.tableWidget1.item(0, k).text().strip())
                if not (i in [0,1]):
                    attention2('b + e')
                    i = 0 # Значение по умолчанию
            except ValueError:
                attention2('b + e')
                i = 0 # Значение по умолчанию
            finally:
                c.append(i)
        # Запишем строкy с = b + e
        self.ui.tableWidget1.clearContents()
        self.ui.tableWidget1.setColumnCount(self.cCode.n)
        for k in range(self.cCode.n):
            cellInfo = QtWidgets.QTableWidgetItem(str(c[k]))
            cellInfo.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget1.setItem(0, k, cellInfo)
        # Вычислим позицию ошибки (b + e) x M,
        # строки b и a
        err, b, a = self.cCode.makeDeCode(c)
        # Запишем позицию ошибки (b + e) x M
        self.ui.lineEdit.setText(str(err))
        # Запишем строкy b
        self.ui.tableWidget2.clearContents()
        self.ui.tableWidget2.setColumnCount(self.cCode.n)
        for k in range(self.cCode.n):
            cellInfo = QtWidgets.QTableWidgetItem(str(b[k]))
            cellInfo.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget2.setItem(0, k, cellInfo)
        # Запишем строкy a
        self.ui.tableWidget3.clearContents()
        self.ui.tableWidget3.setColumnCount(self.cCode.m)
        for k in range(self.cCode.m):
            cellInfo = QtWidgets.QTableWidgetItem(str(a[k]))
            cellInfo.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.tableWidget3.setItem(0, k, cellInfo)
        return

# -*- Main -*-

app = QtWidgets.QApplication([])
application = cWindow()
application.show()
sys.exit(app.exec())
