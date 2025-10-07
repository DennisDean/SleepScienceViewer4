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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGraphicsView,
    QHBoxLayout, QLabel, QLayout, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QStatusBar, QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1066, 859)
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
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 25))
        self.pushButton_2.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 25))
        self.pushButton.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 25))
        self.pushButton_3.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_2.addWidget(self.pushButton_5)

        self.pushButton_8 = QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_2.addWidget(self.pushButton_8)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.comboBox_signals = QComboBox(self.centralwidget)
        self.comboBox_signals.setObjectName(u"comboBox_signals")
        self.comboBox_signals.setMinimumSize(QSize(100, 0))
        self.comboBox_signals.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.comboBox_signals)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_settings = QVBoxLayout()
        self.verticalLayout_settings.setObjectName(u"verticalLayout_settings")
        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy1)
        self.label_14.setMinimumSize(QSize(100, 25))
        self.label_14.setMaximumSize(QSize(100, 25))

        self.verticalLayout_settings.addWidget(self.label_14)

        self.plainTextEdit_2 = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")
        sizePolicy1.setHeightForWidth(self.plainTextEdit_2.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_2.setSizePolicy(sizePolicy1)
        self.plainTextEdit_2.setMinimumSize(QSize(200, 25))
        self.plainTextEdit_2.setMaximumSize(QSize(200, 25))

        self.verticalLayout_settings.addWidget(self.plainTextEdit_2)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 20))
        self.label_7.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_settings.addWidget(self.label_7)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy2)
        self.plainTextEdit.setMinimumSize(QSize(200, 25))
        self.plainTextEdit.setMaximumSize(QSize(200, 25))

        self.verticalLayout_settings.addWidget(self.plainTextEdit)

        self.verticalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_settings.addItem(self.verticalSpacer_2)

        self.label_15 = QLabel(self.centralwidget)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_settings.addWidget(self.label_15)

        self.comboBox_6 = QComboBox(self.centralwidget)
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.verticalLayout_settings.addWidget(self.comboBox_6)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_33.addWidget(self.label_17)

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_33.addWidget(self.label_16)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.comboBox_8 = QComboBox(self.centralwidget)
        self.comboBox_8.setObjectName(u"comboBox_8")

        self.horizontalLayout_22.addWidget(self.comboBox_8)

        self.comboBox_7 = QComboBox(self.centralwidget)
        self.comboBox_7.setObjectName(u"comboBox_7")

        self.horizontalLayout_22.addWidget(self.comboBox_7)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.comboBox_10 = QComboBox(self.centralwidget)
        self.comboBox_10.setObjectName(u"comboBox_10")

        self.horizontalLayout_23.addWidget(self.comboBox_10)

        self.comboBox_9 = QComboBox(self.centralwidget)
        self.comboBox_9.setObjectName(u"comboBox_9")

        self.horizontalLayout_23.addWidget(self.comboBox_9)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.comboBox_28 = QComboBox(self.centralwidget)
        self.comboBox_28.setObjectName(u"comboBox_28")

        self.horizontalLayout_24.addWidget(self.comboBox_28)

        self.comboBox_27 = QComboBox(self.centralwidget)
        self.comboBox_27.setObjectName(u"comboBox_27")

        self.horizontalLayout_24.addWidget(self.comboBox_27)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.comboBox_26 = QComboBox(self.centralwidget)
        self.comboBox_26.setObjectName(u"comboBox_26")

        self.horizontalLayout_25.addWidget(self.comboBox_26)

        self.comboBox_25 = QComboBox(self.centralwidget)
        self.comboBox_25.setObjectName(u"comboBox_25")

        self.horizontalLayout_25.addWidget(self.comboBox_25)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.comboBox_24 = QComboBox(self.centralwidget)
        self.comboBox_24.setObjectName(u"comboBox_24")

        self.horizontalLayout_26.addWidget(self.comboBox_24)

        self.comboBox_23 = QComboBox(self.centralwidget)
        self.comboBox_23.setObjectName(u"comboBox_23")

        self.horizontalLayout_26.addWidget(self.comboBox_23)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.comboBox_22 = QComboBox(self.centralwidget)
        self.comboBox_22.setObjectName(u"comboBox_22")

        self.horizontalLayout_27.addWidget(self.comboBox_22)

        self.comboBox_21 = QComboBox(self.centralwidget)
        self.comboBox_21.setObjectName(u"comboBox_21")

        self.horizontalLayout_27.addWidget(self.comboBox_21)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.comboBox_20 = QComboBox(self.centralwidget)
        self.comboBox_20.setObjectName(u"comboBox_20")

        self.horizontalLayout_28.addWidget(self.comboBox_20)

        self.comboBox_19 = QComboBox(self.centralwidget)
        self.comboBox_19.setObjectName(u"comboBox_19")

        self.horizontalLayout_28.addWidget(self.comboBox_19)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.comboBox_14 = QComboBox(self.centralwidget)
        self.comboBox_14.setObjectName(u"comboBox_14")

        self.horizontalLayout_31.addWidget(self.comboBox_14)

        self.comboBox_13 = QComboBox(self.centralwidget)
        self.comboBox_13.setObjectName(u"comboBox_13")

        self.horizontalLayout_31.addWidget(self.comboBox_13)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_31)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.comboBox_18 = QComboBox(self.centralwidget)
        self.comboBox_18.setObjectName(u"comboBox_18")

        self.horizontalLayout_29.addWidget(self.comboBox_18)

        self.comboBox_17 = QComboBox(self.centralwidget)
        self.comboBox_17.setObjectName(u"comboBox_17")

        self.horizontalLayout_29.addWidget(self.comboBox_17)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.comboBox_16 = QComboBox(self.centralwidget)
        self.comboBox_16.setObjectName(u"comboBox_16")

        self.horizontalLayout_30.addWidget(self.comboBox_16)

        self.comboBox_15 = QComboBox(self.centralwidget)
        self.comboBox_15.setObjectName(u"comboBox_15")

        self.horizontalLayout_30.addWidget(self.comboBox_15)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.comboBox_12 = QComboBox(self.centralwidget)
        self.comboBox_12.setObjectName(u"comboBox_12")

        self.horizontalLayout_32.addWidget(self.comboBox_12)

        self.comboBox_11 = QComboBox(self.centralwidget)
        self.comboBox_11.setObjectName(u"comboBox_11")

        self.horizontalLayout_32.addWidget(self.comboBox_11)


        self.verticalLayout_settings.addLayout(self.horizontalLayout_32)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_settings.addItem(self.verticalSpacer)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_settings.addWidget(self.checkBox, 0, Qt.AlignHCenter)


        self.horizontalLayout_3.addLayout(self.verticalLayout_settings)

        self.verticalLayout_parameters = QVBoxLayout()
        self.verticalLayout_parameters.setObjectName(u"verticalLayout_parameters")
        self.verticalLayout_spectral_epoch = QVBoxLayout()
        self.verticalLayout_spectral_epoch.setObjectName(u"verticalLayout_spectral_epoch")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setMinimumSize(QSize(100, 25))
        self.label_8.setMaximumSize(QSize(100, 25))
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_8, 0, Qt.AlignTop)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy1)
        self.comboBox.setMinimumSize(QSize(100, 25))
        self.comboBox.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_9.addWidget(self.comboBox, 0, Qt.AlignTop)


        self.verticalLayout_spectral_epoch.addLayout(self.horizontalLayout_9)


        self.verticalLayout_parameters.addLayout(self.verticalLayout_spectral_epoch)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_parameters.addItem(self.verticalSpacer_4)

        self.verticalLayout_band_param = QVBoxLayout()
        self.verticalLayout_band_param.setObjectName(u"verticalLayout_band_param")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 25))
        self.label_9.setMaximumSize(QSize(16777215, 25))
        self.label_9.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_9, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(0, 25))
        self.label.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_8.addWidget(self.label, 0, Qt.AlignRight|Qt.AlignTop)

        self.horizontalSlider_2 = QSlider(self.centralwidget)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setMinimumSize(QSize(150, 25))
        self.horizontalSlider_2.setMaximumSize(QSize(150, 25))
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.horizontalLayout_8.addWidget(self.horizontalSlider_2, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(50, 25))
        self.label_2.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_7.addWidget(self.label_2, 0, Qt.AlignRight|Qt.AlignTop)

        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMinimumSize(QSize(150, 25))
        self.horizontalSlider.setMaximumSize(QSize(150, 25))
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_7.addWidget(self.horizontalSlider, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(0, 25))
        self.label_3.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_6.addWidget(self.label_3, 0, Qt.AlignRight|Qt.AlignTop)

        self.horizontalSlider_3 = QSlider(self.centralwidget)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setMinimumSize(QSize(150, 25))
        self.horizontalSlider_3.setMaximumSize(QSize(150, 25))
        self.horizontalSlider_3.setOrientation(Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.horizontalSlider_3, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(0, 25))
        self.label_4.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_5.addWidget(self.label_4, 0, Qt.AlignRight|Qt.AlignTop)

        self.horizontalSlider_4 = QSlider(self.centralwidget)
        self.horizontalSlider_4.setObjectName(u"horizontalSlider_4")
        self.horizontalSlider_4.setMinimumSize(QSize(150, 25))
        self.horizontalSlider_4.setMaximumSize(QSize(150, 25))
        self.horizontalSlider_4.setOrientation(Qt.Horizontal)

        self.horizontalLayout_5.addWidget(self.horizontalSlider_4, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setMinimumSize(QSize(0, 25))
        self.label_5.setMaximumSize(QSize(50, 25))

        self.horizontalLayout.addWidget(self.label_5, 0, Qt.AlignRight|Qt.AlignTop)

        self.horizontalSlider_5 = QSlider(self.centralwidget)
        self.horizontalSlider_5.setObjectName(u"horizontalSlider_5")
        self.horizontalSlider_5.setMinimumSize(QSize(150, 25))
        self.horizontalSlider_5.setMaximumSize(QSize(150, 25))
        self.horizontalSlider_5.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.horizontalSlider_5, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(0, 25))
        self.label_6.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_4.addWidget(self.label_6, 0, Qt.AlignRight|Qt.AlignTop)

        self.horizontalSlider_6 = QSlider(self.centralwidget)
        self.horizontalSlider_6.setObjectName(u"horizontalSlider_6")
        self.horizontalSlider_6.setMinimumSize(QSize(150, 25))
        self.horizontalSlider_6.setMaximumSize(QSize(150, 25))
        self.horizontalSlider_6.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.horizontalSlider_6, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_4)


        self.verticalLayout_parameters.addLayout(self.verticalLayout_band_param)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_parameters.addItem(self.verticalSpacer_3)

        self.verticalLayout_error_detection = QVBoxLayout()
        self.verticalLayout_error_detection.setObjectName(u"verticalLayout_error_detection")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)
        self.label_10.setMinimumSize(QSize(150, 25))
        self.label_10.setMaximumSize(QSize(150, 25))
        self.label_10.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_16.addWidget(self.label_10, 0, Qt.AlignTop)


        self.verticalLayout_error_detection.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 25))
        self.label_11.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_17.addWidget(self.label_11)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMinimumSize(QSize(75, 25))
        self.comboBox_2.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_17.addWidget(self.comboBox_2)


        self.horizontalLayout_13.addLayout(self.horizontalLayout_17)


        self.verticalLayout_error_detection.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QSize(0, 25))
        self.label_12.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_15.addWidget(self.label_12)

        self.comboBox_3 = QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setMinimumSize(QSize(75, 25))
        self.comboBox_3.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_15.addWidget(self.comboBox_3)


        self.verticalLayout_error_detection.addLayout(self.horizontalLayout_15)


        self.verticalLayout_parameters.addLayout(self.verticalLayout_error_detection)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_parameters.addItem(self.verticalSpacer_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_3.addWidget(self.label_18, 0, Qt.AlignHCenter)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_34.addWidget(self.checkBox_2)

        self.comboBox_29 = QComboBox(self.centralwidget)
        self.comboBox_29.setObjectName(u"comboBox_29")

        self.horizontalLayout_34.addWidget(self.comboBox_29)


        self.verticalLayout_3.addLayout(self.horizontalLayout_34)


        self.verticalLayout_parameters.addLayout(self.verticalLayout_3)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_parameters.addItem(self.verticalSpacer_5)


        self.horizontalLayout_3.addLayout(self.verticalLayout_parameters)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.graphicsView_hypnogram = QGraphicsView(self.centralwidget)
        self.graphicsView_hypnogram.setObjectName(u"graphicsView_hypnogram")
        sizePolicy2.setHeightForWidth(self.graphicsView_hypnogram.sizePolicy().hasHeightForWidth())
        self.graphicsView_hypnogram.setSizePolicy(sizePolicy2)
        self.graphicsView_hypnogram.setMinimumSize(QSize(0, 90))
        self.graphicsView_hypnogram.setMaximumSize(QSize(16777215, 90))

        self.horizontalLayout_11.addWidget(self.graphicsView_hypnogram)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 25))
        self.label_13.setMaximumSize(QSize(16777215, 25))
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_13)

        self.comboBox_4 = QComboBox(self.centralwidget)
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setMinimumSize(QSize(0, 25))
        self.comboBox_4.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_8.addWidget(self.comboBox_4)

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


        self.verticalLayout_8.addLayout(self.horizontalLayout_19)


        self.horizontalLayout_11.addLayout(self.verticalLayout_8)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.graphicsView_spectrogram = QGraphicsView(self.centralwidget)
        self.graphicsView_spectrogram.setObjectName(u"graphicsView_spectrogram")
        sizePolicy2.setHeightForWidth(self.graphicsView_spectrogram.sizePolicy().hasHeightForWidth())
        self.graphicsView_spectrogram.setSizePolicy(sizePolicy2)
        self.graphicsView_spectrogram.setMinimumSize(QSize(0, 90))
        self.graphicsView_spectrogram.setMaximumSize(QSize(16777215, 90))

        self.horizontalLayout_18.addWidget(self.graphicsView_spectrogram)

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


        self.horizontalLayout_18.addLayout(self.verticalLayout_12)


        self.verticalLayout_6.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout_20.addWidget(self.graphicsView)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.comboBox_5 = QComboBox(self.centralwidget)
        self.comboBox_5.setObjectName(u"comboBox_5")
        self.comboBox_5.setMinimumSize(QSize(300, 25))
        self.comboBox_5.setMaximumSize(QSize(300, 25))

        self.verticalLayout_11.addWidget(self.comboBox_5, 0, Qt.AlignRight)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(300, 0))
        self.listWidget.setMaximumSize(QSize(300, 16777215))

        self.verticalLayout_11.addWidget(self.listWidget, 0, Qt.AlignRight)


        self.horizontalLayout_20.addLayout(self.verticalLayout_11)


        self.verticalLayout_6.addLayout(self.horizontalLayout_20)


        self.horizontalLayout_10.addLayout(self.verticalLayout_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1066, 23))
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
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Spectrogram", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Figures", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Markings", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Output Suffix", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Description", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Reference Method", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Reference", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Coherence", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Spectral Epoch", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Spectral Bands", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"U+03B4", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"	U+03B8", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"	U+03B1", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"	U+03C3", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"U+03B2", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"	U+0392", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Error Detection", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"	U+0394(0.6-4.6Hz)", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"	U+0392(40-60Hz)", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Multi-Processing", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"# of CPUs", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Spect.", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Heat", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

