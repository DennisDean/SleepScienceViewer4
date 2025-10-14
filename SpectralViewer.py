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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGraphicsView, QHBoxLayout, QLabel, QLayout,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QTextBrowser, QToolBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1339, 2547)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionControl_Bar = QAction(MainWindow)
        self.actionControl_Bar.setObjectName(u"actionControl_Bar")
        self.actionParameters = QAction(MainWindow)
        self.actionParameters.setObjectName(u"actionParameters")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionHypnogram = QAction(MainWindow)
        self.actionHypnogram.setObjectName(u"actionHypnogram")
        self.actionSpectrogram = QAction(MainWindow)
        self.actionSpectrogram.setObjectName(u"actionSpectrogram")
        self.actionMarkings = QAction(MainWindow)
        self.actionMarkings.setObjectName(u"actionMarkings")
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
        self.pushButton_control_settings = QPushButton(self.centralwidget)
        self.pushButton_control_settings.setObjectName(u"pushButton_control_settings")
        self.pushButton_control_settings.setMinimumSize(QSize(0, 25))
        self.pushButton_control_settings.setMaximumSize(QSize(16777215, 25))
        self.pushButton_control_settings.setCheckable(True)
        self.pushButton_control_settings.setChecked(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_settings)

        self.pushButton_control_parameters = QPushButton(self.centralwidget)
        self.pushButton_control_parameters.setObjectName(u"pushButton_control_parameters")
        self.pushButton_control_parameters.setMinimumSize(QSize(0, 25))
        self.pushButton_control_parameters.setMaximumSize(QSize(16777215, 25))
        self.pushButton_control_parameters.setCheckable(True)
        self.pushButton_control_parameters.setChecked(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_parameters)

        self.checkBox_control_coherence = QCheckBox(self.centralwidget)
        self.checkBox_control_coherence.setObjectName(u"checkBox_control_coherence")

        self.horizontalLayout_36.addWidget(self.checkBox_control_coherence)

        self.label_38 = QLabel(self.centralwidget)
        self.label_38.setObjectName(u"label_38")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy1)
        self.label_38.setMinimumSize(QSize(40, 0))
        self.label_38.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_36.addWidget(self.label_38)

        self.pushButton_control_compute = QPushButton(self.centralwidget)
        self.pushButton_control_compute.setObjectName(u"pushButton_control_compute")
        self.pushButton_control_compute.setCheckable(False)
        self.pushButton_control_compute.setChecked(False)

        self.horizontalLayout_36.addWidget(self.pushButton_control_compute)

        self.label_39 = QLabel(self.centralwidget)
        self.label_39.setObjectName(u"label_39")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_39.sizePolicy().hasHeightForWidth())
        self.label_39.setSizePolicy(sizePolicy2)

        self.horizontalLayout_36.addWidget(self.label_39)

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
        self.pushButton_control_markings.setChecked(False)

        self.horizontalLayout_36.addWidget(self.pushButton_control_markings)

        self.pushButton_control_figures = QPushButton(self.centralwidget)
        self.pushButton_control_figures.setObjectName(u"pushButton_control_figures")
        self.pushButton_control_figures.setCheckable(True)

        self.horizontalLayout_36.addWidget(self.pushButton_control_figures)


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
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)
        self.label_7.setMinimumSize(QSize(0, 20))
        self.label_7.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_s.addWidget(self.label_7)

        self.label_53 = QLabel(self.centralwidget)
        self.label_53.setObjectName(u"label_53")
        font = QFont()
        font.setPointSize(10)
        self.label_53.setFont(font)

        self.verticalLayout_s.addWidget(self.label_53)

        self.plainTextEdit_settings_description = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_settings_description.setObjectName(u"plainTextEdit_settings_description")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.plainTextEdit_settings_description.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_settings_description.setSizePolicy(sizePolicy4)
        self.plainTextEdit_settings_description.setMinimumSize(QSize(200, 25))
        self.plainTextEdit_settings_description.setMaximumSize(QSize(200, 25))

        self.verticalLayout_s.addWidget(self.plainTextEdit_settings_description)

        self.label_14 = QLabel(self.centralwidget)
        self.label_14.setObjectName(u"label_14")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy5)
        self.label_14.setMinimumSize(QSize(100, 20))
        self.label_14.setMaximumSize(QSize(100, 20))
        self.label_14.setFont(font)

        self.verticalLayout_s.addWidget(self.label_14)

        self.plainTextEdit_settings_output_suffix = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_settings_output_suffix.setObjectName(u"plainTextEdit_settings_output_suffix")
        sizePolicy4.setHeightForWidth(self.plainTextEdit_settings_output_suffix.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_settings_output_suffix.setSizePolicy(sizePolicy4)
        self.plainTextEdit_settings_output_suffix.setMinimumSize(QSize(200, 25))
        self.plainTextEdit_settings_output_suffix.setMaximumSize(QSize(200, 25))

        self.verticalLayout_s.addWidget(self.plainTextEdit_settings_output_suffix)

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

        self.label_52 = QLabel(self.centralwidget)
        self.label_52.setObjectName(u"label_52")
        sizePolicy5.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy5)
        self.label_52.setMinimumSize(QSize(150, 0))
        self.label_52.setMaximumSize(QSize(150, 16777215))
        self.label_52.setFont(font)
        self.label_52.setAlignment(Qt.AlignCenter)

        self.verticalLayout_s.addWidget(self.label_52, 0, Qt.AlignHCenter)

        self.comboBox_settings_reference_method = QComboBox(self.centralwidget)
        self.comboBox_settings_reference_method.setObjectName(u"comboBox_settings_reference_method")
        sizePolicy4.setHeightForWidth(self.comboBox_settings_reference_method.sizePolicy().hasHeightForWidth())
        self.comboBox_settings_reference_method.setSizePolicy(sizePolicy4)
        self.comboBox_settings_reference_method.setMinimumSize(QSize(150, 25))
        self.comboBox_settings_reference_method.setMaximumSize(QSize(150, 25))

        self.verticalLayout_s.addWidget(self.comboBox_settings_reference_method, 0, Qt.AlignHCenter)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_17 = QLabel(self.centralwidget)
        self.label_17.setObjectName(u"label_17")
        sizePolicy3.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy3)
        self.label_17.setMinimumSize(QSize(100, 20))
        self.label_17.setMaximumSize(QSize(100, 20))
        self.label_17.setFont(font)
        self.label_17.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_33.addWidget(self.label_17)

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        sizePolicy3.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy3)
        self.label_16.setMinimumSize(QSize(100, 20))
        self.label_16.setMaximumSize(QSize(100, 20))
        self.label_16.setFont(font)
        self.label_16.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_33.addWidget(self.label_16)


        self.verticalLayout_s.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig1 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig1.setObjectName(u"comboBox_settings_analysis_sig1")
        sizePolicy4.setHeightForWidth(self.comboBox_settings_analysis_sig1.sizePolicy().hasHeightForWidth())
        self.comboBox_settings_analysis_sig1.setSizePolicy(sizePolicy4)
        self.comboBox_settings_analysis_sig1.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig1.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig1.setFont(font)

        self.horizontalLayout_22.addWidget(self.comboBox_settings_analysis_sig1)

        self.comboBox_settings_ref_sig1 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig1.setObjectName(u"comboBox_settings_ref_sig1")
        self.comboBox_settings_ref_sig1.setMinimumSize(QSize(100, 0))
        self.comboBox_settings_ref_sig1.setMaximumSize(QSize(100, 16777215))
        self.comboBox_settings_ref_sig1.setFont(font)

        self.horizontalLayout_22.addWidget(self.comboBox_settings_ref_sig1)


        self.verticalLayout_s.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig2 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig2.setObjectName(u"comboBox_settings_analysis_sig2")
        self.comboBox_settings_analysis_sig2.setMinimumSize(QSize(100, 0))
        self.comboBox_settings_analysis_sig2.setMaximumSize(QSize(100, 16777215))
        self.comboBox_settings_analysis_sig2.setFont(font)

        self.horizontalLayout_23.addWidget(self.comboBox_settings_analysis_sig2)

        self.comboBox_settings_ref_sig2 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig2.setObjectName(u"comboBox_settings_ref_sig2")
        self.comboBox_settings_ref_sig2.setMinimumSize(QSize(100, 0))
        self.comboBox_settings_ref_sig2.setMaximumSize(QSize(100, 16777215))
        self.comboBox_settings_ref_sig2.setFont(font)

        self.horizontalLayout_23.addWidget(self.comboBox_settings_ref_sig2)


        self.verticalLayout_s.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig3 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig3.setObjectName(u"comboBox_settings_analysis_sig3")
        self.comboBox_settings_analysis_sig3.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig3.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig3.setFont(font)

        self.horizontalLayout_24.addWidget(self.comboBox_settings_analysis_sig3)

        self.comboBox_settings_ref_sig3 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig3.setObjectName(u"comboBox_settings_ref_sig3")
        self.comboBox_settings_ref_sig3.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig3.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig3.setFont(font)

        self.horizontalLayout_24.addWidget(self.comboBox_settings_ref_sig3)


        self.verticalLayout_s.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig4 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig4.setObjectName(u"comboBox_settings_analysis_sig4")
        self.comboBox_settings_analysis_sig4.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig4.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig4.setFont(font)

        self.horizontalLayout_25.addWidget(self.comboBox_settings_analysis_sig4)

        self.comboBox_settings_ref_sig4 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig4.setObjectName(u"comboBox_settings_ref_sig4")
        self.comboBox_settings_ref_sig4.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig4.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig4.setFont(font)

        self.horizontalLayout_25.addWidget(self.comboBox_settings_ref_sig4)


        self.verticalLayout_s.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig5 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig5.setObjectName(u"comboBox_settings_analysis_sig5")
        self.comboBox_settings_analysis_sig5.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig5.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig5.setFont(font)

        self.horizontalLayout_26.addWidget(self.comboBox_settings_analysis_sig5)

        self.comboBox_settings_ref_sig5 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig5.setObjectName(u"comboBox_settings_ref_sig5")
        self.comboBox_settings_ref_sig5.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig5.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig5.setFont(font)

        self.horizontalLayout_26.addWidget(self.comboBox_settings_ref_sig5)


        self.verticalLayout_s.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig6 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig6.setObjectName(u"comboBox_settings_analysis_sig6")
        self.comboBox_settings_analysis_sig6.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig6.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig6.setFont(font)

        self.horizontalLayout_27.addWidget(self.comboBox_settings_analysis_sig6)

        self.comboBox_settings_ref_sig6 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig6.setObjectName(u"comboBox_settings_ref_sig6")
        self.comboBox_settings_ref_sig6.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig6.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig6.setFont(font)

        self.horizontalLayout_27.addWidget(self.comboBox_settings_ref_sig6)


        self.verticalLayout_s.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig7 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig7.setObjectName(u"comboBox_settings_analysis_sig7")
        self.comboBox_settings_analysis_sig7.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig7.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig7.setFont(font)

        self.horizontalLayout_28.addWidget(self.comboBox_settings_analysis_sig7)

        self.comboBox_settings_ref_sig7 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig7.setObjectName(u"comboBox_settings_ref_sig7")
        self.comboBox_settings_ref_sig7.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig7.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig7.setFont(font)

        self.horizontalLayout_28.addWidget(self.comboBox_settings_ref_sig7)


        self.verticalLayout_s.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig8 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig8.setObjectName(u"comboBox_settings_analysis_sig8")
        self.comboBox_settings_analysis_sig8.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig8.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig8.setFont(font)

        self.horizontalLayout_31.addWidget(self.comboBox_settings_analysis_sig8)

        self.comboBox_settings_ref_sig8 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig8.setObjectName(u"comboBox_settings_ref_sig8")
        self.comboBox_settings_ref_sig8.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig8.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig8.setFont(font)

        self.horizontalLayout_31.addWidget(self.comboBox_settings_ref_sig8)


        self.verticalLayout_s.addLayout(self.horizontalLayout_31)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig9 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig9.setObjectName(u"comboBox_settings_analysis_sig9")
        self.comboBox_settings_analysis_sig9.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig9.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig9.setFont(font)

        self.horizontalLayout_29.addWidget(self.comboBox_settings_analysis_sig9)

        self.comboBox_settings_ref_sig9 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig9.setObjectName(u"comboBox_settings_ref_sig9")
        self.comboBox_settings_ref_sig9.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig9.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig9.setFont(font)

        self.horizontalLayout_29.addWidget(self.comboBox_settings_ref_sig9)


        self.verticalLayout_s.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setSizeConstraint(QLayout.SetMinimumSize)
        self.comboBox_settings_analysis_sig10 = QComboBox(self.centralwidget)
        self.comboBox_settings_analysis_sig10.setObjectName(u"comboBox_settings_analysis_sig10")
        self.comboBox_settings_analysis_sig10.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig10.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_analysis_sig10.setFont(font)

        self.horizontalLayout_30.addWidget(self.comboBox_settings_analysis_sig10)

        self.comboBox_settings_ref_sig10 = QComboBox(self.centralwidget)
        self.comboBox_settings_ref_sig10.setObjectName(u"comboBox_settings_ref_sig10")
        self.comboBox_settings_ref_sig10.setMinimumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig10.setMaximumSize(QSize(100, 25))
        self.comboBox_settings_ref_sig10.setFont(font)

        self.horizontalLayout_30.addWidget(self.comboBox_settings_ref_sig10)


        self.verticalLayout_s.addLayout(self.horizontalLayout_30)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setMinimumSize(QSize(0, 20))
        self.line_5.setMaximumSize(QSize(16777215, 20))
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_5)

        self.label_47 = QLabel(self.centralwidget)
        self.label_47.setObjectName(u"label_47")

        self.verticalLayout_6.addWidget(self.label_47)

        self.checkBox_plotting_xlabels = QCheckBox(self.centralwidget)
        self.checkBox_plotting_xlabels.setObjectName(u"checkBox_plotting_xlabels")

        self.verticalLayout_6.addWidget(self.checkBox_plotting_xlabels)


        self.verticalLayout_s.addLayout(self.verticalLayout_6)

        self.verticalLayout_window_size_2 = QVBoxLayout()
        self.verticalLayout_window_size_2.setObjectName(u"verticalLayout_window_size_2")
        self.line_9 = QFrame(self.centralwidget)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_window_size_2.addWidget(self.line_9)

        self.label_27 = QLabel(self.centralwidget)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_window_size_2.addWidget(self.label_27)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.checkBox_settings_band = QCheckBox(self.centralwidget)
        self.checkBox_settings_band.setObjectName(u"checkBox_settings_band")
        self.checkBox_settings_band.setMinimumSize(QSize(0, 20))
        self.checkBox_settings_band.setMaximumSize(QSize(16777215, 20))
        self.checkBox_settings_band.setFont(font)

        self.verticalLayout_18.addWidget(self.checkBox_settings_band, 0, Qt.AlignTop)

        self.comboBox_settings_band_low = QComboBox(self.centralwidget)
        self.comboBox_settings_band_low.setObjectName(u"comboBox_settings_band_low")
        self.comboBox_settings_band_low.setFont(font)

        self.verticalLayout_18.addWidget(self.comboBox_settings_band_low, 0, Qt.AlignTop)

        self.comboBox_settings_band_high = QComboBox(self.centralwidget)
        self.comboBox_settings_band_high.setObjectName(u"comboBox_settings_band_high")
        self.comboBox_settings_band_high.setFont(font)

        self.verticalLayout_18.addWidget(self.comboBox_settings_band_high, 0, Qt.AlignTop)

        self.label_35 = QLabel(self.centralwidget)
        self.label_35.setObjectName(u"label_35")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy6)

        self.verticalLayout_18.addWidget(self.label_35)


        self.horizontalLayout_39.addLayout(self.verticalLayout_18)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.checkBox_settings_notch = QCheckBox(self.centralwidget)
        self.checkBox_settings_notch.setObjectName(u"checkBox_settings_notch")
        self.checkBox_settings_notch.setMinimumSize(QSize(0, 20))
        self.checkBox_settings_notch.setMaximumSize(QSize(16777215, 20))
        self.checkBox_settings_notch.setFont(font)

        self.verticalLayout_19.addWidget(self.checkBox_settings_notch, 0, Qt.AlignTop)

        self.comboBox_settings_notch = QComboBox(self.centralwidget)
        self.comboBox_settings_notch.setObjectName(u"comboBox_settings_notch")
        self.comboBox_settings_notch.setFont(font)

        self.verticalLayout_19.addWidget(self.comboBox_settings_notch, 0, Qt.AlignTop)

        self.label_36 = QLabel(self.centralwidget)
        self.label_36.setObjectName(u"label_36")
        sizePolicy6.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy6)

        self.verticalLayout_19.addWidget(self.label_36)


        self.horizontalLayout_39.addLayout(self.verticalLayout_19)


        self.verticalLayout_window_size_2.addLayout(self.horizontalLayout_39)


        self.verticalLayout_s.addLayout(self.verticalLayout_window_size_2)

        self.label_37 = QLabel(self.centralwidget)
        self.label_37.setObjectName(u"label_37")
        sizePolicy6.setHeightForWidth(self.label_37.sizePolicy().hasHeightForWidth())
        self.label_37.setSizePolicy(sizePolicy6)

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
        sizePolicy5.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy5)
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
        sizePolicy1.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy1)
        self.label_11.setMinimumSize(QSize(100, 20))
        self.label_11.setMaximumSize(QSize(100, 20))
        self.label_11.setFont(font)
        self.label_11.setLayoutDirection(Qt.RightToLeft)
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.label_11, 0, Qt.AlignRight)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy5.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy5)
        self.label_5.setMinimumSize(QSize(30, 0))
        self.label_5.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_17.addWidget(self.label_5)

        self.comboBox_parameters_noise_delta = QComboBox(self.centralwidget)
        self.comboBox_parameters_noise_delta.setObjectName(u"comboBox_parameters_noise_delta")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_noise_delta.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_noise_delta.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_noise_delta.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_noise_delta.setMaximumSize(QSize(75, 25))
        self.comboBox_parameters_noise_delta.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_17.addWidget(self.comboBox_parameters_noise_delta, 0, Qt.AlignRight)

        self.label_50 = QLabel(self.centralwidget)
        self.label_50.setObjectName(u"label_50")
        sizePolicy5.setHeightForWidth(self.label_50.sizePolicy().hasHeightForWidth())
        self.label_50.setSizePolicy(sizePolicy5)
        self.label_50.setMinimumSize(QSize(20, 20))
        self.label_50.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_17.addWidget(self.label_50)


        self.horizontalLayout_13.addLayout(self.horizontalLayout_17)


        self.verticalLayout_error_detection.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setSizeConstraint(QLayout.SetFixedSize)
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy5.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy5)
        self.label_12.setMinimumSize(QSize(100, 20))
        self.label_12.setMaximumSize(QSize(100, 20))
        self.label_12.setFont(font)
        self.label_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.label_12, 0, Qt.AlignLeft)

        self.label_26 = QLabel(self.centralwidget)
        self.label_26.setObjectName(u"label_26")
        sizePolicy1.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy1)
        self.label_26.setMinimumSize(QSize(30, 0))
        self.label_26.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_15.addWidget(self.label_26)

        self.comboBox_parameters_noise_beta = QComboBox(self.centralwidget)
        self.comboBox_parameters_noise_beta.setObjectName(u"comboBox_parameters_noise_beta")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_noise_beta.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_noise_beta.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_noise_beta.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_noise_beta.setMaximumSize(QSize(75, 25))
        self.comboBox_parameters_noise_beta.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_15.addWidget(self.comboBox_parameters_noise_beta, 0, Qt.AlignRight)

        self.label_51 = QLabel(self.centralwidget)
        self.label_51.setObjectName(u"label_51")

        self.horizontalLayout_15.addWidget(self.label_51)


        self.verticalLayout_error_detection.addLayout(self.horizontalLayout_15)


        self.verticalLayout_p.addLayout(self.verticalLayout_error_detection)

        self.line_6 = QFrame(self.centralwidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setMinimumSize(QSize(0, 20))
        self.line_6.setMaximumSize(QSize(16777215, 20))
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_p.addWidget(self.line_6)

        self.label_28 = QLabel(self.centralwidget)
        self.label_28.setObjectName(u"label_28")
        sizePolicy1.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy1)
        self.label_28.setAlignment(Qt.AlignCenter)

        self.verticalLayout_p.addWidget(self.label_28, 0, Qt.AlignHCenter)

        self.verticalLayout_window_size = QVBoxLayout()
        self.verticalLayout_window_size.setObjectName(u"verticalLayout_window_size")
        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName(u"label_19")
        sizePolicy1.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy1)
        self.label_19.setMinimumSize(QSize(100, 20))
        self.label_19.setMaximumSize(QSize(100, 20))
        self.label_19.setFont(font)

        self.verticalLayout_window_size.addWidget(self.label_19, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_31 = QLabel(self.centralwidget)
        self.label_31.setObjectName(u"label_31")
        sizePolicy1.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy1)
        self.label_31.setMinimumSize(QSize(50, 0))
        self.label_31.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_37.addWidget(self.label_31)

        self.label_21 = QLabel(self.centralwidget)
        self.label_21.setObjectName(u"label_21")
        sizePolicy1.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy1)
        self.label_21.setMinimumSize(QSize(75, 0))
        self.label_21.setMaximumSize(QSize(75, 16777215))
        self.label_21.setFont(font)
        self.label_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_37.addWidget(self.label_21, 0, Qt.AlignRight)

        self.comboBox_parameters_taper_window = QComboBox(self.centralwidget)
        self.comboBox_parameters_taper_window.setObjectName(u"comboBox_parameters_taper_window")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_taper_window.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_taper_window.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_taper_window.setMinimumSize(QSize(75, 0))
        self.comboBox_parameters_taper_window.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_37.addWidget(self.comboBox_parameters_taper_window, 0, Qt.AlignRight)

        self.label_48 = QLabel(self.centralwidget)
        self.label_48.setObjectName(u"label_48")
        sizePolicy5.setHeightForWidth(self.label_48.sizePolicy().hasHeightForWidth())
        self.label_48.setSizePolicy(sizePolicy5)
        self.label_48.setMinimumSize(QSize(20, 20))
        self.label_48.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_37.addWidget(self.label_48)


        self.verticalLayout_window_size.addLayout(self.horizontalLayout_37)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_32 = QLabel(self.centralwidget)
        self.label_32.setObjectName(u"label_32")
        sizePolicy1.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy1)
        self.label_32.setMinimumSize(QSize(50, 0))
        self.label_32.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_35.addWidget(self.label_32)

        self.label_20 = QLabel(self.centralwidget)
        self.label_20.setObjectName(u"label_20")
        sizePolicy1.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy1)
        self.label_20.setMinimumSize(QSize(75, 0))
        self.label_20.setMaximumSize(QSize(75, 16777215))
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_35.addWidget(self.label_20, 0, Qt.AlignRight)

        self.comboBox_parameters_taper_step = QComboBox(self.centralwidget)
        self.comboBox_parameters_taper_step.setObjectName(u"comboBox_parameters_taper_step")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_taper_step.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_taper_step.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_taper_step.setMinimumSize(QSize(75, 0))
        self.comboBox_parameters_taper_step.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_35.addWidget(self.comboBox_parameters_taper_step, 0, Qt.AlignRight)

        self.label_49 = QLabel(self.centralwidget)
        self.label_49.setObjectName(u"label_49")
        sizePolicy5.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy5)
        self.label_49.setMinimumSize(QSize(20, 20))
        self.label_49.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_35.addWidget(self.label_49)


        self.verticalLayout_window_size.addLayout(self.horizontalLayout_35)


        self.verticalLayout_p.addLayout(self.verticalLayout_window_size)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")
        sizePolicy1.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy1)
        self.label_18.setFont(font)

        self.verticalLayout_3.addWidget(self.label_18, 0, Qt.AlignLeft)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setSizeConstraint(QLayout.SetFixedSize)
        self.label_33 = QLabel(self.centralwidget)
        self.label_33.setObjectName(u"label_33")
        sizePolicy1.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy1)
        self.label_33.setMinimumSize(QSize(50, 0))
        self.label_33.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_34.addWidget(self.label_33)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        sizePolicy5.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy5)
        self.checkBox_2.setMinimumSize(QSize(100, 20))
        self.checkBox_2.setMaximumSize(QSize(100, 20))
        self.checkBox_2.setFont(font)
        self.checkBox_2.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_34.addWidget(self.checkBox_2, 0, Qt.AlignLeft)

        self.comboBox_parameters_taper_num_cpus = QComboBox(self.centralwidget)
        self.comboBox_parameters_taper_num_cpus.setObjectName(u"comboBox_parameters_taper_num_cpus")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_taper_num_cpus.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_taper_num_cpus.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_taper_num_cpus.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_taper_num_cpus.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_34.addWidget(self.comboBox_parameters_taper_num_cpus)


        self.verticalLayout_3.addLayout(self.horizontalLayout_34)


        self.verticalLayout_p.addLayout(self.verticalLayout_3)

        self.line_7 = QFrame(self.centralwidget)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setMinimumSize(QSize(0, 20))
        self.line_7.setMaximumSize(QSize(16777215, 20))
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_p.addWidget(self.line_7)

        self.verticalLayout_band_param = QVBoxLayout()
        self.verticalLayout_band_param.setObjectName(u"verticalLayout_band_param")
        self.verticalLayout_band_param.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
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
        sizePolicy5.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy5)
        self.label.setMinimumSize(QSize(25, 20))
        self.label.setMaximumSize(QSize(25, 20))
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label, 0, Qt.AlignLeft)

        self.comboBox_parameters_band_delta_low = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_delta_low.setObjectName(u"comboBox_parameters_band_delta_low")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_delta_low.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_delta_low.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_delta_low.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_delta_low.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_8.addWidget(self.comboBox_parameters_band_delta_low, 0, Qt.AlignRight)

        self.label_41 = QLabel(self.centralwidget)
        self.label_41.setObjectName(u"label_41")
        self.label_41.setMinimumSize(QSize(10, 20))
        self.label_41.setMaximumSize(QSize(10, 20))
        self.label_41.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_41)

        self.comboBox_parameters_band_delta_high = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_delta_high.setObjectName(u"comboBox_parameters_band_delta_high")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_delta_high.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_delta_high.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_delta_high.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_delta_high.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_8.addWidget(self.comboBox_parameters_band_delta_high, 0, Qt.AlignRight)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(20, 20))
        self.label_8.setMaximumSize(QSize(20, 20))
        self.label_8.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_8)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy5.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy5)
        self.label_2.setMinimumSize(QSize(25, 20))
        self.label_2.setMaximumSize(QSize(25, 20))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_2, 0, Qt.AlignLeft|Qt.AlignTop)

        self.comboBox_parameters_band_theta_low = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_theta_low.setObjectName(u"comboBox_parameters_band_theta_low")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_theta_low.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_theta_low.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_theta_low.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_theta_low.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_7.addWidget(self.comboBox_parameters_band_theta_low, 0, Qt.AlignRight)

        self.label_42 = QLabel(self.centralwidget)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(10, 20))
        self.label_42.setMaximumSize(QSize(10, 20))
        self.label_42.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label_42)

        self.comboBox_parameters_band_theta_high = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_theta_high.setObjectName(u"comboBox_parameters_band_theta_high")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_theta_high.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_theta_high.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_theta_high.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_theta_high.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_7.addWidget(self.comboBox_parameters_band_theta_high, 0, Qt.AlignRight)

        self.label_24 = QLabel(self.centralwidget)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMinimumSize(QSize(20, 20))
        self.label_24.setMaximumSize(QSize(20, 20))
        self.label_24.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_24)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy5.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy5)
        self.label_3.setMinimumSize(QSize(25, 20))
        self.label_3.setMaximumSize(QSize(25, 20))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_6.addWidget(self.label_3, 0, Qt.AlignLeft|Qt.AlignTop)

        self.comboBox_parameters_band_alpha_low = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_alpha_low.setObjectName(u"comboBox_parameters_band_alpha_low")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_alpha_low.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_alpha_low.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_alpha_low.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_alpha_low.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_6.addWidget(self.comboBox_parameters_band_alpha_low, 0, Qt.AlignRight)

        self.label_43 = QLabel(self.centralwidget)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMinimumSize(QSize(10, 20))
        self.label_43.setMaximumSize(QSize(10, 20))
        self.label_43.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.label_43)

        self.comboBox_parameters_band_alpha_high = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_alpha_high.setObjectName(u"comboBox_parameters_band_alpha_high")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_alpha_high.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_alpha_high.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_alpha_high.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_alpha_high.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_6.addWidget(self.comboBox_parameters_band_alpha_high, 0, Qt.AlignRight)

        self.label_25 = QLabel(self.centralwidget)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setMinimumSize(QSize(20, 20))
        self.label_25.setMaximumSize(QSize(20, 20))
        self.label_25.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_25)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy5.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy5)
        self.label_4.setMinimumSize(QSize(25, 20))
        self.label_4.setMaximumSize(QSize(25, 20))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_4, 0, Qt.AlignLeft|Qt.AlignTop)

        self.comboBox_parameters_band_sigma_low = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_sigma_low.setObjectName(u"comboBox_parameters_band_sigma_low")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_sigma_low.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_sigma_low.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_sigma_low.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_sigma_low.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_5.addWidget(self.comboBox_parameters_band_sigma_low, 0, Qt.AlignRight)

        self.label_44 = QLabel(self.centralwidget)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setMinimumSize(QSize(10, 20))
        self.label_44.setMaximumSize(QSize(10, 20))
        self.label_44.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_44)

        self.comboBox_parameters_band_sigma_high = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_sigma_high.setObjectName(u"comboBox_parameters_band_sigma_high")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_sigma_high.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_sigma_high.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_sigma_high.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_sigma_high.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_5.addWidget(self.comboBox_parameters_band_sigma_high, 0, Qt.AlignRight)

        self.label_29 = QLabel(self.centralwidget)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setMinimumSize(QSize(20, 20))
        self.label_29.setMaximumSize(QSize(20, 20))
        self.label_29.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_29)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_22 = QLabel(self.centralwidget)
        self.label_22.setObjectName(u"label_22")
        sizePolicy5.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy5)
        self.label_22.setMinimumSize(QSize(25, 20))
        self.label_22.setMaximumSize(QSize(25, 20))
        self.label_22.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_22)

        self.comboBox_parameters_band_beta_low = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_beta_low.setObjectName(u"comboBox_parameters_band_beta_low")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_beta_low.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_beta_low.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_beta_low.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_beta_low.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_9.addWidget(self.comboBox_parameters_band_beta_low, 0, Qt.AlignRight)

        self.label_45 = QLabel(self.centralwidget)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setMinimumSize(QSize(10, 20))
        self.label_45.setMaximumSize(QSize(10, 20))
        self.label_45.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_45)

        self.comboBox_parameters_band_beta_high = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_beta_high.setObjectName(u"comboBox_parameters_band_beta_high")
        self.comboBox_parameters_band_beta_high.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_beta_high.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_9.addWidget(self.comboBox_parameters_band_beta_high)

        self.label_30 = QLabel(self.centralwidget)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setMinimumSize(QSize(20, 20))
        self.label_30.setMaximumSize(QSize(20, 20))
        self.label_30.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_30)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy5.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy5)
        self.label_6.setMinimumSize(QSize(25, 25))
        self.label_6.setMaximumSize(QSize(25, 25))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_6, 0, Qt.AlignLeft|Qt.AlignTop)

        self.comboBox_parameters_band_gamma_low = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_gamma_low.setObjectName(u"comboBox_parameters_band_gamma_low")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_gamma_low.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_gamma_low.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_gamma_low.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_gamma_low.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_4.addWidget(self.comboBox_parameters_band_gamma_low, 0, Qt.AlignRight)

        self.label_46 = QLabel(self.centralwidget)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(10, 20))
        self.label_46.setMaximumSize(QSize(10, 20))
        self.label_46.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_46)

        self.comboBox_parameters_band_gamma_high = QComboBox(self.centralwidget)
        self.comboBox_parameters_band_gamma_high.setObjectName(u"comboBox_parameters_band_gamma_high")
        sizePolicy5.setHeightForWidth(self.comboBox_parameters_band_gamma_high.sizePolicy().hasHeightForWidth())
        self.comboBox_parameters_band_gamma_high.setSizePolicy(sizePolicy5)
        self.comboBox_parameters_band_gamma_high.setMinimumSize(QSize(75, 25))
        self.comboBox_parameters_band_gamma_high.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_4.addWidget(self.comboBox_parameters_band_gamma_high, 0, Qt.AlignRight)

        self.label_40 = QLabel(self.centralwidget)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(20, 20))
        self.label_40.setMaximumSize(QSize(20, 20))
        self.label_40.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_40)


        self.verticalLayout_band_param.addLayout(self.horizontalLayout_4)


        self.verticalLayout_p.addLayout(self.verticalLayout_band_param)

        self.line_8 = QFrame(self.centralwidget)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_p.addWidget(self.line_8)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_23 = QLabel(self.centralwidget)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_4.addWidget(self.label_23)


        self.verticalLayout_p.addLayout(self.verticalLayout_4)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy5.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy5)
        self.textBrowser.setMinimumSize(QSize(240, 150))
        self.textBrowser.setMaximumSize(QSize(240, 150))

        self.verticalLayout_p.addWidget(self.textBrowser)

        self.label_34 = QLabel(self.centralwidget)
        self.label_34.setObjectName(u"label_34")
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

        self.comboBox_hynogram = QComboBox(self.centralwidget)
        self.comboBox_hynogram.setObjectName(u"comboBox_hynogram")
        sizePolicy5.setHeightForWidth(self.comboBox_hynogram.sizePolicy().hasHeightForWidth())
        self.comboBox_hynogram.setSizePolicy(sizePolicy5)
        self.comboBox_hynogram.setMinimumSize(QSize(95, 25))
        self.comboBox_hynogram.setMaximumSize(QSize(95, 25))

        self.verticalLayout_hypnogram_control.addWidget(self.comboBox_hynogram)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.pushButton_hypnogram_show_stages = QPushButton(self.centralwidget)
        self.pushButton_hypnogram_show_stages.setObjectName(u"pushButton_hypnogram_show_stages")
        sizePolicy5.setHeightForWidth(self.pushButton_hypnogram_show_stages.sizePolicy().hasHeightForWidth())
        self.pushButton_hypnogram_show_stages.setSizePolicy(sizePolicy5)
        self.pushButton_hypnogram_show_stages.setMinimumSize(QSize(62, 25))
        self.pushButton_hypnogram_show_stages.setMaximumSize(QSize(62, 25))
        self.pushButton_hypnogram_show_stages.setCheckable(True)
        self.pushButton_hypnogram_show_stages.setChecked(True)

        self.horizontalLayout_19.addWidget(self.pushButton_hypnogram_show_stages, 0, Qt.AlignTop)

        self.pushButton_hypnogram_legend = QPushButton(self.centralwidget)
        self.pushButton_hypnogram_legend.setObjectName(u"pushButton_hypnogram_legend")
        sizePolicy5.setHeightForWidth(self.pushButton_hypnogram_legend.sizePolicy().hasHeightForWidth())
        self.pushButton_hypnogram_legend.setSizePolicy(sizePolicy5)
        self.pushButton_hypnogram_legend.setMinimumSize(QSize(25, 25))
        self.pushButton_hypnogram_legend.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_19.addWidget(self.pushButton_hypnogram_legend, 0, Qt.AlignTop)


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
        self.comboBox_spectrogram_signals = QComboBox(self.centralwidget)
        self.comboBox_spectrogram_signals.setObjectName(u"comboBox_spectrogram_signals")
        self.comboBox_spectrogram_signals.setMinimumSize(QSize(95, 25))
        self.comboBox_spectrogram_signals.setMaximumSize(QSize(95, 25))

        self.verticalLayout_12.addWidget(self.comboBox_spectrogram_signals)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.pushButton_spectrogram_show = QPushButton(self.centralwidget)
        self.pushButton_spectrogram_show.setObjectName(u"pushButton_spectrogram_show")
        self.pushButton_spectrogram_show.setMinimumSize(QSize(62, 25))
        self.pushButton_spectrogram_show.setMaximumSize(QSize(62, 25))

        self.horizontalLayout_14.addWidget(self.pushButton_spectrogram_show, 0, Qt.AlignTop)

        self.pushButton_spectrogram_legend = QPushButton(self.centralwidget)
        self.pushButton_spectrogram_legend.setObjectName(u"pushButton_spectrogram_legend")
        self.pushButton_spectrogram_legend.setMinimumSize(QSize(25, 25))
        self.pushButton_spectrogram_legend.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_14.addWidget(self.pushButton_spectrogram_legend, 0, Qt.AlignTop)


        self.verticalLayout_12.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.pushButton_spectrogram_heatmap_show = QPushButton(self.centralwidget)
        self.pushButton_spectrogram_heatmap_show.setObjectName(u"pushButton_spectrogram_heatmap_show")
        self.pushButton_spectrogram_heatmap_show.setMinimumSize(QSize(62, 0))
        self.pushButton_spectrogram_heatmap_show.setMaximumSize(QSize(62, 16777215))

        self.horizontalLayout_21.addWidget(self.pushButton_spectrogram_heatmap_show, 0, Qt.AlignTop)

        self.pushButton_sectrogram_heatmap_legend = QPushButton(self.centralwidget)
        self.pushButton_sectrogram_heatmap_legend.setObjectName(u"pushButton_sectrogram_heatmap_legend")
        self.pushButton_sectrogram_heatmap_legend.setMinimumSize(QSize(25, 0))
        self.pushButton_sectrogram_heatmap_legend.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_21.addWidget(self.pushButton_sectrogram_heatmap_legend, 0, Qt.AlignTop)


        self.verticalLayout_12.addLayout(self.horizontalLayout_21)


        self.horizontalLayout_spectrogram.addLayout(self.verticalLayout_12)


        self.verticalLayout_m.addLayout(self.horizontalLayout_spectrogram)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.verticalLayout_spectral_results = QVBoxLayout()
        self.verticalLayout_spectral_results.setObjectName(u"verticalLayout_spectral_results")
        self.horizontalLayout_results_1 = QHBoxLayout()
        self.horizontalLayout_results_1.setObjectName(u"horizontalLayout_results_1")
        self.graphicsView_results_1 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_1.setObjectName(u"graphicsView_results_1")
        self.graphicsView_results_1.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_1.addWidget(self.graphicsView_results_1)

        self.label_results_1 = QLabel(self.centralwidget)
        self.label_results_1.setObjectName(u"label_results_1")
        sizePolicy5.setHeightForWidth(self.label_results_1.sizePolicy().hasHeightForWidth())
        self.label_results_1.setSizePolicy(sizePolicy5)
        self.label_results_1.setMinimumSize(QSize(95, 25))
        self.label_results_1.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_1.addWidget(self.label_results_1)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_1)

        self.horizontalLayout_results_2 = QHBoxLayout()
        self.horizontalLayout_results_2.setObjectName(u"horizontalLayout_results_2")
        self.graphicsView_results_2 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_2.setObjectName(u"graphicsView_results_2")
        self.graphicsView_results_2.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_2.addWidget(self.graphicsView_results_2)

        self.label_results_2 = QLabel(self.centralwidget)
        self.label_results_2.setObjectName(u"label_results_2")
        sizePolicy5.setHeightForWidth(self.label_results_2.sizePolicy().hasHeightForWidth())
        self.label_results_2.setSizePolicy(sizePolicy5)
        self.label_results_2.setMinimumSize(QSize(95, 25))
        self.label_results_2.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_2.addWidget(self.label_results_2)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_2)

        self.horizontalLayout_results_3 = QHBoxLayout()
        self.horizontalLayout_results_3.setObjectName(u"horizontalLayout_results_3")
        self.graphicsView_results_3 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_3.setObjectName(u"graphicsView_results_3")
        self.graphicsView_results_3.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_3.addWidget(self.graphicsView_results_3)

        self.label_results_3 = QLabel(self.centralwidget)
        self.label_results_3.setObjectName(u"label_results_3")
        sizePolicy5.setHeightForWidth(self.label_results_3.sizePolicy().hasHeightForWidth())
        self.label_results_3.setSizePolicy(sizePolicy5)
        self.label_results_3.setMinimumSize(QSize(95, 25))
        self.label_results_3.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_3.addWidget(self.label_results_3)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_3)

        self.horizontalLayout_results_4 = QHBoxLayout()
        self.horizontalLayout_results_4.setObjectName(u"horizontalLayout_results_4")
        self.graphicsView_results_4 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_4.setObjectName(u"graphicsView_results_4")
        self.graphicsView_results_4.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_4.addWidget(self.graphicsView_results_4)

        self.label_results_4 = QLabel(self.centralwidget)
        self.label_results_4.setObjectName(u"label_results_4")
        sizePolicy5.setHeightForWidth(self.label_results_4.sizePolicy().hasHeightForWidth())
        self.label_results_4.setSizePolicy(sizePolicy5)
        self.label_results_4.setMinimumSize(QSize(95, 25))
        self.label_results_4.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_4.addWidget(self.label_results_4)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_4)

        self.horizontalLayout_results_5 = QHBoxLayout()
        self.horizontalLayout_results_5.setObjectName(u"horizontalLayout_results_5")
        self.graphicsView_results_5 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_5.setObjectName(u"graphicsView_results_5")
        self.graphicsView_results_5.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_5.addWidget(self.graphicsView_results_5)

        self.label_results_5 = QLabel(self.centralwidget)
        self.label_results_5.setObjectName(u"label_results_5")
        sizePolicy5.setHeightForWidth(self.label_results_5.sizePolicy().hasHeightForWidth())
        self.label_results_5.setSizePolicy(sizePolicy5)
        self.label_results_5.setMinimumSize(QSize(95, 25))
        self.label_results_5.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_5.addWidget(self.label_results_5)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_5)

        self.horizontalLayout_results_6 = QHBoxLayout()
        self.horizontalLayout_results_6.setObjectName(u"horizontalLayout_results_6")
        self.graphicsView_results_6 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_6.setObjectName(u"graphicsView_results_6")
        self.graphicsView_results_6.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_6.addWidget(self.graphicsView_results_6)

        self.label_results_6 = QLabel(self.centralwidget)
        self.label_results_6.setObjectName(u"label_results_6")
        sizePolicy5.setHeightForWidth(self.label_results_6.sizePolicy().hasHeightForWidth())
        self.label_results_6.setSizePolicy(sizePolicy5)
        self.label_results_6.setMinimumSize(QSize(95, 25))
        self.label_results_6.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_6.addWidget(self.label_results_6)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_6)

        self.horizontalLayout_results_7 = QHBoxLayout()
        self.horizontalLayout_results_7.setObjectName(u"horizontalLayout_results_7")
        self.graphicsView_results_7 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_7.setObjectName(u"graphicsView_results_7")
        self.graphicsView_results_7.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_7.addWidget(self.graphicsView_results_7)

        self.label_results_7 = QLabel(self.centralwidget)
        self.label_results_7.setObjectName(u"label_results_7")
        sizePolicy5.setHeightForWidth(self.label_results_7.sizePolicy().hasHeightForWidth())
        self.label_results_7.setSizePolicy(sizePolicy5)
        self.label_results_7.setMinimumSize(QSize(95, 25))
        self.label_results_7.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_7.addWidget(self.label_results_7)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_7)

        self.horizontalLayout_results_8 = QHBoxLayout()
        self.horizontalLayout_results_8.setObjectName(u"horizontalLayout_results_8")
        self.graphicsView_results_8 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_8.setObjectName(u"graphicsView_results_8")
        self.graphicsView_results_8.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_8.addWidget(self.graphicsView_results_8)

        self.label_results_8 = QLabel(self.centralwidget)
        self.label_results_8.setObjectName(u"label_results_8")
        sizePolicy5.setHeightForWidth(self.label_results_8.sizePolicy().hasHeightForWidth())
        self.label_results_8.setSizePolicy(sizePolicy5)
        self.label_results_8.setMinimumSize(QSize(95, 25))
        self.label_results_8.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_8.addWidget(self.label_results_8)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_8)

        self.horizontalLayout_results_9 = QHBoxLayout()
        self.horizontalLayout_results_9.setObjectName(u"horizontalLayout_results_9")
        self.graphicsView_results_9 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_9.setObjectName(u"graphicsView_results_9")
        self.graphicsView_results_9.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_9.addWidget(self.graphicsView_results_9)

        self.label_results_9 = QLabel(self.centralwidget)
        self.label_results_9.setObjectName(u"label_results_9")
        sizePolicy5.setHeightForWidth(self.label_results_9.sizePolicy().hasHeightForWidth())
        self.label_results_9.setSizePolicy(sizePolicy5)
        self.label_results_9.setMinimumSize(QSize(95, 25))
        self.label_results_9.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_9.addWidget(self.label_results_9)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_9)

        self.horizontalLayout_results_10 = QHBoxLayout()
        self.horizontalLayout_results_10.setObjectName(u"horizontalLayout_results_10")
        self.graphicsView_results_10 = QGraphicsView(self.centralwidget)
        self.graphicsView_results_10.setObjectName(u"graphicsView_results_10")
        self.graphicsView_results_10.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_results_10.addWidget(self.graphicsView_results_10)

        self.label_results_10 = QLabel(self.centralwidget)
        self.label_results_10.setObjectName(u"label_results_10")
        sizePolicy5.setHeightForWidth(self.label_results_10.sizePolicy().hasHeightForWidth())
        self.label_results_10.setSizePolicy(sizePolicy5)
        self.label_results_10.setMinimumSize(QSize(95, 25))
        self.label_results_10.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_results_10.addWidget(self.label_results_10)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_results_10)

        self.horizontalLayout_time_axis = QHBoxLayout()
        self.horizontalLayout_time_axis.setObjectName(u"horizontalLayout_time_axis")
        self.graphicsView_time_axis = QGraphicsView(self.centralwidget)
        self.graphicsView_time_axis.setObjectName(u"graphicsView_time_axis")
        sizePolicy7.setHeightForWidth(self.graphicsView_time_axis.sizePolicy().hasHeightForWidth())
        self.graphicsView_time_axis.setSizePolicy(sizePolicy7)
        self.graphicsView_time_axis.setMinimumSize(QSize(0, 40))
        self.graphicsView_time_axis.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_time_axis.addWidget(self.graphicsView_time_axis)

        self.label_results_time = QLabel(self.centralwidget)
        self.label_results_time.setObjectName(u"label_results_time")
        sizePolicy5.setHeightForWidth(self.label_results_time.sizePolicy().hasHeightForWidth())
        self.label_results_time.setSizePolicy(sizePolicy5)
        self.label_results_time.setMinimumSize(QSize(95, 0))
        self.label_results_time.setMaximumSize(QSize(95, 16777215))
        self.label_results_time.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_time_axis.addWidget(self.label_results_time)


        self.verticalLayout_spectral_results.addLayout(self.horizontalLayout_time_axis)


        self.horizontalLayout_20.addLayout(self.verticalLayout_spectral_results)

        self.verticalLayout_mark = QVBoxLayout()
        self.verticalLayout_mark.setObjectName(u"verticalLayout_mark")
        self.comboBox_mark = QComboBox(self.centralwidget)
        self.comboBox_mark.setObjectName(u"comboBox_mark")
        sizePolicy5.setHeightForWidth(self.comboBox_mark.sizePolicy().hasHeightForWidth())
        self.comboBox_mark.setSizePolicy(sizePolicy5)
        self.comboBox_mark.setMinimumSize(QSize(200, 0))
        self.comboBox_mark.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_mark.addWidget(self.comboBox_mark)

        self.listWidget_mark = QListWidget(self.centralwidget)
        self.listWidget_mark.setObjectName(u"listWidget_mark")
        sizePolicy6.setHeightForWidth(self.listWidget_mark.sizePolicy().hasHeightForWidth())
        self.listWidget_mark.setSizePolicy(sizePolicy6)
        self.listWidget_mark.setMinimumSize(QSize(200, 0))
        self.listWidget_mark.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_mark.addWidget(self.listWidget_mark)


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
        self.menuShow = QMenu(self.menubar)
        self.menuShow.setObjectName(u"menuShow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuShow.menuAction())
        self.menuShow.addAction(self.actionControl_Bar)
        self.menuShow.addSeparator()
        self.menuShow.addAction(self.actionParameters)
        self.menuShow.addAction(self.actionSettings)
        self.menuShow.addSeparator()
        self.menuShow.addAction(self.actionHypnogram)
        self.menuShow.addAction(self.actionSpectrogram)
        self.menuShow.addAction(self.actionMarkings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionControl_Bar.setText(QCoreApplication.translate("MainWindow", u"Control Bar", None))
        self.actionParameters.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionHypnogram.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.actionSpectrogram.setText(QCoreApplication.translate("MainWindow", u"Spectrogram", None))
        self.actionMarkings.setText(QCoreApplication.translate("MainWindow", u"Markings", None))
        self.pushButton_control_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.pushButton_control_parameters.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.checkBox_control_coherence.setText(QCoreApplication.translate("MainWindow", u"Coherence", None))
        self.label_38.setText("")
        self.pushButton_control_compute.setText(QCoreApplication.translate("MainWindow", u"Compute", None))
        self.label_39.setText("")
        self.pushButton_control_hypnogram.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.pushButton_control_spectrogram.setText(QCoreApplication.translate("MainWindow", u"Spectrogram", None))
        self.pushButton_control_markings.setText(QCoreApplication.translate("MainWindow", u"Markings", None))
        self.pushButton_control_figures.setText(QCoreApplication.translate("MainWindow", u"Figures", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Description", None))
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Brief Description", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Output Suffix", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Signals", None))
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Reference Method", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Reference", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"Plotting", None))
        self.checkBox_plotting_xlabels.setText(QCoreApplication.translate("MainWindow", u"x labels", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.checkBox_settings_band.setText(QCoreApplication.translate("MainWindow", u"Band", None))
        self.label_35.setText("")
        self.checkBox_settings_notch.setText(QCoreApplication.translate("MainWindow", u"Notch", None))
        self.label_36.setText("")
        self.label_37.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Noise Detection (30s)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u0394 (0.6-4.6Hz)", None))
        self.label_5.setText("")
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Hz", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u0392 (40-60Hz)", None))
        self.label_26.setText("")
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Hz", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Multi-taper", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Spectral Epoch", None))
        self.label_31.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Window", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"s", None))
        self.label_32.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"s", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Multi-Processing", None))
        self.label_33.setText("")
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"# of CPUs", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Spectral Bands", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u03b4", None))
        self.label_41.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Hz", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u03b8", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Hz", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u03b1", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Hz", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u03c3", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Hz", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\u03b2", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Hz", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u03b3", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Hz", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Setting Reccomendations:", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Suggested Settings<br /><span style=\" font-size:10pt;\">Noise Detection </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Verdana','Helvetica Neue','Helvetica','Arial','sans-serif'; font-size:14px; color:#58566d; background-color:#e9e9fd;\">     \u0394</span><span style=\" font-size:"
                        "10pt;\"> = 2.0, </span><span style=\" font-family:'Verdana','Helvetica Neue','Helvetica','Arial','sans-serif'; font-size:14px; color:#58566d; background-color:#e9e9fd;\">\u0392</span><span style=\" font-size:10pt;\"> = 2.5</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Spectral Bands</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Verdana','Helvetica Neue','Helvetica','Arial','sans-serif'; font-size:10pt; color:#58566d; background-color:#e9e9fd;\">     \u03b4</span><span style=\" font-size:10pt;\"> :   0.5 -  4.0 Hz,      </span><span style=\" font-family:'Verdana','Helvetica Neue','Helvetica','Arial','sans-serif'; font-size:10pt; color:#58566d; background-color:#e9e9fd;\">\u03b8:   </span><span style=\" font-size:10pt;\">4.0 -    8.0 Hz,</span></p>\n"
"<p style=\" margin-top:"
                        "0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Verdana','Helvetica Neue','Helvetica','Arial','sans-serif'; font-size:10pt; color:#58566d; background-color:#e9e9fd;\">     \u03b1:   </span><span style=\" font-size:10pt;\">8.0 -12.0 Hz,      </span><span style=\" font-family:'Verdana','Helvetica Neue','Helvetica','Arial','sans-serif'; font-size:10pt; color:#58566d; background-color:#e9e9fd;\">\u03c3: </span><span style=\" font-size:10pt;\">12.0 - 15.0 Hz,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Verdana','Helvetica Neue','Helvetica','Arial','sans-serif'; font-size:10pt; color:#58566d; background-color:#e9e9fd;\">     \u03b2 </span><span style=\" font-size:10pt;\">15.0 - 30.0 Hz,      </span><span style=\" font-family:'Verdana','Helvetica Neue','Helvetica','Arial','sans-serif'; font-size:10pt; color:#58566d; backgr"
                        "ound-color:#e9e9fd;\">\u03b3: </span><span style=\" font-size:10pt;\">30.0 - 50.0 Hz</span></p></body></html>", None))
        self.label_34.setText("")
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.pushButton_hypnogram_show_stages.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.pushButton_hypnogram_legend.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.pushButton_spectrogram_show.setText(QCoreApplication.translate("MainWindow", u"Spect.", None))
        self.pushButton_spectrogram_legend.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.pushButton_spectrogram_heatmap_show.setText(QCoreApplication.translate("MainWindow", u"Heat", None))
        self.pushButton_sectrogram_heatmap_legend.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.label_results_1.setText("")
        self.label_results_2.setText("")
        self.label_results_3.setText("")
        self.label_results_4.setText("")
        self.label_results_5.setText("")
        self.label_results_6.setText("")
        self.label_results_7.setText("")
        self.label_results_8.setText("")
        self.label_results_9.setText("")
        self.label_results_10.setText("")
        self.label_results_time.setText("")
        self.menuShow.setTitle(QCoreApplication.translate("MainWindow", u"Show", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

