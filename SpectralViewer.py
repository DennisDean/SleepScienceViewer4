# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SpectralViewer.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGraphicsView, QHBoxLayout, QLabel, QLayout,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QStatusBar, QToolBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1339, 965)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_top_controls = QVBoxLayout()
        self.verticalLayout_top_controls.setObjectName(u"verticalLayout_top_controls")
        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.pushButton_control_parameters = QPushButton(self.centralwidget)
        self.pushButton_control_parameters.setObjectName(u"pushButton_control_parameters")
        self.pushButton_control_parameters.setMinimumSize(QSize(0, 25))
        self.pushButton_control_parameters.setMaximumSize(QSize(16777215, 25))
        self.pushButton_control_parameters.setCheckable(True)
        self.pushButton_control_parameters.setChecked(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_parameters)

        self.pushButton_control_settings = QPushButton(self.centralwidget)
        self.pushButton_control_settings.setObjectName(u"pushButton_control_settings")
        self.pushButton_control_settings.setMinimumSize(QSize(0, 25))
        self.pushButton_control_settings.setMaximumSize(QSize(16777215, 25))
        self.pushButton_control_settings.setCheckable(True)
        self.pushButton_control_settings.setChecked(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_settings)

        self.checkBox_control_coherence = QCheckBox(self.centralwidget)
        self.checkBox_control_coherence.setObjectName(u"checkBox_control_coherence")

        self.horizontalLayout_36.addWidget(self.checkBox_control_coherence)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_36.addItem(self.horizontalSpacer_3)

        self.pushButton_copntrol_compute = QPushButton(self.centralwidget)
        self.pushButton_copntrol_compute.setObjectName(u"pushButton_copntrol_compute")
        self.pushButton_copntrol_compute.setCheckable(True)
        self.pushButton_copntrol_compute.setChecked(True)

        self.horizontalLayout_36.addWidget(self.pushButton_copntrol_compute)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_36.addItem(self.horizontalSpacer)

        self.pushButton_control_hypnogram = QPushButton(self.centralwidget)
        self.pushButton_control_hypnogram.setObjectName(u"pushButton_control_hypnogram")
        self.pushButton_control_hypnogram.setMinimumSize(QSize(0, 25))
        self.pushButton_control_hypnogram.setMaximumSize(QSize(16777215, 25))
        self.pushButton_control_hypnogram.setCheckable(True)
        self.pushButton_control_hypnogram.setChecked(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_hypnogram)

        self.pushButton_control_spectrogram = QPushButton(self.centralwidget)
        self.pushButton_control_spectrogram.setObjectName(u"pushButton_control_spectrogram")
        self.pushButton_control_spectrogram.setCheckable(True)
        self.pushButton_control_spectrogram.setChecked(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_spectrogram)

        self.pushButton_control_markings = QPushButton(self.centralwidget)
        self.pushButton_control_markings.setObjectName(u"pushButton_control_markings")
        self.pushButton_control_markings.setCheckable(True)
        self.pushButton_control_markings.setChecked(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_markings)

        self.pushButton_control_figures = QPushButton(self.centralwidget)
        self.pushButton_control_figures.setObjectName(u"pushButton_control_figures")
        self.pushButton_control_figures.setCheckable(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_figures)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_36.addItem(self.horizontalSpacer_2)

        self.comboBox_signals = QComboBox(self.centralwidget)
        self.comboBox_signals.setObjectName(u"comboBox_signals")
        self.comboBox_signals.setMinimumSize(QSize(100, 0))
        self.comboBox_signals.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_36.addWidget(self.comboBox_signals)


        self.verticalLayout_top_controls.addLayout(self.horizontalLayout_36)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(0, 10))
        self.line_3.setMaximumSize(QSize(16777215, 10))
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_38.addWidget(self.line_3)


        self.verticalLayout_top_controls.addLayout(self.horizontalLayout_38)


        self.horizontalLayout_2.addLayout(self.verticalLayout_top_controls)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_settings = QHBoxLayout()
        self.horizontalLayout_settings.setObjectName(u"horizontalLayout_settings")
        self.verticalLayout_s = QVBoxLayout()
        self.verticalLayout_s.setObjectName(u"verticalLayout_s")
        self.verticalLayout_s.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)
        self.label_7.setMinimumSize(QSize(0, 20))
        self.label_7.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_s.addWidget(self.label_7)

        self.plainTextEdit_2 = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.plainTextEdit_2.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_2.setSizePolicy(sizePolicy2)
        self.plainTextEdit_2.setMinimumSize(QSize(200, 25))
        self.plainTextEdit_2.setMaximumSize(QSize(200, 25))

        self.verticalLayout_s.addWidget(self.plainTextEdit_2)

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy3)
        self.label_14.setMinimumSize(QSize(100, 20))
        self.label_14.setMaximumSize(QSize(100, 20))
        font = QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)

        self.verticalLayout_s.addWidget(self.label_14)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        sizePolicy2.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy2)
        self.plainTextEdit.setMinimumSize(QSize(200, 25))
        self.plainTextEdit.setMaximumSize(QSize(200, 25))

        self.verticalLayout_s.addWidget(self.plainTextEdit)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setMinimumSize(QSize(0, 20))
        self.line_4.setMaximumSize(QSize(16777215, 20))
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_s.addWidget(self.line_4)

        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_s.addWidget(self.label_15)

        self.comboBox_6 = QComboBox(self.centralwidget)
        self.comboBox_6.setObjectName(u"comboBox_6")
        sizePolicy2.setHeightForWidth(self.comboBox_6.sizePolicy().hasHeightForWidth())
        self.comboBox_6.setSizePolicy(sizePolicy2)
        self.comboBox_6.setMinimumSize(QSize(150, 25))
        self.comboBox_6.setMaximumSize(QSize(150, 25))

        self.verticalLayout_s.addWidget(self.comboBox_6, 0, Qt.AlignHCenter)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        sizePolicy1.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy1)
        self.label_17.setMinimumSize(QSize(100, 20))
        self.label_17.setMaximumSize(QSize(100, 20))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_33.addWidget(self.label_17)

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        sizePolicy1.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy1)
        self.label_16.setMinimumSize(QSize(100, 20))
        self.label_16.setMaximumSize(QSize(100, 20))
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_33.addWidget(self.label_16)


        self.verticalLayout_s.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_8 = QComboBox(self.centralwidget)
        self.comboBox_8.setObjectName(u"comboBox_8")
        sizePolicy2.setHeightForWidth(self.comboBox_8.sizePolicy().hasHeightForWidth())
        self.comboBox_8.setSizePolicy(sizePolicy2)
        self.comboBox_8.setMinimumSize(QSize(100, 25))
        self.comboBox_8.setMaximumSize(QSize(100, 25))
        self.comboBox_8.setFont(font)

        self.horizontalLayout_22.addWidget(self.comboBox_8)

        self.comboBox_7 = QComboBox(self.centralwidget)
        self.comboBox_7.setObjectName(u"comboBox_7")
        self.comboBox_7.setMinimumSize(QSize(100, 0))
        self.comboBox_7.setMaximumSize(QSize(100, 16777215))
        self.comboBox_7.setFont(font)

        self.horizontalLayout_22.addWidget(self.comboBox_7)


        self.verticalLayout_s.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_10 = QComboBox(self.centralwidget)
        self.comboBox_10.setObjectName(u"comboBox_10")
        self.comboBox_10.setMinimumSize(QSize(100, 0))
        self.comboBox_10.setMaximumSize(QSize(100, 16777215))
        self.comboBox_10.setFont(font)

        self.horizontalLayout_23.addWidget(self.comboBox_10)

        self.comboBox_9 = QComboBox(self.centralwidget)
        self.comboBox_9.setObjectName(u"comboBox_9")
        self.comboBox_9.setMinimumSize(QSize(100, 0))
        self.comboBox_9.setMaximumSize(QSize(100, 16777215))
        self.comboBox_9.setFont(font)

        self.horizontalLayout_23.addWidget(self.comboBox_9)


        self.verticalLayout_s.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_28 = QComboBox(self.centralwidget)
        self.comboBox_28.setObjectName(u"comboBox_28")
        self.comboBox_28.setMinimumSize(QSize(100, 25))
        self.comboBox_28.setMaximumSize(QSize(100, 25))
        self.comboBox_28.setFont(font)

        self.horizontalLayout_24.addWidget(self.comboBox_28)

        self.comboBox_27 = QComboBox(self.centralwidget)
        self.comboBox_27.setObjectName(u"comboBox_27")
        self.comboBox_27.setMinimumSize(QSize(100, 25))
        self.comboBox_27.setMaximumSize(QSize(100, 25))
        self.comboBox_27.setFont(font)

        self.horizontalLayout_24.addWidget(self.comboBox_27)


        self.verticalLayout_s.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_26 = QComboBox(self.centralwidget)
        self.comboBox_26.setObjectName(u"comboBox_26")
        self.comboBox_26.setMinimumSize(QSize(100, 25))
        self.comboBox_26.setMaximumSize(QSize(100, 25))
        self.comboBox_26.setFont(font)

        self.horizontalLayout_25.addWidget(self.comboBox_26)

        self.comboBox_25 = QComboBox(self.centralwidget)
        self.comboBox_25.setObjectName(u"comboBox_25")
        self.comboBox_25.setMinimumSize(QSize(100, 25))
        self.comboBox_25.setMaximumSize(QSize(100, 25))
        self.comboBox_25.setFont(font)

        self.horizontalLayout_25.addWidget(self.comboBox_25)


        self.verticalLayout_s.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_24 = QComboBox(self.centralwidget)
        self.comboBox_24.setObjectName(u"comboBox_24")
        self.comboBox_24.setMinimumSize(QSize(100, 25))
        self.comboBox_24.setMaximumSize(QSize(100, 25))
        self.comboBox_24.setFont(font)

        self.horizontalLayout_26.addWidget(self.comboBox_24)

        self.comboBox_23 = QComboBox(self.centralwidget)
        self.comboBox_23.setObjectName(u"comboBox_23")
        self.comboBox_23.setMinimumSize(QSize(100, 25))
        self.comboBox_23.setMaximumSize(QSize(100, 25))
        self.comboBox_23.setFont(font)

        self.horizontalLayout_26.addWidget(self.comboBox_23)


        self.verticalLayout_s.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_22 = QComboBox(self.centralwidget)
        self.comboBox_22.setObjectName(u"comboBox_22")
        self.comboBox_22.setMinimumSize(QSize(100, 25))
        self.comboBox_22.setMaximumSize(QSize(100, 25))
        self.comboBox_22.setFont(font)

        self.horizontalLayout_27.addWidget(self.comboBox_22)

        self.comboBox_21 = QComboBox(self.centralwidget)
        self.comboBox_21.setObjectName(u"comboBox_21")
        self.comboBox_21.setMinimumSize(QSize(100, 25))
        self.comboBox_21.setMaximumSize(QSize(100, 25))
        self.comboBox_21.setFont(font)

        self.horizontalLayout_27.addWidget(self.comboBox_21)


        self.verticalLayout_s.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_20 = QComboBox(self.centralwidget)
        self.comboBox_20.setObjectName(u"comboBox_20")
        self.comboBox_20.setMinimumSize(QSize(100, 25))
        self.comboBox_20.setMaximumSize(QSize(100, 25))
        self.comboBox_20.setFont(font)

        self.horizontalLayout_28.addWidget(self.comboBox_20)

        self.comboBox_19 = QComboBox(self.centralwidget)
        self.comboBox_19.setObjectName(u"comboBox_19")
        self.comboBox_19.setMinimumSize(QSize(100, 25))
        self.comboBox_19.setMaximumSize(QSize(100, 25))
        self.comboBox_19.setFont(font)

        self.horizontalLayout_28.addWidget(self.comboBox_19)


        self.verticalLayout_s.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_14 = QComboBox(self.centralwidget)
        self.comboBox_14.setObjectName(u"comboBox_14")
        self.comboBox_14.setMinimumSize(QSize(100, 25))
        self.comboBox_14.setMaximumSize(QSize(100, 25))
        self.comboBox_14.setFont(font)

        self.horizontalLayout_31.addWidget(self.comboBox_14)

        self.comboBox_13 = QComboBox(self.centralwidget)
        self.comboBox_13.setObjectName(u"comboBox_13")
        self.comboBox_13.setMinimumSize(QSize(100, 25))
        self.comboBox_13.setMaximumSize(QSize(100, 25))
        self.comboBox_13.setFont(font)

        self.horizontalLayout_31.addWidget(self.comboBox_13)


        self.verticalLayout_s.addLayout(self.horizontalLayout_31)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_18 = QComboBox(self.centralwidget)
        self.comboBox_18.setObjectName(u"comboBox_18")
        self.comboBox_18.setMinimumSize(QSize(100, 25))
        self.comboBox_18.setMaximumSize(QSize(100, 25))
        self.comboBox_18.setFont(font)

        self.horizontalLayout_29.addWidget(self.comboBox_18)

        self.comboBox_17 = QComboBox(self.centralwidget)
        self.comboBox_17.setObjectName(u"comboBox_17")
        self.comboBox_17.setMinimumSize(QSize(100, 25))
        self.comboBox_17.setMaximumSize(QSize(100, 25))
        self.comboBox_17.setFont(font)

        self.horizontalLayout_29.addWidget(self.comboBox_17)


        self.verticalLayout_s.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_16 = QComboBox(self.centralwidget)
        self.comboBox_16.setObjectName(u"comboBox_16")
        self.comboBox_16.setMinimumSize(QSize(100, 25))
        self.comboBox_16.setMaximumSize(QSize(100, 25))
        self.comboBox_16.setFont(font)

        self.horizontalLayout_30.addWidget(self.comboBox_16)

        self.comboBox_15 = QComboBox(self.centralwidget)
        self.comboBox_15.setObjectName(u"comboBox_15")
        self.comboBox_15.setMinimumSize(QSize(100, 25))
        self.comboBox_15.setMaximumSize(QSize(100, 25))
        self.comboBox_15.setFont(font)

        self.horizontalLayout_30.addWidget(self.comboBox_15)


        self.verticalLayout_s.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_12 = QComboBox(self.centralwidget)
        self.comboBox_12.setObjectName(u"comboBox_12")
        self.comboBox_12.setMinimumSize(QSize(100, 25))
        self.comboBox_12.setMaximumSize(QSize(100, 25))
        self.comboBox_12.setFont(font)

        self.horizontalLayout_32.addWidget(self.comboBox_12)

        self.comboBox_11 = QComboBox(self.centralwidget)
        self.comboBox_11.setObjectName(u"comboBox_11")
        self.comboBox_11.setMinimumSize(QSize(100, 25))
        self.comboBox_11.setMaximumSize(QSize(100, 25))
        self.comboBox_11.setFont(font)

        self.horizontalLayout_32.addWidget(self.comboBox_11)


        self.verticalLayout_s.addLayout(self.horizontalLayout_32)

        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setMinimumSize(QSize(0, 20))
        self.line_5.setMaximumSize(QSize(16777215, 20))
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_s.addWidget(self.line_5)

        self.verticalLayout_window_size_2 = QVBoxLayout()
        self.verticalLayout_window_size_2.setObjectName(u"verticalLayout_window_size_2")
        self.label_27 = QLabel(self.centralwidget)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_window_size_2.addWidget(self.label_27)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setMinimumSize(QSize(0, 20))
        self.checkBox_3.setMaximumSize(QSize(16777215, 20))
        self.checkBox_3.setFont(font)

        self.verticalLayout_18.addWidget(self.checkBox_3, 0, Qt.AlignTop)

        self.comboBox_34 = QComboBox(self.centralwidget)
        self.comboBox_34.setObjectName(u"comboBox_34")
        self.comboBox_34.setFont(font)

        self.verticalLayout_18.addWidget(self.comboBox_34, 0, Qt.AlignTop)

        self.comboBox_33 = QComboBox(self.centralwidget)
        self.comboBox_33.setObjectName(u"comboBox_33")
        self.comboBox_33.setFont(font)

        self.verticalLayout_18.addWidget(self.comboBox_33, 0, Qt.AlignTop)

        self.label_35 = QLabel(self.centralwidget)
        self.label_35.setObjectName(u"label_35")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy4)

        self.verticalLayout_18.addWidget(self.label_35)


        self.horizontalLayout_39.addLayout(self.verticalLayout_18)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.checkBox_4 = QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setMinimumSize(QSize(0, 20))
        self.checkBox_4.setMaximumSize(QSize(16777215, 20))
        self.checkBox_4.setFont(font)

        self.verticalLayout_19.addWidget(self.checkBox_4, 0, Qt.AlignTop)

        self.comboBox_32 = QComboBox(self.centralwidget)
        self.comboBox_32.setObjectName(u"comboBox_32")
        self.comboBox_32.setFont(font)

        self.verticalLayout_19.addWidget(self.comboBox_32, 0, Qt.AlignTop)

        self.label_36 = QLabel(self.centralwidget)
        self.label_36.setObjectName(u"label_36")
        sizePolicy4.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy4)

        self.verticalLayout_19.addWidget(self.label_36)


        self.horizontalLayout_39.addLayout(self.verticalLayout_19)


        self.verticalLayout_window_size_2.addLayout(self.horizontalLayout_39)


        self.verticalLayout_s.addLayout(self.verticalLayout_window_size_2)

        self.label_37 = QLabel(self.centralwidget)
        self.label_37.setObjectName(u"label_37")
        sizePolicy4.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy4)

        self.verticalLayout_s.addWidget(self.label_37)


        self.horizontalLayout_settings.addLayout(self.verticalLayout_s)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(10, 0))
        self.line.setMaximumSize(QSize(10, 16777215))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_settings.addWidget(self.line)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_settings)

        self.horizontalLayout_parameters = QHBoxLayout()
        self.horizontalLayout_parameters.setObjectName(u"horizontalLayout_parameters")
        self.verticalLayout_p = QVBoxLayout()
        self.verticalLayout_p.setObjectName(u"verticalLayout_p")
        self.verticalLayout_error_detection = QVBoxLayout()
        self.verticalLayout_error_detection.setObjectName(u"verticalLayout_error_detection")
        self.verticalLayout_error_detection.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setSizeConstraint(QLayout.SetFixedSize)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        sizePolicy3.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy3)
        self.label_10.setMinimumSize(QSize(150, 25))
        self.label_10.setMaximumSize(QSize(150, 25))
        self.label_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_16.addWidget(self.label_10, 0, Qt.AlignHCenter)


        self.verticalLayout_error_detection.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setSizeConstraint(QLayout.SetFixedSize)
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy5)
        self.label_11.setMinimumSize(QSize(100, 20))
        self.label_11.setMaximumSize(QSize(100, 20))
        self.label_11.setFont(font)
        self.label_11.setLayoutDirection(Qt.RightToLeft)
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.label_11, 0, Qt.AlignRight)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setMinimumSize(QSize(30, 0))
        self.label_5.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_17.addWidget(self.label_5)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy3.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy3)
        self.comboBox_2.setMinimumSize(QSize(50, 20))
        self.comboBox_2.setMaximumSize(QSize(50, 20))
        self.comboBox_2.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_17.addWidget(self.comboBox_2, 0, Qt.AlignRight)


        self.horizontalLayout_13.addLayout(self.horizontalLayout_17)


        self.verticalLayout_error_detection.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setSizeConstraint(QLayout.SetFixedSize)
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy3.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy3)
        self.label_12.setMinimumSize(QSize(100, 20))
        self.label_12.setMaximumSize(QSize(100, 20))
        self.label_12.setFont(font)
        self.label_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.label_12, 0, Qt.AlignLeft)

        self.label_26 = QLabel(self.centralwidget)
        self.label_26.setObjectName(u"label_26")
        sizePolicy5.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy5)
        self.label_26.setMinimumSize(QSize(30, 0))
        self.label_26.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_15.addWidget(self.label_26)

        self.comboBox_3 = QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName(u"comboBox_3")
        sizePolicy3.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy3)
        self.comboBox_3.setMinimumSize(QSize(50, 25))
        self.comboBox_3.setMaximumSize(QSize(50, 25))
        self.comboBox_3.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_15.addWidget(self.comboBox_3, 0, Qt.AlignRight)


        self.verticalLayout_error_detection.addLayout(self.horizontalLayout_15)


        self.verticalLayout_p.addLayout(self.verticalLayout_error_detection)

        self.line_6 = QFrame(self.centralwidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setMinimumSize(QSize(0, 20))
        self.line_6.setMaximumSize(QSize(16777215, 20))
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_p.addWidget(self.line_6)

        self.verticalLayout_band_param = QVBoxLayout()
        self.verticalLayout_band_param.setObjectName(u"verticalLayout_band_param")
        self.verticalLayout_band_param.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        sizePolicy5.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy5)
        self.label_9.setMinimumSize(QSize(0, 25))
        self.label_9.setMaximumSize(QSize(16777215, 25))
        self.label_9.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_9, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetMinimumSize)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)
        self.label.setMinimumSize(QSize(25, 20))
        self.label.setMaximumSize(QSize(25, 20))
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label, 0, Qt.AlignLeft)

        self.label_22 = QLabel(self.centralwidget)
        self.label_22.setObjectName(u"label_22")
        sizePolicy5.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy5)
        self.label_22.setMinimumSize(QSize(100, 20))
        self.label_22.setMaximumSize(QSize(100, 20))
        self.label_22.setFont(font)
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_22, 0, Qt.AlignRight)

        self.horizontalSlider_2 = QSlider(self.centralwidget)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        sizePolicy3.setHeightForWidth(self.horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_2.setSizePolicy(sizePolicy3)
        self.horizontalSlider_2.setMinimumSize(QSize(100, 25))
        self.horizontalSlider_2.setMaximumSize(QSize(100, 25))
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.horizontalLayout_8.addWidget(self.horizontalSlider_2)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setMinimumSize(QSize(25, 20))
        self.label_2.setMaximumSize(QSize(25, 20))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_2, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_23 = QLabel(self.centralwidget)
        self.label_23.setObjectName(u"label_23")
        sizePolicy5.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy5)
        self.label_23.setMinimumSize(QSize(100, 20))
        self.label_23.setMaximumSize(QSize(100, 20))
        self.label_23.setFont(font)
        self.label_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_23, 0, Qt.AlignRight)

        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        sizePolicy3.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy3)
        self.horizontalSlider.setMinimumSize(QSize(100, 25))
        self.horizontalSlider.setMaximumSize(QSize(100, 25))
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_7.addWidget(self.horizontalSlider)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setMinimumSize(QSize(25, 20))
        self.label_3.setMaximumSize(QSize(25, 20))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_6.addWidget(self.label_3, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_24 = QLabel(self.centralwidget)
        self.label_24.setObjectName(u"label_24")
        sizePolicy5.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy5)
        self.label_24.setMinimumSize(QSize(100, 20))
        self.label_24.setMaximumSize(QSize(100, 20))
        self.label_24.setFont(font)
        self.label_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_24)

        self.horizontalSlider_3 = QSlider(self.centralwidget)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        sizePolicy3.setHeightForWidth(self.horizontalSlider_3.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_3.setSizePolicy(sizePolicy3)
        self.horizontalSlider_3.setMinimumSize(QSize(100, 25))
        self.horizontalSlider_3.setMaximumSize(QSize(100, 25))
        self.horizontalSlider_3.setOrientation(Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.horizontalSlider_3)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        self.label_4.setMinimumSize(QSize(25, 20))
        self.label_4.setMaximumSize(QSize(25, 20))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_4, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_25 = QLabel(self.centralwidget)
        self.label_25.setObjectName(u"label_25")
        sizePolicy5.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy5)
        self.label_25.setMinimumSize(QSize(100, 20))
        self.label_25.setMaximumSize(QSize(100, 20))
        self.label_25.setFont(font)
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_25)

        self.horizontalSlider_4 = QSlider(self.centralwidget)
        self.horizontalSlider_4.setObjectName(u"horizontalSlider_4")
        sizePolicy3.setHeightForWidth(self.horizontalSlider_4.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_4.setSizePolicy(sizePolicy3)
        self.horizontalSlider_4.setMinimumSize(QSize(100, 25))
        self.horizontalSlider_4.setMaximumSize(QSize(100, 25))
        self.horizontalSlider_4.setOrientation(Qt.Horizontal)

        self.horizontalLayout_5.addWidget(self.horizontalSlider_4)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy3.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy3)
        self.label_6.setMinimumSize(QSize(25, 25))
        self.label_6.setMaximumSize(QSize(25, 25))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_6, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_29 = QLabel(self.centralwidget)
        self.label_29.setObjectName(u"label_29")
        sizePolicy5.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy5)
        self.label_29.setMinimumSize(QSize(100, 0))
        self.label_29.setMaximumSize(QSize(100, 16777215))
        self.label_29.setFont(font)
        self.label_29.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_29)

        self.horizontalSlider_6 = QSlider(self.centralwidget)
        self.horizontalSlider_6.setObjectName(u"horizontalSlider_6")
        sizePolicy3.setHeightForWidth(self.horizontalSlider_6.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_6.setSizePolicy(sizePolicy3)
        self.horizontalSlider_6.setMinimumSize(QSize(100, 25))
        self.horizontalSlider_6.setMaximumSize(QSize(100, 25))
        self.horizontalSlider_6.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.horizontalSlider_6)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_4)


        self.verticalLayout_p.addLayout(self.verticalLayout_band_param)

        self.line_7 = QFrame(self.centralwidget)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setMinimumSize(QSize(0, 20))
        self.line_7.setMaximumSize(QSize(16777215, 20))
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_p.addWidget(self.line_7)

        self.label_28 = QLabel(self.centralwidget)
        self.label_28.setObjectName(u"label_28")
        sizePolicy5.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy5)
        self.label_28.setAlignment(Qt.AlignCenter)

        self.verticalLayout_p.addWidget(self.label_28, 0, Qt.AlignHCenter)

        self.verticalLayout_spectral_epoch = QVBoxLayout()
        self.verticalLayout_spectral_epoch.setObjectName(u"verticalLayout_spectral_epoch")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)
        self.label_8.setMinimumSize(QSize(100, 25))
        self.label_8.setMaximumSize(QSize(100, 25))
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_8, 0, Qt.AlignLeft|Qt.AlignTop)

        self.label_30 = QLabel(self.centralwidget)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMinimumSize(QSize(20, 0))
        self.label_30.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_9.addWidget(self.label_30)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy3.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy3)
        self.comboBox.setMinimumSize(QSize(100, 25))
        self.comboBox.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_9.addWidget(self.comboBox, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_spectral_epoch.addLayout(self.horizontalLayout_9)


        self.verticalLayout_p.addLayout(self.verticalLayout_spectral_epoch)

        self.verticalLayout_window_size = QVBoxLayout()
        self.verticalLayout_window_size.setObjectName(u"verticalLayout_window_size")
        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName(u"label_19")
        sizePolicy5.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy5)
        self.label_19.setMinimumSize(QSize(100, 20))
        self.label_19.setMaximumSize(QSize(100, 20))
        self.label_19.setFont(font)

        self.verticalLayout_window_size.addWidget(self.label_19, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_31 = QLabel(self.centralwidget)
        self.label_31.setObjectName(u"label_31")
        sizePolicy5.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy5)
        self.label_31.setMinimumSize(QSize(50, 0))
        self.label_31.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_37.addWidget(self.label_31)

        self.label_21 = QLabel(self.centralwidget)
        self.label_21.setObjectName(u"label_21")
        sizePolicy5.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy5)
        self.label_21.setMinimumSize(QSize(75, 0))
        self.label_21.setMaximumSize(QSize(75, 16777215))
        self.label_21.setFont(font)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_37.addWidget(self.label_21, 0, Qt.AlignRight)

        self.comboBox_31 = QComboBox(self.centralwidget)
        self.comboBox_31.setObjectName(u"comboBox_31")
        sizePolicy3.setHeightForWidth(self.comboBox_31.sizePolicy().hasHeightForWidth())
        self.comboBox_31.setSizePolicy(sizePolicy3)
        self.comboBox_31.setMinimumSize(QSize(50, 0))
        self.comboBox_31.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_37.addWidget(self.comboBox_31, 0, Qt.AlignRight)


        self.verticalLayout_window_size.addLayout(self.horizontalLayout_37)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_32 = QLabel(self.centralwidget)
        self.label_32.setObjectName(u"label_32")
        sizePolicy5.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy5)
        self.label_32.setMinimumSize(QSize(50, 0))
        self.label_32.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_35.addWidget(self.label_32)

        self.label_20 = QLabel(self.centralwidget)
        self.label_20.setObjectName(u"label_20")
        sizePolicy5.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy5)
        self.label_20.setMinimumSize(QSize(75, 0))
        self.label_20.setMaximumSize(QSize(75, 16777215))
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_35.addWidget(self.label_20, 0, Qt.AlignRight)

        self.comboBox_30 = QComboBox(self.centralwidget)
        self.comboBox_30.setObjectName(u"comboBox_30")
        sizePolicy3.setHeightForWidth(self.comboBox_30.sizePolicy().hasHeightForWidth())
        self.comboBox_30.setSizePolicy(sizePolicy3)
        self.comboBox_30.setMinimumSize(QSize(50, 0))
        self.comboBox_30.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_35.addWidget(self.comboBox_30, 0, Qt.AlignRight)


        self.verticalLayout_window_size.addLayout(self.horizontalLayout_35)


        self.verticalLayout_p.addLayout(self.verticalLayout_window_size)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        sizePolicy5.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy5)
        self.label_18.setFont(font)

        self.verticalLayout_3.addWidget(self.label_18, 0, Qt.AlignLeft)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setSizeConstraint(QLayout.SetFixedSize)
        self.label_33 = QLabel(self.centralwidget)
        self.label_33.setObjectName(u"label_33")
        sizePolicy5.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy5)
        self.label_33.setMinimumSize(QSize(50, 0))
        self.label_33.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_34.addWidget(self.label_33)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        sizePolicy3.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy3)
        self.checkBox_2.setMinimumSize(QSize(100, 20))
        self.checkBox_2.setMaximumSize(QSize(100, 20))
        self.checkBox_2.setFont(font)
        self.checkBox_2.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_34.addWidget(self.checkBox_2, 0, Qt.AlignLeft)

        self.comboBox_29 = QComboBox(self.centralwidget)
        self.comboBox_29.setObjectName(u"comboBox_29")
        sizePolicy3.setHeightForWidth(self.comboBox_29.sizePolicy().hasHeightForWidth())
        self.comboBox_29.setSizePolicy(sizePolicy3)
        self.comboBox_29.setMinimumSize(QSize(50, 20))
        self.comboBox_29.setMaximumSize(QSize(50, 20))

        self.horizontalLayout_34.addWidget(self.comboBox_29)


        self.verticalLayout_3.addLayout(self.horizontalLayout_34)


        self.verticalLayout_p.addLayout(self.verticalLayout_3)

        self.label_34 = QLabel(self.centralwidget)
        self.label_34.setObjectName(u"label_34")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy6)

        self.verticalLayout_p.addWidget(self.label_34)


        self.horizontalLayout_parameters.addLayout(self.verticalLayout_p)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setMinimumSize(QSize(10, 0))
        self.line_2.setMaximumSize(QSize(10, 16777215))
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_parameters.addWidget(self.line_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_parameters)

        self.verticalLayout_data_views = QVBoxLayout()
        self.verticalLayout_data_views.setObjectName(u"verticalLayout_data_views")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_m = QVBoxLayout()
        self.verticalLayout_m.setObjectName(u"verticalLayout_m")
        self.horizontalLayout_hypnogram = QHBoxLayout()
        self.horizontalLayout_hypnogram.setObjectName(u"horizontalLayout_hypnogram")
        self.graphicsView_hypnogram = QGraphicsView(self.centralwidget)
        self.graphicsView_hypnogram.setObjectName(u"graphicsView_hypnogram")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.graphicsView_hypnogram.sizePolicy().hasHeightForWidth())
        self.graphicsView_hypnogram.setSizePolicy(sizePolicy7)
        self.graphicsView_hypnogram.setMinimumSize(QSize(0, 90))
        self.graphicsView_hypnogram.setMaximumSize(QSize(16777215, 90))

        self.horizontalLayout_hypnogram.addWidget(self.graphicsView_hypnogram)

        self.verticalLayout_hypnogram_control = QVBoxLayout()
        self.verticalLayout_hypnogram_control.setObjectName(u"verticalLayout_hypnogram_control")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 25))
        self.label_13.setMaximumSize(QSize(16777215, 25))
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_hypnogram_control.addWidget(self.label_13)

        self.comboBox_4 = QComboBox(self.centralwidget)
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setMinimumSize(QSize(0, 25))
        self.comboBox_4.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_hypnogram_control.addWidget(self.comboBox_4)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(62, 25))
        self.pushButton_6.setMaximumSize(QSize(62, 25))

        self.horizontalLayout_19.addWidget(self.pushButton_6, 0, Qt.AlignTop)

        self.pushButton_7 = QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setMinimumSize(QSize(25, 25))
        self.pushButton_7.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_19.addWidget(self.pushButton_7, 0, Qt.AlignTop)


        self.verticalLayout_hypnogram_control.addLayout(self.horizontalLayout_19)


        self.horizontalLayout_hypnogram.addLayout(self.verticalLayout_hypnogram_control)


        self.verticalLayout_m.addLayout(self.horizontalLayout_hypnogram)

        self.horizontalLayout_spectrogram = QHBoxLayout()
        self.horizontalLayout_spectrogram.setObjectName(u"horizontalLayout_spectrogram")
        self.graphicsView_spectrogram = QGraphicsView(self.centralwidget)
        self.graphicsView_spectrogram.setObjectName(u"graphicsView_spectrogram")
        sizePolicy7.setHeightForWidth(self.graphicsView_spectrogram.sizePolicy().hasHeightForWidth())
        self.graphicsView_spectrogram.setSizePolicy(sizePolicy7)
        self.graphicsView_spectrogram.setMinimumSize(QSize(0, 90))
        self.graphicsView_spectrogram.setMaximumSize(QSize(16777215, 90))

        self.horizontalLayout_spectrogram.addWidget(self.graphicsView_spectrogram)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.pushButton_10 = QPushButton(self.centralwidget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setMinimumSize(QSize(62, 25))
        self.pushButton_10.setMaximumSize(QSize(62, 25))

        self.horizontalLayout_14.addWidget(self.pushButton_10, 0, Qt.AlignTop)

        self.pushButton_9 = QPushButton(self.centralwidget)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setMinimumSize(QSize(25, 25))
        self.pushButton_9.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_14.addWidget(self.pushButton_9, 0, Qt.AlignTop)


        self.verticalLayout_12.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.pushButton_12 = QPushButton(self.centralwidget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setMinimumSize(QSize(62, 0))
        self.pushButton_12.setMaximumSize(QSize(62, 16777215))

        self.horizontalLayout_21.addWidget(self.pushButton_12, 0, Qt.AlignTop)

        self.pushButton_11 = QPushButton(self.centralwidget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setMinimumSize(QSize(25, 0))
        self.pushButton_11.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_21.addWidget(self.pushButton_11, 0, Qt.AlignTop)


        self.verticalLayout_12.addLayout(self.horizontalLayout_21)


        self.horizontalLayout_spectrogram.addLayout(self.verticalLayout_12)


        self.verticalLayout_m.addLayout(self.horizontalLayout_spectrogram)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout.addWidget(self.graphicsView)


        self.horizontalLayout_20.addLayout(self.horizontalLayout)

        self.verticalLayout_mark = QVBoxLayout()
        self.verticalLayout_mark.setObjectName(u"verticalLayout_mark")
        self.comboBox_5 = QComboBox(self.centralwidget)
        self.comboBox_5.setObjectName(u"comboBox_5")
        sizePolicy3.setHeightForWidth(self.comboBox_5.sizePolicy().hasHeightForWidth())
        self.comboBox_5.setSizePolicy(sizePolicy3)
        self.comboBox_5.setMinimumSize(QSize(200, 0))
        self.comboBox_5.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_mark.addWidget(self.comboBox_5)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy4.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy4)
        self.listWidget.setMinimumSize(QSize(200, 0))
        self.listWidget.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_mark.addWidget(self.listWidget)


        self.horizontalLayout_20.addLayout(self.verticalLayout_mark)


        self.verticalLayout_m.addLayout(self.horizontalLayout_20)


        self.horizontalLayout_10.addLayout(self.verticalLayout_m)


        self.verticalLayout_data_views.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_3.addLayout(self.verticalLayout_data_views)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1339, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_control_parameters.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.pushButton_control_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.checkBox_control_coherence.setText(QCoreApplication.translate("MainWindow", u"Coherence", None))
        self.pushButton_copntrol_compute.setText(QCoreApplication.translate("MainWindow", u"Compute", None))
        self.pushButton_control_hypnogram.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.pushButton_control_spectrogram.setText(QCoreApplication.translate("MainWindow", u"Spectrogram", None))
        self.pushButton_control_markings.setText(QCoreApplication.translate("MainWindow", u"Markings", None))
        self.pushButton_control_figures.setText(QCoreApplication.translate("MainWindow", u"Figures", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Description", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Output Suffix", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Reference Method", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Reference", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Band", None))
        self.label_35.setText("")
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"Notch", None))
        self.label_36.setText("")
        self.label_37.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Noise Detection (30s)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u0394 (0.6-4.6Hz)", None))
        self.label_5.setText("")
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u0392 (40-60Hz)", None))
        self.label_26.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Spectral Bands", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u03b4", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"0.5 - 4.0 Hz", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u03b8", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"4.0 - 8.0 Hz", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u03b1", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"8.0 - 12.0 Hz", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u03c3", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"12.0 - 15.0 Hz", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u03b3", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"30.0 - 50.0 Hz", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Multi-taper", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Spectral Epoch", None))
        self.label_30.setText("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Window Size", None))
        self.label_31.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Window", None))
        self.label_32.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Multi-Processing", None))
        self.label_33.setText("")
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"# of CPUs", None))
        self.label_34.setText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Spect.", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Heat", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

