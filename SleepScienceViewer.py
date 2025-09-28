# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SleepScienceViewer.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QHBoxLayout,
    QLabel, QLayout, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1203, 1620)
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
        self.actionEDF_Signal_Export_2 = QAction(MainWindow)
        self.actionEDF_Signal_Export_2.setObjectName(u"actionEDF_Signal_Export_2")
        self.actionOpen_Signal_Window = QAction(MainWindow)
        self.actionOpen_Signal_Window.setObjectName(u"actionOpen_Signal_Window")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_master = QVBoxLayout()
        self.verticalLayout_master.setObjectName(u"verticalLayout_master")
        self.horizontalLayout_file_commands = QHBoxLayout()
        self.horizontalLayout_file_commands.setObjectName(u"horizontalLayout_file_commands")
        self.load_edf_textEdit = QTextEdit(self.centralwidget)
        self.load_edf_textEdit.setObjectName(u"load_edf_textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_edf_textEdit.sizePolicy().hasHeightForWidth())
        self.load_edf_textEdit.setSizePolicy(sizePolicy)
        self.load_edf_textEdit.setMinimumSize(QSize(0, 25))
        self.load_edf_textEdit.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_file_commands.addWidget(self.load_edf_textEdit)

        self.load_edf_pushButton = QPushButton(self.centralwidget)
        self.load_edf_pushButton.setObjectName(u"load_edf_pushButton")
        self.load_edf_pushButton.setMinimumSize(QSize(0, 25))
        self.load_edf_pushButton.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_file_commands.addWidget(self.load_edf_pushButton)

        self.horizontalSpacer = QSpacerItem(60, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_file_commands.addItem(self.horizontalSpacer)

        self.load_annotation_textEdit = QTextEdit(self.centralwidget)
        self.load_annotation_textEdit.setObjectName(u"load_annotation_textEdit")
        sizePolicy.setHeightForWidth(self.load_annotation_textEdit.sizePolicy().hasHeightForWidth())
        self.load_annotation_textEdit.setSizePolicy(sizePolicy)
        self.load_annotation_textEdit.setMinimumSize(QSize(30, 25))
        self.load_annotation_textEdit.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_file_commands.addWidget(self.load_annotation_textEdit)

        self.load_annotation_pushButton = QPushButton(self.centralwidget)
        self.load_annotation_pushButton.setObjectName(u"load_annotation_pushButton")
        self.load_annotation_pushButton.setMinimumSize(QSize(0, 25))
        self.load_annotation_pushButton.setMaximumSize(QSize(125, 25))

        self.horizontalLayout_file_commands.addWidget(self.load_annotation_pushButton)

        self.label_files_pacer = QLabel(self.centralwidget)
        self.label_files_pacer.setObjectName(u"label_files_pacer")
        self.label_files_pacer.setMinimumSize(QSize(40, 20))
        self.label_files_pacer.setMaximumSize(QSize(40, 20))

        self.horizontalLayout_file_commands.addWidget(self.label_files_pacer)

        self.pushButton_show_hypnogram = QPushButton(self.centralwidget)
        self.pushButton_show_hypnogram.setObjectName(u"pushButton_show_hypnogram")
        self.pushButton_show_hypnogram.setEnabled(True)
        self.pushButton_show_hypnogram.setMinimumSize(QSize(38, 25))
        self.pushButton_show_hypnogram.setMaximumSize(QSize(38, 25))
        self.pushButton_show_hypnogram.setCheckable(True)
        self.pushButton_show_hypnogram.setChecked(True)

        self.horizontalLayout_file_commands.addWidget(self.pushButton_show_hypnogram)

        self.pushButton_show_spectrogram = QPushButton(self.centralwidget)
        self.pushButton_show_spectrogram.setObjectName(u"pushButton_show_spectrogram")
        self.pushButton_show_spectrogram.setMinimumSize(QSize(38, 25))
        self.pushButton_show_spectrogram.setMaximumSize(QSize(38, 25))
        self.pushButton_show_spectrogram.setCheckable(True)
        self.pushButton_show_spectrogram.setChecked(True)

        self.horizontalLayout_file_commands.addWidget(self.pushButton_show_spectrogram)

        self.pushButton_show_annotation = QPushButton(self.centralwidget)
        self.pushButton_show_annotation.setObjectName(u"pushButton_show_annotation")
        self.pushButton_show_annotation.setMinimumSize(QSize(38, 25))
        self.pushButton_show_annotation.setMaximumSize(QSize(38, 16777215))
        self.pushButton_show_annotation.setCheckable(True)
        self.pushButton_show_annotation.setChecked(True)

        self.horizontalLayout_file_commands.addWidget(self.pushButton_show_annotation)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(40, 20))
        self.label_4.setMaximumSize(QSize(40, 20))

        self.horizontalLayout_file_commands.addWidget(self.label_4)

        self.spectrogram_comboBox = QComboBox(self.centralwidget)
        self.spectrogram_comboBox.setObjectName(u"spectrogram_comboBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spectrogram_comboBox.sizePolicy().hasHeightForWidth())
        self.spectrogram_comboBox.setSizePolicy(sizePolicy2)
        self.spectrogram_comboBox.setMinimumSize(QSize(95, 25))
        self.spectrogram_comboBox.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_file_commands.addWidget(self.spectrogram_comboBox)


        self.verticalLayout_master.addLayout(self.horizontalLayout_file_commands)

        self.horizontalLayout_hypnogram = QHBoxLayout()
        self.horizontalLayout_hypnogram.setObjectName(u"horizontalLayout_hypnogram")
        self.hypnogram_graphicsView = QGraphicsView(self.centralwidget)
        self.hypnogram_graphicsView.setObjectName(u"hypnogram_graphicsView")
        sizePolicy.setHeightForWidth(self.hypnogram_graphicsView.sizePolicy().hasHeightForWidth())
        self.hypnogram_graphicsView.setSizePolicy(sizePolicy)
        self.hypnogram_graphicsView.setMinimumSize(QSize(0, 90))
        self.hypnogram_graphicsView.setMaximumSize(QSize(16777215, 90))

        self.horizontalLayout_hypnogram.addWidget(self.hypnogram_graphicsView)

        self.verticalLayout_hypnogram_commands = QVBoxLayout()
        self.verticalLayout_hypnogram_commands.setSpacing(0)
        self.verticalLayout_hypnogram_commands.setObjectName(u"verticalLayout_hypnogram_commands")
        self.hypnogram_label = QLabel(self.centralwidget)
        self.hypnogram_label.setObjectName(u"hypnogram_label")
        sizePolicy2.setHeightForWidth(self.hypnogram_label.sizePolicy().hasHeightForWidth())
        self.hypnogram_label.setSizePolicy(sizePolicy2)
        self.hypnogram_label.setMinimumSize(QSize(0, 20))
        self.hypnogram_label.setMaximumSize(QSize(16777215, 20))
        self.hypnogram_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_hypnogram_commands.addWidget(self.hypnogram_label, 0, Qt.AlignTop)

        self.hypnogram_comboBox = QComboBox(self.centralwidget)
        self.hypnogram_comboBox.setObjectName(u"hypnogram_comboBox")
        self.hypnogram_comboBox.setMinimumSize(QSize(95, 25))
        self.hypnogram_comboBox.setMaximumSize(QSize(95, 25))

        self.verticalLayout_hypnogram_commands.addWidget(self.hypnogram_comboBox, 0, Qt.AlignTop)

        self.horizontalLayout_hypnogram_show = QHBoxLayout()
        self.horizontalLayout_hypnogram_show.setObjectName(u"horizontalLayout_hypnogram_show")
        self.pushButton_hyp_show_stages = QPushButton(self.centralwidget)
        self.pushButton_hyp_show_stages.setObjectName(u"pushButton_hyp_show_stages")
        self.pushButton_hyp_show_stages.setMinimumSize(QSize(62, 25))
        self.pushButton_hyp_show_stages.setMaximumSize(QSize(62, 25))
        self.pushButton_hyp_show_stages.setCheckable(True)
        self.pushButton_hyp_show_stages.setChecked(True)

        self.horizontalLayout_hypnogram_show.addWidget(self.pushButton_hyp_show_stages, 0, Qt.AlignTop)

        self.pushButton_hypnogram_legend = QPushButton(self.centralwidget)
        self.pushButton_hypnogram_legend.setObjectName(u"pushButton_hypnogram_legend")
        self.pushButton_hypnogram_legend.setMinimumSize(QSize(25, 25))
        self.pushButton_hypnogram_legend.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_hypnogram_show.addWidget(self.pushButton_hypnogram_legend, 0, Qt.AlignTop)


        self.verticalLayout_hypnogram_commands.addLayout(self.horizontalLayout_hypnogram_show)


        self.horizontalLayout_hypnogram.addLayout(self.verticalLayout_hypnogram_commands)


        self.verticalLayout_master.addLayout(self.horizontalLayout_hypnogram)

        self.horizontalLayout_spectrogram_text = QHBoxLayout()
        self.horizontalLayout_spectrogram_text.setObjectName(u"horizontalLayout_spectrogram_text")
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_spectrogram_text.addItem(self.horizontalSpacer_13)

        self.spectrogram_label = QLabel(self.centralwidget)
        self.spectrogram_label.setObjectName(u"spectrogram_label")
        sizePolicy2.setHeightForWidth(self.spectrogram_label.sizePolicy().hasHeightForWidth())
        self.spectrogram_label.setSizePolicy(sizePolicy2)
        self.spectrogram_label.setMinimumSize(QSize(0, 20))
        self.spectrogram_label.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_spectrogram_text.addWidget(self.spectrogram_label)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_spectrogram_text.addItem(self.horizontalSpacer_4)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(125, 20))
        self.label.setMaximumSize(QSize(125, 20))

        self.horizontalLayout_spectrogram_text.addWidget(self.label)


        self.verticalLayout_master.addLayout(self.horizontalLayout_spectrogram_text)

        self.horizontalLayout_spectrogram_plot = QHBoxLayout()
        self.horizontalLayout_spectrogram_plot.setObjectName(u"horizontalLayout_spectrogram_plot")
        self.horizontalLayout_spectrogram_plot.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.spectrogram_graphicsView = QGraphicsView(self.centralwidget)
        self.spectrogram_graphicsView.setObjectName(u"spectrogram_graphicsView")
        sizePolicy.setHeightForWidth(self.spectrogram_graphicsView.sizePolicy().hasHeightForWidth())
        self.spectrogram_graphicsView.setSizePolicy(sizePolicy)
        self.spectrogram_graphicsView.setMinimumSize(QSize(0, 60))
        self.spectrogram_graphicsView.setMaximumSize(QSize(16777215, 60))

        self.horizontalLayout_spectrogram_plot.addWidget(self.spectrogram_graphicsView)

        self.verticalLayout_spectrogram_command_container = QVBoxLayout()
        self.verticalLayout_spectrogram_command_container.setObjectName(u"verticalLayout_spectrogram_command_container")
        self.verticalLayout_spectrogram_commands = QVBoxLayout()
        self.verticalLayout_spectrogram_commands.setObjectName(u"verticalLayout_spectrogram_commands")
        self.horizontalLayout_spectrogram_command_2 = QHBoxLayout()
        self.horizontalLayout_spectrogram_command_2.setObjectName(u"horizontalLayout_spectrogram_command_2")
        self.compute_spectrogram_pushButton = QPushButton(self.centralwidget)
        self.compute_spectrogram_pushButton.setObjectName(u"compute_spectrogram_pushButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.compute_spectrogram_pushButton.sizePolicy().hasHeightForWidth())
        self.compute_spectrogram_pushButton.setSizePolicy(sizePolicy3)
        self.compute_spectrogram_pushButton.setMinimumSize(QSize(62, 25))
        self.compute_spectrogram_pushButton.setMaximumSize(QSize(62, 25))

        self.horizontalLayout_spectrogram_command_2.addWidget(self.compute_spectrogram_pushButton, 0, Qt.AlignTop)

        self.pushButton_spectrogra_legend = QPushButton(self.centralwidget)
        self.pushButton_spectrogra_legend.setObjectName(u"pushButton_spectrogra_legend")
        self.pushButton_spectrogra_legend.setMinimumSize(QSize(25, 25))
        self.pushButton_spectrogra_legend.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_spectrogram_command_2.addWidget(self.pushButton_spectrogra_legend)


        self.verticalLayout_spectrogram_commands.addLayout(self.horizontalLayout_spectrogram_command_2)


        self.verticalLayout_spectrogram_command_container.addLayout(self.verticalLayout_spectrogram_commands)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_spectrogram_heat = QPushButton(self.centralwidget)
        self.pushButton_spectrogram_heat.setObjectName(u"pushButton_spectrogram_heat")
        self.pushButton_spectrogram_heat.setMinimumSize(QSize(62, 0))
        self.pushButton_spectrogram_heat.setMaximumSize(QSize(62, 16777215))

        self.horizontalLayout_4.addWidget(self.pushButton_spectrogram_heat)

        self.pushButton_heat_legend = QPushButton(self.centralwidget)
        self.pushButton_heat_legend.setObjectName(u"pushButton_heat_legend")
        self.pushButton_heat_legend.setMinimumSize(QSize(25, 25))
        self.pushButton_heat_legend.setMaximumSize(QSize(25, 25))

        self.horizontalLayout_4.addWidget(self.pushButton_heat_legend)


        self.verticalLayout_spectrogram_command_container.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_spectrogram_plot.addLayout(self.verticalLayout_spectrogram_command_container)


        self.verticalLayout_master.addLayout(self.horizontalLayout_spectrogram_plot)

        self.horizontalLayout_annotation_plot = QHBoxLayout()
        self.horizontalLayout_annotation_plot.setObjectName(u"horizontalLayout_annotation_plot")
        self.graphicsView_annotation = QGraphicsView(self.centralwidget)
        self.graphicsView_annotation.setObjectName(u"graphicsView_annotation")
        sizePolicy.setHeightForWidth(self.graphicsView_annotation.sizePolicy().hasHeightForWidth())
        self.graphicsView_annotation.setSizePolicy(sizePolicy)
        self.graphicsView_annotation.setMinimumSize(QSize(0, 25))
        self.graphicsView_annotation.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_annotation_plot.addWidget(self.graphicsView_annotation)

        self.horizontalLayout_annotation_commands = QHBoxLayout()
        self.horizontalLayout_annotation_commands.setObjectName(u"horizontalLayout_annotation_commands")
        self.pushButton_legend = QPushButton(self.centralwidget)
        self.pushButton_legend.setObjectName(u"pushButton_legend")
        self.pushButton_legend.setMinimumSize(QSize(95, 25))
        self.pushButton_legend.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_annotation_commands.addWidget(self.pushButton_legend)


        self.horizontalLayout_annotation_plot.addLayout(self.horizontalLayout_annotation_commands)


        self.verticalLayout_master.addLayout(self.horizontalLayout_annotation_plot)

        self.horizontalLayout_signals = QHBoxLayout()
        self.horizontalLayout_signals.setObjectName(u"horizontalLayout_signals")
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
        self.first_pushButton.setMinimumSize(QSize(0, 25))
        self.first_pushButton.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_16.addWidget(self.first_pushButton)

        self.next_epoch_pushButton = QPushButton(self.centralwidget)
        self.next_epoch_pushButton.setObjectName(u"next_epoch_pushButton")
        self.next_epoch_pushButton.setMinimumSize(QSize(0, 25))
        self.next_epoch_pushButton.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_16.addWidget(self.next_epoch_pushButton)

        self.horizontalSpacer_9 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_9)

        self.update_epoch_pushButton = QPushButton(self.centralwidget)
        self.update_epoch_pushButton.setObjectName(u"update_epoch_pushButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.update_epoch_pushButton.sizePolicy().hasHeightForWidth())
        self.update_epoch_pushButton.setSizePolicy(sizePolicy4)
        self.update_epoch_pushButton.setMinimumSize(QSize(30, 25))
        self.update_epoch_pushButton.setMaximumSize(QSize(30, 25))

        self.horizontalLayout_16.addWidget(self.update_epoch_pushButton)

        self.epochs_textEdit = QTextEdit(self.centralwidget)
        self.epochs_textEdit.setObjectName(u"epochs_textEdit")
        sizePolicy.setHeightForWidth(self.epochs_textEdit.sizePolicy().hasHeightForWidth())
        self.epochs_textEdit.setSizePolicy(sizePolicy)
        self.epochs_textEdit.setMinimumSize(QSize(0, 25))
        self.epochs_textEdit.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_16.addWidget(self.epochs_textEdit)

        self.epochs_label = QLabel(self.centralwidget)
        self.epochs_label.setObjectName(u"epochs_label")
        sizePolicy2.setHeightForWidth(self.epochs_label.sizePolicy().hasHeightForWidth())
        self.epochs_label.setSizePolicy(sizePolicy2)
        self.epochs_label.setMinimumSize(QSize(0, 25))
        self.epochs_label.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_16.addWidget(self.epochs_label)

        self.horizontalSpacer_12 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_12)

        self.horizontalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_8)

        self.previous_pushButton = QPushButton(self.centralwidget)
        self.previous_pushButton.setObjectName(u"previous_pushButton")
        sizePolicy3.setHeightForWidth(self.previous_pushButton.sizePolicy().hasHeightForWidth())
        self.previous_pushButton.setSizePolicy(sizePolicy3)
        self.previous_pushButton.setMinimumSize(QSize(0, 25))
        self.previous_pushButton.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_16.addWidget(self.previous_pushButton)

        self.last_epoch_pushButton = QPushButton(self.centralwidget)
        self.last_epoch_pushButton.setObjectName(u"last_epoch_pushButton")
        sizePolicy3.setHeightForWidth(self.last_epoch_pushButton.sizePolicy().hasHeightForWidth())
        self.last_epoch_pushButton.setSizePolicy(sizePolicy3)
        self.last_epoch_pushButton.setMinimumSize(QSize(0, 25))
        self.last_epoch_pushButton.setMaximumSize(QSize(50, 25))

        self.horizontalLayout_16.addWidget(self.last_epoch_pushButton)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_6)

        self.epoch_comboBox = QComboBox(self.centralwidget)
        self.epoch_comboBox.setObjectName(u"epoch_comboBox")
        sizePolicy2.setHeightForWidth(self.epoch_comboBox.sizePolicy().hasHeightForWidth())
        self.epoch_comboBox.setSizePolicy(sizePolicy2)
        self.epoch_comboBox.setMinimumSize(QSize(100, 25))
        self.epoch_comboBox.setMaximumSize(QSize(100, 25))

        self.horizontalLayout_16.addWidget(self.epoch_comboBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.signal_1_comboBox = QComboBox(self.centralwidget)
        self.signal_1_comboBox.setObjectName(u"signal_1_comboBox")
        self.signal_1_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_1_comboBox.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setBold(False)
        self.signal_1_comboBox.setFont(font)

        self.verticalLayout_7.addWidget(self.signal_1_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig1_color = QComboBox(self.centralwidget)
        self.comboBox_sig1_color.setObjectName(u"comboBox_sig1_color")
        self.comboBox_sig1_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig1_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_7.addWidget(self.comboBox_sig1_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_15.addLayout(self.verticalLayout_7)

        self.signal_1_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_1_graphicsView.setObjectName(u"signal_1_graphicsView")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.signal_1_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_1_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_1_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_1_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_15.addWidget(self.signal_1_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.signal_2_comboBox = QComboBox(self.centralwidget)
        self.signal_2_comboBox.setObjectName(u"signal_2_comboBox")
        self.signal_2_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_2_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_2_comboBox.setFont(font)

        self.verticalLayout_8.addWidget(self.signal_2_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig2_color = QComboBox(self.centralwidget)
        self.comboBox_sig2_color.setObjectName(u"comboBox_sig2_color")
        self.comboBox_sig2_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig2_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_8.addWidget(self.comboBox_sig2_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_14.addLayout(self.verticalLayout_8)

        self.signal_2_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_2_graphicsView.setObjectName(u"signal_2_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_2_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_2_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_2_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_2_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_14.addWidget(self.signal_2_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.signal_3_comboBox = QComboBox(self.centralwidget)
        self.signal_3_comboBox.setObjectName(u"signal_3_comboBox")
        self.signal_3_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_3_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_3_comboBox.setFont(font)

        self.verticalLayout_9.addWidget(self.signal_3_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig3_color = QComboBox(self.centralwidget)
        self.comboBox_sig3_color.setObjectName(u"comboBox_sig3_color")
        self.comboBox_sig3_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig3_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_9.addWidget(self.comboBox_sig3_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_13.addLayout(self.verticalLayout_9)

        self.signal_3_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_3_graphicsView.setObjectName(u"signal_3_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_3_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_3_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_3_graphicsView.setMinimumSize(QSize(50, 50))
        self.signal_3_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_13.addWidget(self.signal_3_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.signal_4_comboBox = QComboBox(self.centralwidget)
        self.signal_4_comboBox.setObjectName(u"signal_4_comboBox")
        self.signal_4_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_4_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_4_comboBox.setFont(font)

        self.verticalLayout_10.addWidget(self.signal_4_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig4_color = QComboBox(self.centralwidget)
        self.comboBox_sig4_color.setObjectName(u"comboBox_sig4_color")
        self.comboBox_sig4_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig4_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_10.addWidget(self.comboBox_sig4_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_12.addLayout(self.verticalLayout_10)

        self.signal_4_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_4_graphicsView.setObjectName(u"signal_4_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_4_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_4_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_4_graphicsView.setMinimumSize(QSize(50, 50))
        self.signal_4_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_12.addWidget(self.signal_4_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.signal_5_comboBox = QComboBox(self.centralwidget)
        self.signal_5_comboBox.setObjectName(u"signal_5_comboBox")
        self.signal_5_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_5_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_5_comboBox.setFont(font)

        self.verticalLayout_11.addWidget(self.signal_5_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig5_color = QComboBox(self.centralwidget)
        self.comboBox_sig5_color.setObjectName(u"comboBox_sig5_color")
        self.comboBox_sig5_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig5_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_11.addWidget(self.comboBox_sig5_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_11.addLayout(self.verticalLayout_11)

        self.signal_5_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_5_graphicsView.setObjectName(u"signal_5_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_5_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_5_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_5_graphicsView.setMinimumSize(QSize(50, 50))
        self.signal_5_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_11.addWidget(self.signal_5_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.signal_6_comboBox = QComboBox(self.centralwidget)
        self.signal_6_comboBox.setObjectName(u"signal_6_comboBox")
        self.signal_6_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_6_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_6_comboBox.setFont(font)

        self.verticalLayout_12.addWidget(self.signal_6_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig6_color = QComboBox(self.centralwidget)
        self.comboBox_sig6_color.setObjectName(u"comboBox_sig6_color")
        self.comboBox_sig6_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig6_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_12.addWidget(self.comboBox_sig6_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_10.addLayout(self.verticalLayout_12)

        self.signal_6_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_6_graphicsView.setObjectName(u"signal_6_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_6_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_6_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_6_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_6_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_10.addWidget(self.signal_6_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.signal_7_comboBox = QComboBox(self.centralwidget)
        self.signal_7_comboBox.setObjectName(u"signal_7_comboBox")
        self.signal_7_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_7_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_7_comboBox.setFont(font)

        self.verticalLayout_13.addWidget(self.signal_7_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig7_color = QComboBox(self.centralwidget)
        self.comboBox_sig7_color.setObjectName(u"comboBox_sig7_color")
        self.comboBox_sig7_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig7_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_13.addWidget(self.comboBox_sig7_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_9.addLayout(self.verticalLayout_13)

        self.signal_7_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_7_graphicsView.setObjectName(u"signal_7_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_7_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_7_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_7_graphicsView.setMinimumSize(QSize(50, 50))
        self.signal_7_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_9.addWidget(self.signal_7_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.signal_8_comboBox = QComboBox(self.centralwidget)
        self.signal_8_comboBox.setObjectName(u"signal_8_comboBox")
        self.signal_8_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_8_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_8_comboBox.setFont(font)

        self.verticalLayout_14.addWidget(self.signal_8_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig8_color = QComboBox(self.centralwidget)
        self.comboBox_sig8_color.setObjectName(u"comboBox_sig8_color")
        self.comboBox_sig8_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig8_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_14.addWidget(self.comboBox_sig8_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_8.addLayout(self.verticalLayout_14)

        self.signal_8_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_8_graphicsView.setObjectName(u"signal_8_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_8_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_8_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_8_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_8_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_8.addWidget(self.signal_8_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.signal_9_comboBox = QComboBox(self.centralwidget)
        self.signal_9_comboBox.setObjectName(u"signal_9_comboBox")
        self.signal_9_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_9_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_9_comboBox.setFont(font)

        self.verticalLayout_15.addWidget(self.signal_9_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig9_color = QComboBox(self.centralwidget)
        self.comboBox_sig9_color.setObjectName(u"comboBox_sig9_color")
        self.comboBox_sig9_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig9_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_15.addWidget(self.comboBox_sig9_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_7.addLayout(self.verticalLayout_15)

        self.signal_9_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_9_graphicsView.setObjectName(u"signal_9_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_9_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_9_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_9_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_9_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_7.addWidget(self.signal_9_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.signal_10_comboBox = QComboBox(self.centralwidget)
        self.signal_10_comboBox.setObjectName(u"signal_10_comboBox")
        self.signal_10_comboBox.setMinimumSize(QSize(100, 0))
        self.signal_10_comboBox.setMaximumSize(QSize(100, 16777215))
        self.signal_10_comboBox.setFont(font)

        self.verticalLayout_16.addWidget(self.signal_10_comboBox, 0, Qt.AlignTop)

        self.comboBox_sig10_color = QComboBox(self.centralwidget)
        self.comboBox_sig10_color.setObjectName(u"comboBox_sig10_color")
        self.comboBox_sig10_color.setMinimumSize(QSize(40, 0))
        self.comboBox_sig10_color.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout_16.addWidget(self.comboBox_sig10_color, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_5.addLayout(self.verticalLayout_16)

        self.signal_10_graphicsView = QGraphicsView(self.centralwidget)
        self.signal_10_graphicsView.setObjectName(u"signal_10_graphicsView")
        sizePolicy5.setHeightForWidth(self.signal_10_graphicsView.sizePolicy().hasHeightForWidth())
        self.signal_10_graphicsView.setSizePolicy(sizePolicy5)
        self.signal_10_graphicsView.setMinimumSize(QSize(0, 50))
        self.signal_10_graphicsView.setMaximumSize(QSize(16777215, 200))

        self.horizontalLayout_5.addWidget(self.signal_10_graphicsView)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_signals.addLayout(self.verticalLayout_3)

        self.verticalLayout_Annotation_List_Widget = QVBoxLayout()
        self.verticalLayout_Annotation_List_Widget.setObjectName(u"verticalLayout_Annotation_List_Widget")
        self.verticalLayout_Annotation_List_Widget.setSizeConstraint(QLayout.SetMinimumSize)
        self.annotation_comboBox = QComboBox(self.centralwidget)
        self.annotation_comboBox.setObjectName(u"annotation_comboBox")
        self.annotation_comboBox.setMinimumSize(QSize(300, 25))
        self.annotation_comboBox.setMaximumSize(QSize(300, 25))

        self.verticalLayout_Annotation_List_Widget.addWidget(self.annotation_comboBox)

        self.annotation_listWidget = QListWidget(self.centralwidget)
        self.annotation_listWidget.setObjectName(u"annotation_listWidget")
        self.annotation_listWidget.setMaximumSize(QSize(300, 16777215))

        self.verticalLayout_Annotation_List_Widget.addWidget(self.annotation_listWidget)


        self.horizontalLayout_signals.addLayout(self.verticalLayout_Annotation_List_Widget)


        self.verticalLayout_master.addLayout(self.horizontalLayout_signals)


        self.horizontalLayout.addLayout(self.verticalLayout_master)

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
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuGenerate.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_Edf)
        self.menuFile.addAction(self.actionOpen_XML)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuGenerate.addAction(self.actionEDF_Summary)
        self.menuGenerate.addAction(self.actionEDF_Signal_Export_2)
        self.menuGenerate.addSeparator()
        self.menuGenerate.addAction(self.actionAnnotation_Summary)
        self.menuGenerate.addAction(self.actionAnnotation_Export)
        self.menuGenerate.addAction(self.actionSleep_Stages_Export)
        self.menuHelp.addAction(self.actionEDF_Standard)
        self.menuHelp.addAction(self.actionAnnotation_Standard)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuWindow.addAction(self.actionOpen_Signal_Window)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sleep Science Viewer", None))
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
        self.actionEDF_Signal_Export_2.setText(QCoreApplication.translate("MainWindow", u"EDF Signal Export", None))
        self.actionOpen_Signal_Window.setText(QCoreApplication.translate("MainWindow", u"Open Signal Window", None))
        self.load_edf_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load EDF", None))
        self.load_annotation_pushButton.setText(QCoreApplication.translate("MainWindow", u"Load Annot.", None))
        self.label_files_pacer.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_show_hypnogram.setToolTip(QCoreApplication.translate("MainWindow", u"Show Hypnogram Plot", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_hypnogram.setText(QCoreApplication.translate("MainWindow", u"Hyp", None))
#if QT_CONFIG(tooltip)
        self.pushButton_show_spectrogram.setToolTip(QCoreApplication.translate("MainWindow", u"Show Spectrogram Plot", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_spectrogram.setText(QCoreApplication.translate("MainWindow", u"Spc", None))
#if QT_CONFIG(tooltip)
        self.pushButton_show_annotation.setToolTip(QCoreApplication.translate("MainWindow", u"Show Annotation Plot", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_annotation.setText(QCoreApplication.translate("MainWindow", u"Ann", None))
        self.label_4.setText("")
        self.hypnogram_label.setText(QCoreApplication.translate("MainWindow", u"Hypnogram", None))
        self.pushButton_hyp_show_stages.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.pushButton_hypnogram_legend.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.spectrogram_label.setText(QCoreApplication.translate("MainWindow", u"Multi-Taper Spectrogram", None))
        self.label.setText("")
        self.compute_spectrogram_pushButton.setText(QCoreApplication.translate("MainWindow", u"Spect.", None))
        self.pushButton_spectrogra_legend.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.pushButton_spectrogram_heat.setText(QCoreApplication.translate("MainWindow", u"Heat", None))
        self.pushButton_heat_legend.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.pushButton_legend.setText(QCoreApplication.translate("MainWindow", u"Legend", None))
        self.first_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u2759\u25c0", None))
        self.next_epoch_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
        self.update_epoch_pushButton.setText(QCoreApplication.translate("MainWindow", u"U", None))
        self.epochs_label.setText(QCoreApplication.translate("MainWindow", u"/max_epochs", None))
        self.previous_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u25c0", None))
        self.last_epoch_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u25b6\u2759", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuGenerate.setTitle(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Window", None))
    # retranslateUi

