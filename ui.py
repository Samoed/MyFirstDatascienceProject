# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'base.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStatusBar,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1088, 722)
        MainWindow.setMinimumSize(QSize(1088, 722))
        MainWindow.setMaximumSize(QSize(1088, 722))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setGeometry(QRect(340, 50, 731, 651))
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 7, 321, 691))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName("label_10")

        self.gridLayout.addWidget(self.label_10, 8, 0, 1, 1)

        self.like_button = QPushButton(self.gridLayoutWidget)
        self.like_button.setObjectName("like_button")

        self.gridLayout.addWidget(self.like_button, 15, 1, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")

        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)

        self.two_button = QPushButton(self.gridLayoutWidget)
        self.two_button.setObjectName("two_button")

        self.gridLayout.addWidget(self.two_button, 5, 1, 1, 1)

        self.hang_button = QPushButton(self.gridLayoutWidget)
        self.hang_button.setObjectName("hang_button")

        self.gridLayout.addWidget(self.hang_button, 12, 1, 1, 1)

        self.label_14 = QLabel(self.gridLayoutWidget)
        self.label_14.setObjectName("label_14")

        self.gridLayout.addWidget(self.label_14, 12, 0, 1, 1)

        self.l_combobox = QComboBox(self.gridLayoutWidget)
        self.l_combobox.addItem("")
        self.l_combobox.addItem("")
        self.l_combobox.addItem("")
        self.l_combobox.setObjectName("l_combobox")
        self.l_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.l_combobox.setAcceptDrops(True)

        self.gridLayout.addWidget(self.l_combobox, 3, 1, 1, 1)

        self.four_button = QPushButton(self.gridLayoutWidget)
        self.four_button.setObjectName("four_button")

        self.gridLayout.addWidget(self.four_button, 7, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.label_15 = QLabel(self.gridLayoutWidget)
        self.label_15.setObjectName("label_15")

        self.gridLayout.addWidget(self.label_15, 15, 0, 1, 1)

        self.two_fingers_combobox = QComboBox(self.gridLayoutWidget)
        self.two_fingers_combobox.addItem("")
        self.two_fingers_combobox.addItem("")
        self.two_fingers_combobox.addItem("")
        self.two_fingers_combobox.setObjectName("two_fingers_combobox")
        self.two_fingers_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.two_fingers_combobox.setAcceptDrops(False)

        self.gridLayout.addWidget(self.two_fingers_combobox, 2, 1, 1, 1)

        self.five_button = QPushButton(self.gridLayoutWidget)
        self.five_button.setObjectName("five_button")

        self.gridLayout.addWidget(self.five_button, 8, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.ok_button = QPushButton(self.gridLayoutWidget)
        self.ok_button.setObjectName("ok_button")

        self.gridLayout.addWidget(self.ok_button, 9, 1, 1, 1)

        self.three_button = QPushButton(self.gridLayoutWidget)
        self.three_button.setObjectName("three_button")

        self.gridLayout.addWidget(self.three_button, 6, 1, 1, 1)

        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName("label_12")

        self.gridLayout.addWidget(self.label_12, 11, 0, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")

        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget)
        self.label_13.setObjectName("label_13")

        self.gridLayout.addWidget(self.label_13, 13, 0, 1, 1)

        self.one_combobox = QComboBox(self.gridLayoutWidget)
        self.one_combobox.addItem("")
        self.one_combobox.addItem("")
        self.one_combobox.addItem("")
        self.one_combobox.setObjectName("one_combobox")
        self.one_combobox.setCursor(QCursor(Qt.PointingHandCursor))
        self.one_combobox.setAcceptDrops(True)

        self.gridLayout.addWidget(self.one_combobox, 4, 1, 1, 1)

        self.stop_button = QPushButton(self.gridLayoutWidget)
        self.stop_button.setObjectName("stop_button")

        self.gridLayout.addWidget(self.stop_button, 19, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 17, 0, 1, 2)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName("label_11")

        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)

        self.label_16 = QLabel(self.gridLayoutWidget)
        self.label_16.setObjectName("label_16")

        self.gridLayout.addWidget(self.label_16, 16, 0, 1, 1)

        self.start_button = QPushButton(self.gridLayoutWidget)
        self.start_button.setObjectName("start_button")

        self.gridLayout.addWidget(self.start_button, 18, 0, 1, 2)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")

        self.gridLayout.addWidget(self.label_7, 10, 0, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)

        self.dislike_button = QPushButton(self.gridLayoutWidget)
        self.dislike_button.setObjectName("dislike_button")

        self.gridLayout.addWidget(self.dislike_button, 16, 1, 1, 1)

        self.c_button = QPushButton(self.gridLayoutWidget)
        self.c_button.setObjectName("c_button")

        self.gridLayout.addWidget(self.c_button, 10, 1, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.open_combobox_2 = QComboBox(self.gridLayoutWidget)
        self.open_combobox_2.addItem("")
        self.open_combobox_2.setObjectName("open_combobox_2")
        self.open_combobox_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.open_combobox_2.setAcceptDrops(False)

        self.gridLayout.addWidget(self.open_combobox_2, 0, 1, 1, 1)

        self.heavy_button = QPushButton(self.gridLayoutWidget)
        self.heavy_button.setObjectName("heavy_button")

        self.gridLayout.addWidget(self.heavy_button, 11, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 0, 1, 2)

        self.palm_button = QPushButton(self.gridLayoutWidget)
        self.palm_button.setObjectName("palm_button")

        self.gridLayout.addWidget(self.palm_button, 13, 1, 1, 1)

        self.add_profile_button = QPushButton(self.centralwidget)
        self.add_profile_button.setObjectName("add_profile_button")
        self.add_profile_button.setGeometry(QRect(340, 10, 88, 34))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.label_5.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", "Five", None))
        self.like_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", "Ok", None))
        self.two_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.hang_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", "Hang", None))
        self.l_combobox.setItemText(0, QCoreApplication.translate("MainWindow", "Move mouse", None))
        self.l_combobox.setItemText(1, QCoreApplication.translate("MainWindow", "Left mouse (LMB)", None))
        self.l_combobox.setItemText(2, QCoreApplication.translate("MainWindow", "Right mouse", None))

        self.four_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", "One", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", "Like", None))
        self.two_fingers_combobox.setItemText(0, QCoreApplication.translate("MainWindow", "Mouse move", None))
        self.two_fingers_combobox.setItemText(1, QCoreApplication.translate("MainWindow", "Left mouse (LMB)", None))
        self.two_fingers_combobox.setItemText(2, QCoreApplication.translate("MainWindow", "Right mouse", None))

        self.five_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", "Two fingers near", None))
        self.ok_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.three_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", "Heavy", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", "Four", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", "Palm", None))
        self.one_combobox.setItemText(0, QCoreApplication.translate("MainWindow", "Mouse move", None))
        self.one_combobox.setItemText(1, QCoreApplication.translate("MainWindow", "Left click (LMB)", None))
        self.one_combobox.setItemText(2, QCoreApplication.translate("MainWindow", "Right click", None))

        self.stop_button.setText(QCoreApplication.translate("MainWindow", "Stop", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "Three", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", "L", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", "Dislike", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", "Start", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", "C", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Two", None))
        self.dislike_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.c_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", "Profile", None))
        self.open_combobox_2.setItemText(0, QCoreApplication.translate("MainWindow", "default", None))

        self.heavy_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.palm_button.setText(QCoreApplication.translate("MainWindow", "Press button, then key", None))
        self.add_profile_button.setText(QCoreApplication.translate("MainWindow", "Add Profile", None))

    # retranslateUi
