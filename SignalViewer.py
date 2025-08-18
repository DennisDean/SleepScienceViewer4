# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SignalViewer.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QHBoxLayout,
    QLabel, QLayout, QListWidget, QListWidgetItem,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_SignalWindow(object):
    def setupUi(self, SignalWindow):
        if not SignalWindow.objectName():
            SignalWindow.setObjectName(u"SignalWindow")
        SignalWindow.resize(1279, 881)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SignalWindow.sizePolicy().hasHeightForWidth())
        SignalWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(SignalWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_controls = QHBoxLayout()
        self.horizontalLayout_controls.setObjectName(u"horizontalLayout_controls")
        self.horizontalLayout_controls.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(6, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer)

        self.comboBox_signals = QComboBox(self.centralwidget)
        self.comboBox_signals.setObjectName(u"comboBox_signals")
        self.comboBox_signals.setMinimumSize(QSize(150, 25))
        self.comboBox_signals.setMaximumSize(QSize(150, 25))

        self.horizontalLayout_controls.addWidget(self.comboBox_signals)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_2)

        self.comboBox_method = QComboBox(self.centralwidget)
        self.comboBox_method.setObjectName(u"comboBox_method")
        self.comboBox_method.setMinimumSize(QSize(150, 25))
        self.comboBox_method.setMaximumSize(QSize(150, 25))

        self.horizontalLayout_controls.addWidget(self.comboBox_method)

        self.pushButton_setup = QPushButton(self.centralwidget)
        self.pushButton_setup.setObjectName(u"pushButton_setup")
        self.pushButton_setup.setMinimumSize(QSize(100, 25))
        self.pushButton_setup.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_controls.addWidget(self.pushButton_setup)

        self.pushButton_compute = QPushButton(self.centralwidget)
        self.pushButton_compute.setObjectName(u"pushButton_compute")
        self.pushButton_compute.setMinimumSize(QSize(100, 25))
        self.pushButton_compute.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_controls.addWidget(self.pushButton_compute)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_5)

        self.pushButton_save = QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setMinimumSize(QSize(100, 25))
        self.pushButton_save.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_controls.addWidget(self.pushButton_save)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_4)

        self.pushButton_load = QPushButton(self.centralwidget)
        self.pushButton_load.setObjectName(u"pushButton_load")
        self.pushButton_load.setMinimumSize(QSize(100, 25))
        self.pushButton_load.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_controls.addWidget(self.pushButton_load)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_controls)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_data = QHBoxLayout()
        self.horizontalLayout_data.setObjectName(u"horizontalLayout_data")
        self.horizontalLayout_data.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout_signals = QVBoxLayout()
        self.verticalLayout_signals.setSpacing(0)
        self.verticalLayout_signals.setObjectName(u"verticalLayout_signals")
        self.verticalLayout_signals.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_8 = QSpacerItem(6, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_8)

        self.horizontalSpacer_26 = QSpacerItem(100, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_26)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_27)

        self.pushButton_first = QPushButton(self.centralwidget)
        self.pushButton_first.setObjectName(u"pushButton_first")
        self.pushButton_first.setMinimumSize(QSize(0, 25))
        self.pushButton_first.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_11.addWidget(self.pushButton_first)

        self.pushButton_next = QPushButton(self.centralwidget)
        self.pushButton_next.setObjectName(u"pushButton_next")
        self.pushButton_next.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_11.addWidget(self.pushButton_next)

        self.horizontalSpacer_6 = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_6)

        self.pushButton_update = QPushButton(self.centralwidget)
        self.pushButton_update.setObjectName(u"pushButton_update")
        self.pushButton_update.setMinimumSize(QSize(40, 25))
        self.pushButton_update.setMaximumSize(QSize(40, 25))

        self.horizontalLayout_11.addWidget(self.pushButton_update)

        self.textEdit_epoch = QTextEdit(self.centralwidget)
        self.textEdit_epoch.setObjectName(u"textEdit_epoch")
        self.textEdit_epoch.setMinimumSize(QSize(75, 25))
        self.textEdit_epoch.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_11.addWidget(self.textEdit_epoch)

        self.horizontalSpacer_23 = QSpacerItem(6, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_23)

        self.label_page = QLabel(self.centralwidget)
        self.label_page.setObjectName(u"label_page")
        self.label_page.setMinimumSize(QSize(0, 25))
        self.label_page.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_11.addWidget(self.label_page)

        self.horizontalSpacer_7 = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_7)

        self.pushButton_previous = QPushButton(self.centralwidget)
        self.pushButton_previous.setObjectName(u"pushButton_previous")
        self.pushButton_previous.setMinimumSize(QSize(0, 25))
        self.pushButton_previous.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_11.addWidget(self.pushButton_previous)

        self.pushButton_last = QPushButton(self.centralwidget)
        self.pushButton_last.setObjectName(u"pushButton_last")
        self.pushButton_last.setMinimumSize(QSize(0, 25))
        self.pushButton_last.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_11.addWidget(self.pushButton_last)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_25)

        self.comboBox_epoch = QComboBox(self.centralwidget)
        self.comboBox_epoch.setObjectName(u"comboBox_epoch")
        self.comboBox_epoch.setMinimumSize(QSize(100, 25))
        self.comboBox_epoch.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_11.addWidget(self.comboBox_epoch)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_9 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_9)

        self.label_signal_1 = QLabel(self.centralwidget)
        self.label_signal_1.setObjectName(u"label_signal_1")
        self.label_signal_1.setMinimumSize(QSize(40, 12))
        self.label_signal_1.setMaximumSize(QSize(40, 12))
        font = QFont()
        font.setPointSize(9)
        self.label_signal_1.setFont(font)
        self.label_signal_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.label_signal_1)

        self.horizontalSpacer_29 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_29)

        self.graphicsView_signal_1 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_1.setObjectName(u"graphicsView_signal_1")
        self.graphicsView_signal_1.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_1.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_10.addWidget(self.graphicsView_signal_1)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_24 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_24)

        self.label_signal_2 = QLabel(self.centralwidget)
        self.label_signal_2.setObjectName(u"label_signal_2")
        self.label_signal_2.setMinimumSize(QSize(40, 12))
        self.label_signal_2.setMaximumSize(QSize(40, 12))
        self.label_signal_2.setFont(font)
        self.label_signal_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.label_signal_2)

        self.horizontalSpacer_30 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_30)

        self.graphicsView_signal_2 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_2.setObjectName(u"graphicsView_signal_2")
        self.graphicsView_signal_2.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_2.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_16.addWidget(self.graphicsView_signal_2)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_22 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_22)

        self.label_signal_3 = QLabel(self.centralwidget)
        self.label_signal_3.setObjectName(u"label_signal_3")
        self.label_signal_3.setMinimumSize(QSize(40, 12))
        self.label_signal_3.setMaximumSize(QSize(40, 12))
        self.label_signal_3.setFont(font)
        self.label_signal_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.label_signal_3)

        self.horizontalSpacer_31 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_31)

        self.graphicsView_signal_3 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_3.setObjectName(u"graphicsView_signal_3")
        self.graphicsView_signal_3.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_3.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_15.addWidget(self.graphicsView_signal_3)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_10 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_10)

        self.label_signal_4 = QLabel(self.centralwidget)
        self.label_signal_4.setObjectName(u"label_signal_4")
        self.label_signal_4.setMinimumSize(QSize(40, 12))
        self.label_signal_4.setMaximumSize(QSize(40, 12))
        self.label_signal_4.setFont(font)
        self.label_signal_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_signal_4)

        self.horizontalSpacer_32 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_32)

        self.graphicsView_signal_4 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_4.setObjectName(u"graphicsView_signal_4")
        self.graphicsView_signal_4.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_4.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.graphicsView_signal_4)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_28 = QSpacerItem(6, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_28)

        self.label_signal_5 = QLabel(self.centralwidget)
        self.label_signal_5.setObjectName(u"label_signal_5")
        self.label_signal_5.setMinimumSize(QSize(40, 12))
        self.label_signal_5.setMaximumSize(QSize(40, 12))
        self.label_signal_5.setFont(font)
        self.label_signal_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.label_signal_5)

        self.horizontalSpacer_33 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_33)

        self.graphicsView_signal_5 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_5.setObjectName(u"graphicsView_signal_5")
        sizePolicy.setHeightForWidth(self.graphicsView_signal_5.sizePolicy().hasHeightForWidth())
        self.graphicsView_signal_5.setSizePolicy(sizePolicy)
        self.graphicsView_signal_5.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_5.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_17.addWidget(self.graphicsView_signal_5)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_11 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_11)

        self.label_signal_6 = QLabel(self.centralwidget)
        self.label_signal_6.setObjectName(u"label_signal_6")
        self.label_signal_6.setMinimumSize(QSize(40, 12))
        self.label_signal_6.setMaximumSize(QSize(40, 12))
        self.label_signal_6.setFont(font)
        self.label_signal_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.label_signal_6)

        self.horizontalSpacer_34 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_34)

        self.graphicsView_signal_6 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_6.setObjectName(u"graphicsView_signal_6")
        self.graphicsView_signal_6.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_6.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_14.addWidget(self.graphicsView_signal_6)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_12 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_12)

        self.label_signal_7 = QLabel(self.centralwidget)
        self.label_signal_7.setObjectName(u"label_signal_7")
        self.label_signal_7.setMinimumSize(QSize(40, 12))
        self.label_signal_7.setMaximumSize(QSize(40, 12))
        self.label_signal_7.setFont(font)
        self.label_signal_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_signal_7)

        self.horizontalSpacer_35 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_35)

        self.graphicsView_signal_7 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_7.setObjectName(u"graphicsView_signal_7")
        self.graphicsView_signal_7.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_7.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_12.addWidget(self.graphicsView_signal_7)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_13 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_13)

        self.label_signal_8 = QLabel(self.centralwidget)
        self.label_signal_8.setObjectName(u"label_signal_8")
        self.label_signal_8.setMinimumSize(QSize(40, 12))
        self.label_signal_8.setMaximumSize(QSize(40, 12))
        self.label_signal_8.setFont(font)
        self.label_signal_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.label_signal_8)

        self.horizontalSpacer_36 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_36)

        self.graphicsView_signal_8 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_8.setObjectName(u"graphicsView_signal_8")
        self.graphicsView_signal_8.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_8.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_13.addWidget(self.graphicsView_signal_8)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_14 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_14)

        self.label_signal_9 = QLabel(self.centralwidget)
        self.label_signal_9.setObjectName(u"label_signal_9")
        self.label_signal_9.setMinimumSize(QSize(40, 12))
        self.label_signal_9.setMaximumSize(QSize(40, 12))
        self.label_signal_9.setFont(font)
        self.label_signal_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_signal_9)

        self.horizontalSpacer_37 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_37)

        self.graphicsView_signal_9 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_9.setObjectName(u"graphicsView_signal_9")
        self.graphicsView_signal_9.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_9.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_9.addWidget(self.graphicsView_signal_9)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_15 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_15)

        self.label_signal_10 = QLabel(self.centralwidget)
        self.label_signal_10.setObjectName(u"label_signal_10")
        self.label_signal_10.setMinimumSize(QSize(40, 12))
        self.label_signal_10.setMaximumSize(QSize(40, 12))
        self.label_signal_10.setFont(font)
        self.label_signal_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_signal_10)

        self.horizontalSpacer_38 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_38)

        self.graphicsView_signal_10 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_10.setObjectName(u"graphicsView_signal_10")
        self.graphicsView_signal_10.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_10.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_8.addWidget(self.graphicsView_signal_10)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_8)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_16 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_16)

        self.label_signal_11 = QLabel(self.centralwidget)
        self.label_signal_11.setObjectName(u"label_signal_11")
        self.label_signal_11.setMinimumSize(QSize(40, 12))
        self.label_signal_11.setMaximumSize(QSize(40, 12))
        self.label_signal_11.setFont(font)
        self.label_signal_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_signal_11)

        self.horizontalSpacer_39 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_39)

        self.graphicsView_signal_11 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_11.setObjectName(u"graphicsView_signal_11")
        self.graphicsView_signal_11.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_11.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout.addWidget(self.graphicsView_signal_11)


        self.verticalLayout_signals.addLayout(self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_17 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_17)

        self.label_signal_12 = QLabel(self.centralwidget)
        self.label_signal_12.setObjectName(u"label_signal_12")
        self.label_signal_12.setMinimumSize(QSize(40, 12))
        self.label_signal_12.setMaximumSize(QSize(40, 12))
        self.label_signal_12.setFont(font)
        self.label_signal_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_signal_12)

        self.horizontalSpacer_40 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_40)

        self.graphicsView_signal_12 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_12.setObjectName(u"graphicsView_signal_12")
        self.graphicsView_signal_12.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_12.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_7.addWidget(self.graphicsView_signal_12)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_18 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_18)

        self.label_signal_13 = QLabel(self.centralwidget)
        self.label_signal_13.setObjectName(u"label_signal_13")
        self.label_signal_13.setMinimumSize(QSize(40, 12))
        self.label_signal_13.setMaximumSize(QSize(40, 12))
        self.label_signal_13.setFont(font)
        self.label_signal_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_signal_13)

        self.horizontalSpacer_41 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_41)

        self.graphicsView_signal_13 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_13.setObjectName(u"graphicsView_signal_13")
        self.graphicsView_signal_13.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_13.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_6.addWidget(self.graphicsView_signal_13)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_19 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_19)

        self.label_signal_14 = QLabel(self.centralwidget)
        self.label_signal_14.setObjectName(u"label_signal_14")
        self.label_signal_14.setMinimumSize(QSize(40, 12))
        self.label_signal_14.setMaximumSize(QSize(40, 12))
        self.label_signal_14.setFont(font)
        self.label_signal_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_signal_14)

        self.horizontalSpacer_42 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_42)

        self.graphicsView_signal_14 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_14.setObjectName(u"graphicsView_signal_14")
        self.graphicsView_signal_14.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_14.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_5.addWidget(self.graphicsView_signal_14)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_20 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_20)

        self.label_signal_15 = QLabel(self.centralwidget)
        self.label_signal_15.setObjectName(u"label_signal_15")
        self.label_signal_15.setMinimumSize(QSize(40, 12))
        self.label_signal_15.setMaximumSize(QSize(40, 12))
        self.label_signal_15.setFont(font)
        self.label_signal_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_signal_15)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_44 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_44)

        self.graphicsView_signal_15 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_15.setObjectName(u"graphicsView_signal_15")
        self.graphicsView_signal_15.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_15.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_4.addWidget(self.graphicsView_signal_15)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_21 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_21)

        self.rotatedlabel_axis = QLabel(self.centralwidget)
        self.rotatedlabel_axis.setObjectName(u"rotatedlabel_axis")
        self.rotatedlabel_axis.setMinimumSize(QSize(40, 12))
        self.rotatedlabel_axis.setMaximumSize(QSize(40, 16777215))
        self.rotatedlabel_axis.setFont(font)
        self.rotatedlabel_axis.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.rotatedlabel_axis)

        self.horizontalSpacer_43 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_43)

        self.graphicsView_signal_axis = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_axis.setObjectName(u"graphicsView_signal_axis")
        self.graphicsView_signal_axis.setMinimumSize(QSize(0, 20))
        self.graphicsView_signal_axis.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_3.addWidget(self.graphicsView_signal_axis)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_data.addLayout(self.verticalLayout_signals)

        self.verticalLayout_annotation = QVBoxLayout()
        self.verticalLayout_annotation.setObjectName(u"verticalLayout_annotation")
        self.verticalLayout_annotation.setSizeConstraint(QLayout.SetMaximumSize)
        self.comboBox_annotation = QComboBox(self.centralwidget)
        self.comboBox_annotation.setObjectName(u"comboBox_annotation")
        self.comboBox_annotation.setMinimumSize(QSize(250, 25))
        self.comboBox_annotation.setMaximumSize(QSize(250, 25))

        self.verticalLayout_annotation.addWidget(self.comboBox_annotation)

        self.listWidget_annotation = QListWidget(self.centralwidget)
        self.listWidget_annotation.setObjectName(u"listWidget_annotation")
        self.listWidget_annotation.setMinimumSize(QSize(250, 0))
        self.listWidget_annotation.setMaximumSize(QSize(250, 16777215))

        self.verticalLayout_annotation.addWidget(self.listWidget_annotation)


        self.horizontalLayout_data.addLayout(self.verticalLayout_annotation)


        self.verticalLayout.addLayout(self.horizontalLayout_data)

        SignalWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SignalWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1279, 23))
        SignalWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SignalWindow)
        self.statusbar.setObjectName(u"statusbar")
        SignalWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SignalWindow)

        QMetaObject.connectSlotsByName(SignalWindow)
    # setupUi

    def retranslateUi(self, SignalWindow):
        SignalWindow.setWindowTitle(QCoreApplication.translate("SignalWindow", u"Signal Window", None))
        self.pushButton_setup.setText(QCoreApplication.translate("SignalWindow", u"Setup", None))
        self.pushButton_compute.setText(QCoreApplication.translate("SignalWindow", u"Compute", None))
        self.pushButton_save.setText(QCoreApplication.translate("SignalWindow", u"Save", None))
        self.pushButton_load.setText(QCoreApplication.translate("SignalWindow", u"Load", None))
        self.pushButton_first.setText(QCoreApplication.translate("SignalWindow", u"First", None))
        self.pushButton_next.setText(QCoreApplication.translate("SignalWindow", u"Next", None))
        self.pushButton_update.setText(QCoreApplication.translate("SignalWindow", u"U", None))
        self.label_page.setText(QCoreApplication.translate("SignalWindow", u"1 of x pages", None))
        self.pushButton_previous.setText(QCoreApplication.translate("SignalWindow", u"Previous", None))
        self.pushButton_last.setText(QCoreApplication.translate("SignalWindow", u"Last", None))
        self.label_signal_1.setText(QCoreApplication.translate("SignalWindow", u"1", None))
        self.label_signal_2.setText(QCoreApplication.translate("SignalWindow", u"2", None))
        self.label_signal_3.setText(QCoreApplication.translate("SignalWindow", u"3", None))
        self.label_signal_4.setText(QCoreApplication.translate("SignalWindow", u"4", None))
        self.label_signal_5.setText(QCoreApplication.translate("SignalWindow", u"5", None))
        self.label_signal_6.setText(QCoreApplication.translate("SignalWindow", u"6", None))
        self.label_signal_7.setText(QCoreApplication.translate("SignalWindow", u"7", None))
        self.label_signal_8.setText(QCoreApplication.translate("SignalWindow", u"8", None))
        self.label_signal_9.setText(QCoreApplication.translate("SignalWindow", u"9", None))
        self.label_signal_10.setText(QCoreApplication.translate("SignalWindow", u"10", None))
        self.label_signal_11.setText(QCoreApplication.translate("SignalWindow", u"11", None))
        self.label_signal_12.setText(QCoreApplication.translate("SignalWindow", u"12", None))
        self.label_signal_13.setText(QCoreApplication.translate("SignalWindow", u"13", None))
        self.label_signal_14.setText(QCoreApplication.translate("SignalWindow", u"14", None))
        self.label_signal_15.setText(QCoreApplication.translate("SignalWindow", u"15", None))
        self.rotatedlabel_axis.setText(QCoreApplication.translate("SignalWindow", u"Time:", None))
    # retranslateUi

