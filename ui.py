# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'base.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(908, 381)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.closed_combobox = QComboBox(self.centralwidget)
        self.closed_combobox.addItem("")
        self.closed_combobox.addItem("")
        self.closed_combobox.addItem("")
        self.closed_combobox.addItem("")
        self.closed_combobox.setObjectName(u"closed_combobox")
        self.closed_combobox.setGeometry(QRect(70, 52, 171, 32))
        self.closed_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.closed_combobox.setAcceptDrops(True)
        self.open_combobox = QComboBox(self.centralwidget)
        self.open_combobox.addItem("")
        self.open_combobox.addItem("")
        self.open_combobox.addItem("")
        self.open_combobox.addItem("")
        self.open_combobox.setObjectName(u"open_combobox")
        self.open_combobox.setGeometry(QRect(70, 14, 171, 32))
        self.open_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.open_combobox.setAcceptDrops(False)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(15, 52, 49, 31))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(19, 14, 45, 32))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(29, 128, 35, 32))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(11, 90, 53, 31))
        self.ok_combobox = QComboBox(self.centralwidget)
        self.ok_combobox.addItem("")
        self.ok_combobox.addItem("")
        self.ok_combobox.addItem("")
        self.ok_combobox.addItem("")
        self.ok_combobox.setObjectName(u"ok_combobox")
        self.ok_combobox.setGeometry(QRect(70, 128, 171, 32))
        self.ok_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.ok_combobox.setAcceptDrops(True)
        self.pointer_combobox = QComboBox(self.centralwidget)
        self.pointer_combobox.addItem("")
        self.pointer_combobox.addItem("")
        self.pointer_combobox.addItem("")
        self.pointer_combobox.addItem("")
        self.pointer_combobox.setObjectName(u"pointer_combobox")
        self.pointer_combobox.setGeometry(QRect(70, 90, 171, 32))
        self.pointer_combobox.setCursor(QCursor(Qt.ArrowCursor))
        self.pointer_combobox.setMouseTracking(True)
        self.pointer_combobox.setAcceptDrops(False)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(280, 20, 581, 331))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(30, 230, 211, 41))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(30, 280, 211, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.closed_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Mouse move", None))
        self.closed_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041b\u041a\u041c", None))
        self.closed_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"S", None))
        self.closed_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"L", None))

        self.open_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Mouse move", None))
        self.open_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041b\u041a\u041c", None))
        self.open_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"L", None))
        self.open_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"S", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Closed\u270a", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Open\u270b", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Pointer\u261d\ufe0f", None))
        self.ok_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Move mouse", None))
        self.ok_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041b\u041a\u041c", None))
        self.ok_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"L", None))
        self.ok_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"S", None))

        self.pointer_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Mouse move", None))
        self.pointer_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041b\u041a\u041c", None))
        self.pointer_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"S", None))
        self.pointer_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"L", None))

        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
    # retranslateUi

