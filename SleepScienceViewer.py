# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SleepScienceViewer.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGraphicsView,
    QHBoxLayout, QLabel, QLayout, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1203, 1061)
        self.actionOpen_Edf = QAction(MainWindow)
        self.actionOpen_Edf.setObjectName(u"actionOpen_Edf")
        self.actionOpen_XML = QAction(MainWindow)
        self.actionOpen_XML.setObjectName(u"actionOpen_XML")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionEDF_Summary = QAction(MainWindow)
        self.actionEDF_Summary.setObjectName(u"actionEDF_Summary")
        self.actionEDF_Signal_Export = QAction(MainWindow)
        self.actionEDF_Signal_Export.setObjectName(u"actionEDF_Signal_Export")
        self.actionAnnotation_Summary = QAction(MainWindow)
        self.actionAnnotation_Summary.setObjectName(u"actionAnnotation_Summary")
        self.actionSleep_Stages_Export = QAction(MainWindow)
        self.actionSleep_Stages_Export.setObjectName(u"actionSleep_Stages_Export")
        self.actionAnnotation_Export = QAction(MainWindow)
        self.actionAnnotation_Export.setObjectName(u"actionAnnotation_Export")
        self.actionEDF_Standard = QAction(MainWindow)
        self.actionEDF_Standard.setObjectName(u"actionEDF_Standard")
        self.actionAnnotation_Standard = QAction(MainWindow)
        self.actionAnnotation_Standard.setObjectName(u"actionAnnotation_Standard")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.load_edf_textEdit = QTextEdit(self.centralwidget)
        self.load_edf_textEdit.setObjectName(u"load_edf_textEdit")
        self.load_edf_textEdit.setMaximumSize(QSize(16777215, 35))

        self.horizontalLayout_2.addWidget(self.load_edf_textEdit)

        self.load_edf_pushButton = QPushButton(self.centralwidget)
        self.load_edf_pushButton.setObjectName(u"load_edf_pushButton")

        self.horizontalLayout_2.addWidget(self.load_edf_pushButton)

        self.horizontalSpacer = QSpacerItem(60, 10, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.load_annotation_textEdit = QTextEdit(self.centralwidget)
        self.load_annotation_textEdit.setObjectName(u"load_annotation_textEdit")
        self.load_annotation_textEdit.setMaximumSize(QSize(16777215, 35))

        self.horizontalLayout_2.addWidget(self.load_annotation_textEdit)

        self.load_annotation_pushButton = QPushButton(self.centralwidget)
        self.load_annotation_pushButton.setObjectName(u"load_annotation_pushButton")
        self.load_annotation_pushButton.setMaximumSize(QSize(125, 16777215))

        self.horizontalLayout_2.addWidget(self.load_annotation_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer_10 = QSpacerItem(125, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_10)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_3)

        self.hypnogram_label = QLabel(self.centralwidget)
        self.hypnogram_label.setObjectName(u"hypnogram_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hypnogram_label.sizePolicy().hasHeightForWidth())
        self.hypnogram_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_17.addWidget(self.hypnogram_label)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_11)

        self.hypnogram_comboBox = QComboBox(self.centralwidget)
        self.hypnogram_comboBox.setObjectName(u"hypnogram_comboBox")
        self.hypnogram_comboBox.setMinimumSize(QSize(125, 0))
        self.hypnogram_comboBox.setMaximumSize(QSize(125, 16777215))

        self.horizontalLayout_17.addWidget(self.hypnogram_comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_17)

        self.hypnogram_graphicsView = QGraphicsView(self.centralwidget)
        self.hypnogram_graphicsView.setObjectName(u"hypnogram_graphicsView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.hypnogram_graphicsView.sizePolicy().hasHeightForWidth())
        self.hypnogram_graphicsView.setSizePolicy(sizePolicy1)
        self.hypnogram_graphicsView.setMinimumSize(QSize(0, 90))
        self.hypnogram_graphicsView.setMaximumSize(QSize(16777215, 90))

        self.verticalLayout_2.addWidget(self.hypnogram_graphicsView)

        self.spectrogram_graphicsView = QGraphicsView(self.centralwidget)
        self.spectrogram_graphicsView.setObjectName(u"spectrogram_graphicsView")
        sizePolicy1.setHeightForWidth(self.spectrogram_graphicsView.sizePolicy().hasHeightForWidth())
        self.spectrogram_graphicsView.setSizePolicy(sizePolicy1)
        self.spectrogram_graphicsView.setMinimumSize(QSize(0, 90))
        self.spectrogram_graphicsView.setMaximumSize(QSize(16777215, 90))

        self.verticalLayout_2.addWidget(self.spectrogram_graphicsView)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.compute_spectrogram_pushButton = QPushButton(self.centralwidget)
        self.compute_spectrogram_pushButton.setObjectName(u"compute_spectrogram_pushButton")
        self.compute_spectrogram_pushButton.setMinimumSize(QSize(125, 0))
        self.compute_spectrogram_pushButton.setMaximumSize(QSize(125, 16777215))

        self.horizontalLayout_19.addWidget(self.compute_spectrogram_pushButton)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_5)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.horizontalLayout_19.addWidget(self.label_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_4)

        self.spectrogram_comboBox = QComboBox(self.centralwidget)
        self.spectrogram_comboBox.setObjectName(u"spectrogram_comboBox")
        self.spectrogram_comboBox.setMinimumSize(QSize(125, 0))
        self.spectrogram_comboBox.setMaximumSize(QSize(125, 16777215))

        self.horizontalLayout_19.addWidget(self.spectrogram_comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_19)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_7)

        self.first_pushButton = QPushButton(self.centralwidget)
        self.first_pushButton.setObjectName(u"first_pushButton")
        self.first_pushButton.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_16.addWidget(self.first_pushButton)

        self.next_epoch_pushButton = QPushButton(self.centralwidget)
        self.next_epoch_pushButton.setObjectName(u"next_epoch_pushButton")
        self.next_epoch_pushButton.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_16.addWidget(self.next_epoch_pushButton)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_9)

        self.update_epoch_pushButton = QPushButton(self.centralwidget)
        self.update_epoch_pushButton.setObjectName(u"update_epoch_pushButton")
        self.update_epoch_pushButton.setMinimumSize(QSize(30, 0))
        self.update_epoch_pushButton.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_16.addWidget(self.update_epoch_pushButton)

        self.epochs_textEdit = QTextEdit(self.centralwidget)
        self.epochs_textEdit.setObjectName(u"epochs_textEdit")
        self.epochs_textEdit.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_16.addWidget(self.epochs_textEdit)

        self.epochs_label = QLabel(self.centralwidget)
        self.epochs_label.setObjectName(u"epochs_label")

        self.horizontalLayout_16.addWidget(self.epochs_label)

        self.horizontalSpacer_12 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_12)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_8)

        self.previous_pushButton = QPushButton(self.centralwidget)
        self.previous_pushButton.setObjectName(u"previous_pushButton")
        self.previous_pushButton.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_16.addWidget(self.previous_pushButton)

        self.last_epoch_pushButton = QPushButton(self.centralwidget)
        self.last_epoch_pushButton.setObjectName(u"last_epoch_pushButton")
        self.last_epoch_pushButton.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_16.addWidget(self.last_epoch_pushButton)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_6)

        self.epoch_comboBox = QComboBox(self.centralwidget)
        self.epoch_comboBox.setObjectName(u"epoch_comboBox")
        self.epoch_comboBox.setMinimumSize(QSize(100, 0))
        self.epoch_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_16.addWidget(self.epoch_comboBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.signal_1_comboBox = QComboBox(self.centralwidget)
        self.signal_1_comboBox.setObjectName(u"signal_1_comboBox")
        self.signal_1_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_1_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_15.addWidget(self.signal_1_comboBox)

        self.color_1_pushButton = QPushButton(self.centralwidget)
        self.color_1_pushButton.setObjectName(u"color_1_pushButton")
        self.color_1_pushButton.setMinimumSize(QSize(25, 0))
        self.color_1_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_15.addWidget(self.color_1_pushButton)

        self.signal_1_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_1_graphicsView.setObjectName(u"signal_1_graphicsView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.signal_1_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_1_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_1_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_1_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_15.addWidget(self.signal_1_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.signal_2_comboBox = QComboBox(self.centralwidget)
        self.signal_2_comboBox.setObjectName(u"signal_2_comboBox")
        self.signal_2_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_2_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_14.addWidget(self.signal_2_comboBox)

        self.color_2_pushButton = QPushButton(self.centralwidget)
        self.color_2_pushButton.setObjectName(u"color_2_pushButton")
        self.color_2_pushButton.setMinimumSize(QSize(25, 0))
        self.color_2_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_14.addWidget(self.color_2_pushButton)

        self.signal_2_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_2_graphicsView.setObjectName(u"signal_2_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_2_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_2_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_2_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_2_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_14.addWidget(self.signal_2_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.signal_3_comboBox = QComboBox(self.centralwidget)
        self.signal_3_comboBox.setObjectName(u"signal_3_comboBox")
        self.signal_3_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_3_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_13.addWidget(self.signal_3_comboBox)

        self.color_3_pushButton = QPushButton(self.centralwidget)
        self.color_3_pushButton.setObjectName(u"color_3_pushButton")
        self.color_3_pushButton.setMinimumSize(QSize(25, 0))
        self.color_3_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_13.addWidget(self.color_3_pushButton)

        self.signal_3_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_3_graphicsView.setObjectName(u"signal_3_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_3_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_3_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_3_graphicsView.setMinimumSize(QSize(50, 0))
        self.signal_3_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_13.addWidget(self.signal_3_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.signal_4_comboBox = QComboBox(self.centralwidget)
        self.signal_4_comboBox.setObjectName(u"signal_4_comboBox")
        self.signal_4_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_4_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_12.addWidget(self.signal_4_comboBox)

        self.color_4_pushButton = QPushButton(self.centralwidget)
        self.color_4_pushButton.setObjectName(u"color_4_pushButton")
        self.color_4_pushButton.setMinimumSize(QSize(25, 0))
        self.color_4_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_12.addWidget(self.color_4_pushButton)

        self.signal_4_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_4_graphicsView.setObjectName(u"signal_4_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_4_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_4_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_4_graphicsView.setMinimumSize(QSize(50, 0))
        self.signal_4_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_12.addWidget(self.signal_4_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.signal_5_comboBox = QComboBox(self.centralwidget)
        self.signal_5_comboBox.setObjectName(u"signal_5_comboBox")
        self.signal_5_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_5_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_11.addWidget(self.signal_5_comboBox)

        self.color_5_pushButton = QPushButton(self.centralwidget)
        self.color_5_pushButton.setObjectName(u"color_5_pushButton")
        self.color_5_pushButton.setMinimumSize(QSize(25, 0))
        self.color_5_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_11.addWidget(self.color_5_pushButton)

        self.signal_5_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_5_graphicsView.setObjectName(u"signal_5_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_5_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_5_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_5_graphicsView.setMinimumSize(QSize(50, 0))
        self.signal_5_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_11.addWidget(self.signal_5_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.signal_6_comboBox = QComboBox(self.centralwidget)
        self.signal_6_comboBox.setObjectName(u"signal_6_comboBox")
        self.signal_6_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_6_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_10.addWidget(self.signal_6_comboBox)

        self.color_6_pushButton = QPushButton(self.centralwidget)
        self.color_6_pushButton.setObjectName(u"color_6_pushButton")
        self.color_6_pushButton.setMinimumSize(QSize(25, 0))
        self.color_6_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_10.addWidget(self.color_6_pushButton)

        self.signal_6_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_6_graphicsView.setObjectName(u"signal_6_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_6_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_6_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_6_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_6_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_10.addWidget(self.signal_6_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.signal_7_comboBox = QComboBox(self.centralwidget)
        self.signal_7_comboBox.setObjectName(u"signal_7_comboBox")
        self.signal_7_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_7_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_9.addWidget(self.signal_7_comboBox)

        self.color_7_pushButton = QPushButton(self.centralwidget)
        self.color_7_pushButton.setObjectName(u"color_7_pushButton")
        self.color_7_pushButton.setMinimumSize(QSize(25, 0))
        self.color_7_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_9.addWidget(self.color_7_pushButton)

        self.signal_7_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_7_graphicsView.setObjectName(u"signal_7_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_7_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_7_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_7_graphicsView.setMinimumSize(QSize(50, 0))
        self.signal_7_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_9.addWidget(self.signal_7_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.signal_8_comboBox = QComboBox(self.centralwidget)
        self.signal_8_comboBox.setObjectName(u"signal_8_comboBox")
        self.signal_8_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_8_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_8.addWidget(self.signal_8_comboBox)

        self.color_8_pushButton = QPushButton(self.centralwidget)
        self.color_8_pushButton.setObjectName(u"color_8_pushButton")
        self.color_8_pushButton.setMinimumSize(QSize(25, 0))
        self.color_8_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_8.addWidget(self.color_8_pushButton)

        self.signal_8_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_8_graphicsView.setObjectName(u"signal_8_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_8_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_8_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_8_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_8_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_8.addWidget(self.signal_8_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.signal_9_comboBox = QComboBox(self.centralwidget)
        self.signal_9_comboBox.setObjectName(u"signal_9_comboBox")
        self.signal_9_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_9_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_7.addWidget(self.signal_9_comboBox)

        self.color_9_pushButton = QPushButton(self.centralwidget)
        self.color_9_pushButton.setObjectName(u"color_9_pushButton")
        self.color_9_pushButton.setMinimumSize(QSize(25, 0))
        self.color_9_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_7.addWidget(self.color_9_pushButton)

        self.signal_9_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_9_graphicsView.setObjectName(u"signal_9_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_9_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_9_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_9_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_9_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_7.addWidget(self.signal_9_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.signal_10_comboBox = QComboBox(self.centralwidget)
        self.signal_10_comboBox.setObjectName(u"signal_10_comboBox")
        self.signal_10_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_10_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.signal_10_comboBox)

        self.color_10_pushButton = QPushButton(self.centralwidget)
        self.color_10_pushButton.setObjectName(u"color_10_pushButton")
        self.color_10_pushButton.setMinimumSize(QSize(25, 0))
        self.color_10_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_5.addWidget(self.color_10_pushButton)

        self.signal_10_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_10_graphicsView.setObjectName(u"signal_10_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_10_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_10_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_10_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_10_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_5.addWidget(self.signal_10_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.signal_11_comboBox = QComboBox(self.centralwidget)
        self.signal_11_comboBox.setObjectName(u"signal_11_comboBox")
        self.signal_11_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_11_comboBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_6.addWidget(self.signal_11_comboBox)

        self.color_11_pushButton = QPushButton(self.centralwidget)
        self.color_11_pushButton.setObjectName(u"color_11_pushButton")
        self.color_11_pushButton.setMinimumSize(QSize(25, 0))
        self.color_11_pushButton.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_6.addWidget(self.color_11_pushButton)

        self.signal_11_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_11_graphicsView.setObjectName(u"signal_11_graphicsView")
        sizePolicy2.setHeightForWidth(self.signal_11_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_11_graphicsView.setSizePolicy(sizePolicy2)
        self.signal_11_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_11_graphicsView.setMaximumSize(QSize(16777215, 50))

        self.horizontalLayout_6.addWidget(self.signal_11_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetMinimumSize)
        self.annotation_comboBox = QComboBox(self.centralwidget)
        self.annotation_comboBox.setObjectName(u"annotation_comboBox")
        self.annotation_comboBox.setMaximumSize(QSize(300, 16777215))

        self.verticalLayout_4.addWidget(self.annotation_comboBox)

        self.annotation_listWidget = QListWidget(self.centralwidget)
        self.annotation_listWidget.setObjectName(u"annotation_listWidget")
        self.annotation_listWidget.setMaximumSize(QSize(300, 16777215))

        self.verticalLayout_4.addWidget(self.annotation_listWidget)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1203, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuGenerate = QMenu(self.menubar)
        self.menuGenerate.setObjectName(u"menuGenerate")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuGenerate.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_Edf)
        self.menuFile.addAction(self.actionOpen_XML)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuGenerate.addAction(self.actionEDF_Summary)
        self.menuGenerate.addSeparator()
        self.menuGenerate.addAction(self.actionAnnotation_Summary)
        self.menuGenerate.addAction(self.actionAnnotation_Export)
        self.menuGenerate.addAction(self.actionSleep_Stages_Export)
        self.menuHelp.addAction(self.actionEDF_Standard)
        self.menuHelp.addAction(self.actionAnnotation_Standard)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_Edf.setText(QCoreApplication.translate("MainWindow", u"Open Edf", None))
        self.actionOpen_XML.setText(QCoreApplication.translate("MainWindow", u"Open XML", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionEDF_Summary.setText(QCoreApplication.translate("MainWindow", u"EDF Summary", None))
        self.actionEDF_Signal_Export.setText(QCoreApplication.translate("MainWindow", u"EDF Signal Export", None))
        self.actionAnnotation_Summary.setText(QCoreApplication.translate("MainWindow", u"Annotation Summary", None))
        self.actionSleep_Stages_Export.setText(QCoreApplication.translate("MainWindow", u"Sleep Stages Export", None))
        self.actionAnnotation_Export.setText(QCoreApplication.translate("MainWindow", u"Annotation Export", None))
        self.actionEDF_Standard.setText(QCoreApplication.translate("MainWindow", u"EDF Standard", None))
        self.actionAnnotation_Standard.setText(QCoreApplication.translate("MainWindow", u"Annotation Standard", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.load_edf_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load EDF", None))
        self.load_annotation_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load Annot.", None))
        self.hypnogram_label.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.compute_spectrogram_pushButton.setText(QCoreApplication.translate("MainWindow", u"Compute", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Multitaper Spectrogram", None))
        self.first_pushButton.setText(QCoreApplication.translate("MainWindow", u"First", None))
        self.next_epoch_pushButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.update_epoch_pushButton.setText(QCoreApplication.translate("MainWindow", u"U", None))
        self.epochs_label.setText(QCoreApplication.translate("MainWindow", u"/max_epochs", None))
        self.previous_pushButton.setText(QCoreApplication.translate("MainWindow", u"Prev.", None))
        self.last_epoch_pushButton.setText(QCoreApplication.translate("MainWindow", u"Last", None))
        self.color_1_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_2_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_3_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_4_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_5_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_6_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_7_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_8_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_9_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_10_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.color_11_pushButton.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuGenerate.setTitle(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

