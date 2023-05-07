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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1088, 722)
        MainWindow.setMinimumSize(QSize(1088, 722))
        MainWindow.setMaximumSize(QSize(1088, 722))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(340, 50, 731, 651))
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 7, 321, 691))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_15 = QLabel(self.gridLayoutWidget)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 16, 0, 1, 1)

        self.like_button = QPushButton(self.gridLayoutWidget)
        self.like_button.setObjectName(u"like_button")

        self.gridLayout.addWidget(self.like_button, 16, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 0, 1, 2)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.three_button = QPushButton(self.gridLayoutWidget)
        self.three_button.setObjectName(u"three_button")

        self.gridLayout.addWidget(self.three_button, 7, 1, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_16 = QLabel(self.gridLayoutWidget)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 17, 0, 1, 1)

        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 12, 0, 1, 1)

        self.hang_button = QPushButton(self.gridLayoutWidget)
        self.hang_button.setObjectName(u"hang_button")

        self.gridLayout.addWidget(self.hang_button, 13, 1, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 9, 0, 1, 1)

        self.palm_button = QPushButton(self.gridLayoutWidget)
        self.palm_button.setObjectName(u"palm_button")

        self.gridLayout.addWidget(self.palm_button, 14, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.c_button = QPushButton(self.gridLayoutWidget)
        self.c_button.setObjectName(u"c_button")

        self.gridLayout.addWidget(self.c_button, 11, 1, 1, 1)

        self.heavy_button = QPushButton(self.gridLayoutWidget)
        self.heavy_button.setObjectName(u"heavy_button")

        self.gridLayout.addWidget(self.heavy_button, 12, 1, 1, 1)

        self.one_combobox = QComboBox(self.gridLayoutWidget)
        self.one_combobox.addItem("")
        self.one_combobox.addItem("")
        self.one_combobox.addItem("")
        self.one_combobox.addItem("")
        self.one_combobox.setObjectName(u"one_combobox")
        self.one_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.one_combobox.setAcceptDrops(True)

        self.gridLayout.addWidget(self.one_combobox, 5, 1, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 14, 0, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.two_button = QPushButton(self.gridLayoutWidget)
        self.two_button.setObjectName(u"two_button")

        self.gridLayout.addWidget(self.two_button, 6, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 7, 0, 1, 1)

        self.l_combobox = QComboBox(self.gridLayoutWidget)
        self.l_combobox.addItem("")
        self.l_combobox.addItem("")
        self.l_combobox.addItem("")
        self.l_combobox.addItem("")
        self.l_combobox.setObjectName(u"l_combobox")
        self.l_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.l_combobox.setAcceptDrops(True)

        self.gridLayout.addWidget(self.l_combobox, 4, 1, 1, 1)

        self.two_fingers_near_combobox = QComboBox(self.gridLayoutWidget)
        self.two_fingers_near_combobox.addItem("")
        self.two_fingers_near_combobox.addItem("")
        self.two_fingers_near_combobox.addItem("")
        self.two_fingers_near_combobox.addItem("")
        self.two_fingers_near_combobox.setObjectName(u"two_fingers_near_combobox")
        self.two_fingers_near_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.two_fingers_near_combobox.setAcceptDrops(False)

        self.gridLayout.addWidget(self.two_fingers_near_combobox, 3, 1, 1, 1)

        self.label_14 = QLabel(self.gridLayoutWidget)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 13, 0, 1, 1)

        self.five_button = QPushButton(self.gridLayoutWidget)
        self.five_button.setObjectName(u"five_button")

        self.gridLayout.addWidget(self.five_button, 9, 1, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 10, 0, 1, 1)

        self.four_button = QPushButton(self.gridLayoutWidget)
        self.four_button.setObjectName(u"four_button")

        self.gridLayout.addWidget(self.four_button, 8, 1, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 11, 0, 1, 1)

        self.dislike_button = QPushButton(self.gridLayoutWidget)
        self.dislike_button.setObjectName(u"dislike_button")

        self.gridLayout.addWidget(self.dislike_button, 17, 1, 1, 1)

        self.ok_button = QPushButton(self.gridLayoutWidget)
        self.ok_button.setObjectName(u"ok_button")

        self.gridLayout.addWidget(self.ok_button, 10, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 18, 0, 1, 2)

        self.profile_combobox = QComboBox(self.gridLayoutWidget)
        self.profile_combobox.addItem("")
        self.profile_combobox.setObjectName(u"profile_combobox")
        self.profile_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.profile_combobox.setAcceptDrops(False)

        self.gridLayout.addWidget(self.profile_combobox, 0, 1, 1, 1)

        self.add_profile_button = QPushButton(self.gridLayoutWidget)
        self.add_profile_button.setObjectName(u"add_profile_button")

        self.gridLayout.addWidget(self.add_profile_button, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_5.setText("")
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Like", None))
        self.like_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Four", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Two fingers near", None))
        self.three_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Dislike", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Heavy", None))
        self.hang_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Five", None))
        self.palm_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"One", None))
        self.c_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.heavy_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.one_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.one_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Mouse move", None))
        self.one_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"Left mouse (LMB)", None))
        self.one_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"Right mouse", None))

        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Palm", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Two", None))
        self.two_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Three", None))
        self.l_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.l_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Move mouse", None))
        self.l_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"Left mouse (LMB)", None))
        self.l_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"Right mouse", None))

        self.two_fingers_near_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.two_fingers_near_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Mouse move", None))
        self.two_fingers_near_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"Left mouse (LMB)", None))
        self.two_fingers_near_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"Right mouse", None))

        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Hang", None))
        self.five_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Ok", None))
        self.four_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.dislike_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.ok_button.setText(QCoreApplication.translate("MainWindow", u"Press button, then key", None))
        self.profile_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"default", None))

        self.add_profile_button.setText(QCoreApplication.translate("MainWindow", u"Add Profile", None))
    # retranslateUi

