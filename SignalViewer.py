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
        SignalWindow.resize(1282, 1000)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SignalWindow.sizePolicy().hasHeightForWidth())
        SignalWindow.setSizePolicy(sizePolicy)
        SignalWindow.setMinimumSize(QSize(20, 20))
        self.centralwidget = QWidget(SignalWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_upper_hypnogram = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_upper_hypnogram)

        self.horizontalLayout_controls = QHBoxLayout()
        self.horizontalLayout_controls.setObjectName(u"horizontalLayout_controls")
        self.horizontalLayout_controls.setSizeConstraint(QLayout.SetMinimumSize)
        self.pushButton_sync_y = QPushButton(self.centralwidget)
        self.pushButton_sync_y.setObjectName(u"pushButton_sync_y")
        self.pushButton_sync_y.setMinimumSize(QSize(70, 25))
        self.pushButton_sync_y.setMaximumSize(QSize(70, 40))
        self.pushButton_sync_y.setCheckable(True)

        self.horizontalLayout_controls.addWidget(self.pushButton_sync_y)

        self.horizontalSpacer_46 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_46)

        self.comboBox_filter_low = QComboBox(self.centralwidget)
        self.comboBox_filter_low.setObjectName(u"comboBox_filter_low")
        self.comboBox_filter_low.setMinimumSize(QSize(75, 25))
        self.comboBox_filter_low.setMaximumSize(QSize(75, 25))
        self.comboBox_filter_low.setMaxVisibleItems(18)

        self.horizontalLayout_controls.addWidget(self.comboBox_filter_low)

        self.comboBox_filter_high = QComboBox(self.centralwidget)
        self.comboBox_filter_high.setObjectName(u"comboBox_filter_high")
        self.comboBox_filter_high.setMinimumSize(QSize(75, 25))
        self.comboBox_filter_high.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_controls.addWidget(self.comboBox_filter_high)

        self.pushButton_filter = QPushButton(self.centralwidget)
        self.pushButton_filter.setObjectName(u"pushButton_filter")
        self.pushButton_filter.setMinimumSize(QSize(60, 25))
        self.pushButton_filter.setMaximumSize(QSize(60, 25))
        self.pushButton_filter.setCheckable(True)

        self.horizontalLayout_controls.addWidget(self.pushButton_filter)

        self.horizontalSpacer_45 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_45)

        self.comboBox_filter_notch = QComboBox(self.centralwidget)
        self.comboBox_filter_notch.setObjectName(u"comboBox_filter_notch")
        self.comboBox_filter_notch.setMinimumSize(QSize(75, 25))
        self.comboBox_filter_notch.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_controls.addWidget(self.comboBox_filter_notch)

        self.pushButton_notch = QPushButton(self.centralwidget)
        self.pushButton_notch.setObjectName(u"pushButton_notch")
        self.pushButton_notch.setMinimumSize(QSize(100, 25))
        self.pushButton_notch.setMaximumSize(QSize(100, 25))
        self.pushButton_notch.setCheckable(True)

        self.horizontalLayout_controls.addWidget(self.pushButton_notch)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_5)

        self.pushButton_save = QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setEnabled(False)
        self.pushButton_save.setMinimumSize(QSize(75, 25))
        self.pushButton_save.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_controls.addWidget(self.pushButton_save)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_4)

        self.pushButton_load = QPushButton(self.centralwidget)
        self.pushButton_load.setObjectName(u"pushButton_load")
        self.pushButton_load.setEnabled(False)
        self.pushButton_load.setMinimumSize(QSize(75, 25))
        self.pushButton_load.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_controls.addWidget(self.pushButton_load)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_3)

        self.pushButton_mark = QPushButton(self.centralwidget)
        self.pushButton_mark.setObjectName(u"pushButton_mark")
        self.pushButton_mark.setEnabled(False)
        self.pushButton_mark.setCheckable(True)

        self.horizontalLayout_controls.addWidget(self.pushButton_mark)

        self.horizontalSpacer_48 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_48)

        self.pushButton_show_hypnogram = QPushButton(self.centralwidget)
        self.pushButton_show_hypnogram.setObjectName(u"pushButton_show_hypnogram")
        self.pushButton_show_hypnogram.setMinimumSize(QSize(35, 0))
        self.pushButton_show_hypnogram.setMaximumSize(QSize(35, 16777215))
        self.pushButton_show_hypnogram.setCheckable(True)
        self.pushButton_show_hypnogram.setChecked(True)

        self.horizontalLayout_controls.addWidget(self.pushButton_show_hypnogram)

        self.pushButton_show_spectrogram_plot = QPushButton(self.centralwidget)
        self.pushButton_show_spectrogram_plot.setObjectName(u"pushButton_show_spectrogram_plot")
        self.pushButton_show_spectrogram_plot.setMinimumSize(QSize(35, 0))
        self.pushButton_show_spectrogram_plot.setMaximumSize(QSize(35, 16777215))
        self.pushButton_show_spectrogram_plot.setCheckable(True)
        self.pushButton_show_spectrogram_plot.setChecked(True)

        self.horizontalLayout_controls.addWidget(self.pushButton_show_spectrogram_plot)

        self.pushButton_show_annotation_panel = QPushButton(self.centralwidget)
        self.pushButton_show_annotation_panel.setObjectName(u"pushButton_show_annotation_panel")
        self.pushButton_show_annotation_panel.setMinimumSize(QSize(35, 0))
        self.pushButton_show_annotation_panel.setMaximumSize(QSize(35, 16777215))
        self.pushButton_show_annotation_panel.setCheckable(True)
        self.pushButton_show_annotation_panel.setChecked(True)

        self.horizontalLayout_controls.addWidget(self.pushButton_show_annotation_panel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_controls.addItem(self.horizontalSpacer_2)

        self.comboBox_signals = QComboBox(self.centralwidget)
        self.comboBox_signals.setObjectName(u"comboBox_signals")
        self.comboBox_signals.setMinimumSize(QSize(95, 25))
        self.comboBox_signals.setMaximumSize(QSize(95, 25))

        self.horizontalLayout_controls.addWidget(self.comboBox_signals)


        self.verticalLayout.addLayout(self.horizontalLayout_controls)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_hypnogram = QHBoxLayout()
        self.horizontalLayout_hypnogram.setObjectName(u"horizontalLayout_hypnogram")
        self.graphicsView_hypnogram = QGraphicsView(self.centralwidget)
        self.graphicsView_hypnogram.setObjectName(u"graphicsView_hypnogram")
        self.graphicsView_hypnogram.setMinimumSize(QSize(0, 90))
        self.graphicsView_hypnogram.setMaximumSize(QSize(16777215, 90))

        self.horizontalLayout_hypnogram.addWidget(self.graphicsView_hypnogram, 0, Qt.AlignTop)

        self.verticalLayout_hypnogram_commands = QVBoxLayout()
        self.verticalLayout_hypnogram_commands.setObjectName(u"verticalLayout_hypnogram_commands")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 25))
        self.label_3.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_hypnogram_commands.addWidget(self.label_3, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.comboBox_hypnogram = QComboBox(self.centralwidget)
        self.comboBox_hypnogram.setObjectName(u"comboBox_hypnogram")
        self.comboBox_hypnogram.setMinimumSize(QSize(95, 0))
        self.comboBox_hypnogram.setMaximumSize(QSize(95, 16777215))

        self.verticalLayout_hypnogram_commands.addWidget(self.comboBox_hypnogram, 0, Qt.AlignTop)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_show_hypnogram_stages_in_color = QPushButton(self.centralwidget)
        self.pushButton_show_hypnogram_stages_in_color.setObjectName(u"pushButton_show_hypnogram_stages_in_color")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(20)
        sizePolicy1.setHeightForWidth(self.pushButton_show_hypnogram_stages_in_color.sizePolicy().hasHeightForWidth())
        self.pushButton_show_hypnogram_stages_in_color.setSizePolicy(sizePolicy1)
        self.pushButton_show_hypnogram_stages_in_color.setMinimumSize(QSize(62, 20))
        self.pushButton_show_hypnogram_stages_in_color.setMaximumSize(QSize(62, 25))
        self.pushButton_show_hypnogram_stages_in_color.setCheckable(True)
        self.pushButton_show_hypnogram_stages_in_color.setChecked(True)

        self.horizontalLayout_3.addWidget(self.pushButton_show_hypnogram_stages_in_color)

        self.pushButton_hypnogram_legend = QPushButton(self.centralwidget)
        self.pushButton_hypnogram_legend.setObjectName(u"pushButton_hypnogram_legend")
        self.pushButton_hypnogram_legend.setMinimumSize(QSize(25, 0))
        self.pushButton_hypnogram_legend.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_3.addWidget(self.pushButton_hypnogram_legend, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_hypnogram_commands.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_hypnogram.addLayout(self.verticalLayout_hypnogram_commands)


        self.verticalLayout.addLayout(self.horizontalLayout_hypnogram)

        self.horizontalLayout_spectrogram_label = QHBoxLayout()
        self.horizontalLayout_spectrogram_label.setObjectName(u"horizontalLayout_spectrogram_label")
        self.label_mt_spacer_3 = QLabel(self.centralwidget)
        self.label_mt_spacer_3.setObjectName(u"label_mt_spacer_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_mt_spacer_3.sizePolicy().hasHeightForWidth())
        self.label_mt_spacer_3.setSizePolicy(sizePolicy2)

        self.horizontalLayout_spectrogram_label.addWidget(self.label_mt_spacer_3)

        self.label_spectrogram = QLabel(self.centralwidget)
        self.label_spectrogram.setObjectName(u"label_spectrogram")

        self.horizontalLayout_spectrogram_label.addWidget(self.label_spectrogram, 0, Qt.AlignHCenter)

        self.label_mt_spacer_2 = QLabel(self.centralwidget)
        self.label_mt_spacer_2.setObjectName(u"label_mt_spacer_2")
        sizePolicy2.setHeightForWidth(self.label_mt_spacer_2.sizePolicy().hasHeightForWidth())
        self.label_mt_spacer_2.setSizePolicy(sizePolicy2)

        self.horizontalLayout_spectrogram_label.addWidget(self.label_mt_spacer_2)

        self.label_mt_spacer = QLabel(self.centralwidget)
        self.label_mt_spacer.setObjectName(u"label_mt_spacer")
        self.label_mt_spacer.setMinimumSize(QSize(95, 0))
        self.label_mt_spacer.setMaximumSize(QSize(95, 16777215))

        self.horizontalLayout_spectrogram_label.addWidget(self.label_mt_spacer)


        self.verticalLayout.addLayout(self.horizontalLayout_spectrogram_label)

        self.horizontalLayout_spectrogam = QHBoxLayout()
        self.horizontalLayout_spectrogam.setObjectName(u"horizontalLayout_spectrogam")
        self.graphicsView_spectrogram = QGraphicsView(self.centralwidget)
        self.graphicsView_spectrogram.setObjectName(u"graphicsView_spectrogram")
        self.graphicsView_spectrogram.setMinimumSize(QSize(0, 60))
        self.graphicsView_spectrogram.setMaximumSize(QSize(16777215, 60))

        self.horizontalLayout_spectrogam.addWidget(self.graphicsView_spectrogram)

        self.verticalLayout_spectrogram_commands = QVBoxLayout()
        self.verticalLayout_spectrogram_commands.setObjectName(u"verticalLayout_spectrogram_commands")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_show_spectrogram = QPushButton(self.centralwidget)
        self.pushButton_show_spectrogram.setObjectName(u"pushButton_show_spectrogram")
        self.pushButton_show_spectrogram.setMinimumSize(QSize(62, 0))
        self.pushButton_show_spectrogram.setMaximumSize(QSize(62, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButton_show_spectrogram)

        self.pushButton_spectrogram_legend = QPushButton(self.centralwidget)
        self.pushButton_spectrogram_legend.setObjectName(u"pushButton_spectrogram_legend")
        self.pushButton_spectrogram_legend.setMinimumSize(QSize(25, 0))
        self.pushButton_spectrogram_legend.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButton_spectrogram_legend)


        self.verticalLayout_spectrogram_commands.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_heatmap = QPushButton(self.centralwidget)
        self.pushButton_heatmap.setObjectName(u"pushButton_heatmap")
        self.pushButton_heatmap.setMinimumSize(QSize(62, 0))
        self.pushButton_heatmap.setMaximumSize(QSize(62, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_heatmap)

        self.pushButton_heat_legend = QPushButton(self.centralwidget)
        self.pushButton_heat_legend.setObjectName(u"pushButton_heat_legend")
        self.pushButton_heat_legend.setMinimumSize(QSize(25, 0))
        self.pushButton_heat_legend.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout.addWidget(self.pushButton_heat_legend)


        self.verticalLayout_spectrogram_commands.addLayout(self.horizontalLayout)


        self.horizontalLayout_spectrogam.addLayout(self.verticalLayout_spectrogram_commands)


        self.verticalLayout.addLayout(self.horizontalLayout_spectrogam)

        self.horizontalLayout_annotation_plot = QHBoxLayout()
        self.horizontalLayout_annotation_plot.setObjectName(u"horizontalLayout_annotation_plot")
        self.graphicsView_annotation_plot = QGraphicsView(self.centralwidget)
        self.graphicsView_annotation_plot.setObjectName(u"graphicsView_annotation_plot")
        self.graphicsView_annotation_plot.setMinimumSize(QSize(0, 25))
        self.graphicsView_annotation_plot.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_annotation_plot.addWidget(self.graphicsView_annotation_plot)

        self.pushButton_annotation_legend = QPushButton(self.centralwidget)
        self.pushButton_annotation_legend.setObjectName(u"pushButton_annotation_legend")
        self.pushButton_annotation_legend.setMinimumSize(QSize(95, 0))
        self.pushButton_annotation_legend.setMaximumSize(QSize(95, 16777215))

        self.horizontalLayout_annotation_plot.addWidget(self.pushButton_annotation_legend)


        self.verticalLayout.addLayout(self.horizontalLayout_annotation_plot)

        self.verticalSpacer_lower_hypnogram = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_lower_hypnogram)

        self.horizontalLayout_data = QHBoxLayout()
        self.horizontalLayout_data.setObjectName(u"horizontalLayout_data")
        self.horizontalLayout_data.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout_signals = QVBoxLayout()
        self.verticalLayout_signals.setSpacing(0)
        self.verticalLayout_signals.setObjectName(u"verticalLayout_signals")
        self.verticalLayout_signals.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout_signal_controls = QHBoxLayout()
        self.horizontalLayout_signal_controls.setSpacing(0)
        self.horizontalLayout_signal_controls.setObjectName(u"horizontalLayout_signal_controls")
        self.horizontalLayout_signal_controls.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_8 = QSpacerItem(6, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer_8)

        self.label_epoch_numbers = QLabel(self.centralwidget)
        self.label_epoch_numbers.setObjectName(u"label_epoch_numbers")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_epoch_numbers.sizePolicy().hasHeightForWidth())
        self.label_epoch_numbers.setSizePolicy(sizePolicy3)
        self.label_epoch_numbers.setMinimumSize(QSize(40, 12))
        self.label_epoch_numbers.setMaximumSize(QSize(40, 12))
        font = QFont()
        font.setPointSize(9)
        self.label_epoch_numbers.setFont(font)
        self.label_epoch_numbers.setAlignment(Qt.AlignBottom|Qt.AlignRight|Qt.AlignTrailing)

        self.horizontalLayout_signal_controls.addWidget(self.label_epoch_numbers)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)
        self.label.setMinimumSize(QSize(10, 20))
        self.label.setMaximumSize(QSize(10, 20))

        self.horizontalLayout_signal_controls.addWidget(self.label)

        self.horizontalSpacer_47 = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer_47)

        self.pushButton_epoch_show_stages = QPushButton(self.centralwidget)
        self.pushButton_epoch_show_stages.setObjectName(u"pushButton_epoch_show_stages")
        self.pushButton_epoch_show_stages.setMinimumSize(QSize(62, 25))
        self.pushButton_epoch_show_stages.setMaximumSize(QSize(62, 25))
        self.pushButton_epoch_show_stages.setCheckable(True)
        self.pushButton_epoch_show_stages.setChecked(True)

        self.horizontalLayout_signal_controls.addWidget(self.pushButton_epoch_show_stages)

        self.horizontalSpacer_26 = QSpacerItem(100, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer_26)

        self.horizontalSpacer_27 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer_27)

        self.pushButton_first = QPushButton(self.centralwidget)
        self.pushButton_first.setObjectName(u"pushButton_first")
        self.pushButton_first.setMinimumSize(QSize(0, 25))
        self.pushButton_first.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_signal_controls.addWidget(self.pushButton_first, 0, Qt.AlignTop)

        self.pushButton_next = QPushButton(self.centralwidget)
        self.pushButton_next.setObjectName(u"pushButton_next")
        self.pushButton_next.setMinimumSize(QSize(0, 25))

        self.horizontalLayout_signal_controls.addWidget(self.pushButton_next, 0, Qt.AlignTop)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer_6)

        self.pushButton_update = QPushButton(self.centralwidget)
        self.pushButton_update.setObjectName(u"pushButton_update")
        self.pushButton_update.setMinimumSize(QSize(40, 25))
        self.pushButton_update.setMaximumSize(QSize(40, 25))

        self.horizontalLayout_signal_controls.addWidget(self.pushButton_update, 0, Qt.AlignTop)

        self.textEdit_epoch = QTextEdit(self.centralwidget)
        self.textEdit_epoch.setObjectName(u"textEdit_epoch")
        self.textEdit_epoch.setMinimumSize(QSize(75, 25))
        self.textEdit_epoch.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_signal_controls.addWidget(self.textEdit_epoch, 0, Qt.AlignTop)

        self.horizontalSpacer_23 = QSpacerItem(6, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer_23)

        self.label_page = QLabel(self.centralwidget)
        self.label_page.setObjectName(u"label_page")
        self.label_page.setMinimumSize(QSize(0, 25))
        self.label_page.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_signal_controls.addWidget(self.label_page, 0, Qt.AlignTop)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer)

        self.horizontalSpacer_7 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer_7)

        self.pushButton_previous = QPushButton(self.centralwidget)
        self.pushButton_previous.setObjectName(u"pushButton_previous")
        self.pushButton_previous.setMinimumSize(QSize(0, 25))
        self.pushButton_previous.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_signal_controls.addWidget(self.pushButton_previous, 0, Qt.AlignTop)

        self.pushButton_last = QPushButton(self.centralwidget)
        self.pushButton_last.setObjectName(u"pushButton_last")
        self.pushButton_last.setMinimumSize(QSize(0, 25))
        self.pushButton_last.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_signal_controls.addWidget(self.pushButton_last, 0, Qt.AlignTop)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_controls.addItem(self.horizontalSpacer_25)

        self.comboBox_epoch = QComboBox(self.centralwidget)
        self.comboBox_epoch.setObjectName(u"comboBox_epoch")
        self.comboBox_epoch.setMinimumSize(QSize(75, 25))
        self.comboBox_epoch.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_signal_controls.addWidget(self.comboBox_epoch, 0, Qt.AlignTop)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_controls)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.horizontalLayout_6.addItem(self.verticalSpacer_2)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_signal_1 = QHBoxLayout()
        self.horizontalLayout_signal_1.setSpacing(0)
        self.horizontalLayout_signal_1.setObjectName(u"horizontalLayout_signal_1")
        self.horizontalLayout_signal_1.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_9 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_1.addItem(self.horizontalSpacer_9)

        self.label_signal_1 = QLabel(self.centralwidget)
        self.label_signal_1.setObjectName(u"label_signal_1")
        self.label_signal_1.setMinimumSize(QSize(40, 12))
        self.label_signal_1.setMaximumSize(QSize(40, 12))
        self.label_signal_1.setFont(font)
        self.label_signal_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_1.addWidget(self.label_signal_1)

        self.horizontalSpacer_29 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_1.addItem(self.horizontalSpacer_29)

        self.graphicsView_signal_1 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_1.setObjectName(u"graphicsView_signal_1")
        self.graphicsView_signal_1.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_1.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_1.addWidget(self.graphicsView_signal_1)

        self.comboBox_mark_1 = QComboBox(self.centralwidget)
        self.comboBox_mark_1.setObjectName(u"comboBox_mark_1")
        self.comboBox_mark_1.setEnabled(True)
        self.comboBox_mark_1.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_1.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_1.addWidget(self.comboBox_mark_1)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_1)

        self.horizontalLayout_signal_2 = QHBoxLayout()
        self.horizontalLayout_signal_2.setSpacing(0)
        self.horizontalLayout_signal_2.setObjectName(u"horizontalLayout_signal_2")
        self.horizontalLayout_signal_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_24 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_2.addItem(self.horizontalSpacer_24)

        self.label_signal_2 = QLabel(self.centralwidget)
        self.label_signal_2.setObjectName(u"label_signal_2")
        self.label_signal_2.setMinimumSize(QSize(40, 12))
        self.label_signal_2.setMaximumSize(QSize(40, 12))
        self.label_signal_2.setFont(font)
        self.label_signal_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_2.addWidget(self.label_signal_2)

        self.horizontalSpacer_30 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_2.addItem(self.horizontalSpacer_30)

        self.graphicsView_signal_2 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_2.setObjectName(u"graphicsView_signal_2")
        self.graphicsView_signal_2.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_2.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_2.addWidget(self.graphicsView_signal_2)

        self.comboBox_mark_2 = QComboBox(self.centralwidget)
        self.comboBox_mark_2.setObjectName(u"comboBox_mark_2")
        self.comboBox_mark_2.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_2.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_signal_2.addWidget(self.comboBox_mark_2)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_2)

        self.horizontalLayout_signal_3 = QHBoxLayout()
        self.horizontalLayout_signal_3.setSpacing(0)
        self.horizontalLayout_signal_3.setObjectName(u"horizontalLayout_signal_3")
        self.horizontalLayout_signal_3.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_22 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_3.addItem(self.horizontalSpacer_22)

        self.label_signal_3 = QLabel(self.centralwidget)
        self.label_signal_3.setObjectName(u"label_signal_3")
        self.label_signal_3.setMinimumSize(QSize(40, 12))
        self.label_signal_3.setMaximumSize(QSize(40, 12))
        self.label_signal_3.setFont(font)
        self.label_signal_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_3.addWidget(self.label_signal_3)

        self.horizontalSpacer_31 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_3.addItem(self.horizontalSpacer_31)

        self.graphicsView_signal_3 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_3.setObjectName(u"graphicsView_signal_3")
        self.graphicsView_signal_3.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_3.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_3.addWidget(self.graphicsView_signal_3)

        self.comboBox_mark_3 = QComboBox(self.centralwidget)
        self.comboBox_mark_3.setObjectName(u"comboBox_mark_3")
        self.comboBox_mark_3.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_3.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_3.addWidget(self.comboBox_mark_3)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_3)

        self.horizontalLayout_signal_4 = QHBoxLayout()
        self.horizontalLayout_signal_4.setSpacing(0)
        self.horizontalLayout_signal_4.setObjectName(u"horizontalLayout_signal_4")
        self.horizontalLayout_signal_4.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_10 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_4.addItem(self.horizontalSpacer_10)

        self.label_signal_4 = QLabel(self.centralwidget)
        self.label_signal_4.setObjectName(u"label_signal_4")
        self.label_signal_4.setMinimumSize(QSize(40, 12))
        self.label_signal_4.setMaximumSize(QSize(40, 12))
        self.label_signal_4.setFont(font)
        self.label_signal_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_4.addWidget(self.label_signal_4)

        self.horizontalSpacer_32 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_4.addItem(self.horizontalSpacer_32)

        self.graphicsView_signal_4 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_4.setObjectName(u"graphicsView_signal_4")
        self.graphicsView_signal_4.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_4.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_4.addWidget(self.graphicsView_signal_4)

        self.comboBox_mark_4 = QComboBox(self.centralwidget)
        self.comboBox_mark_4.setObjectName(u"comboBox_mark_4")
        self.comboBox_mark_4.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_4.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_4.addWidget(self.comboBox_mark_4)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_4)

        self.horizontalLayout_signal_5 = QHBoxLayout()
        self.horizontalLayout_signal_5.setSpacing(0)
        self.horizontalLayout_signal_5.setObjectName(u"horizontalLayout_signal_5")
        self.horizontalLayout_signal_5.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_28 = QSpacerItem(6, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_5.addItem(self.horizontalSpacer_28)

        self.label_signal_5 = QLabel(self.centralwidget)
        self.label_signal_5.setObjectName(u"label_signal_5")
        self.label_signal_5.setMinimumSize(QSize(40, 12))
        self.label_signal_5.setMaximumSize(QSize(40, 12))
        self.label_signal_5.setFont(font)
        self.label_signal_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_5.addWidget(self.label_signal_5)

        self.horizontalSpacer_33 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_5.addItem(self.horizontalSpacer_33)

        self.graphicsView_signal_5 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_5.setObjectName(u"graphicsView_signal_5")
        sizePolicy.setHeightForWidth(self.graphicsView_signal_5.sizePolicy().hasHeightForWidth())
        self.graphicsView_signal_5.setSizePolicy(sizePolicy)
        self.graphicsView_signal_5.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_5.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_5.addWidget(self.graphicsView_signal_5)

        self.comboBox_mark_5 = QComboBox(self.centralwidget)
        self.comboBox_mark_5.setObjectName(u"comboBox_mark_5")
        self.comboBox_mark_5.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_5.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_5.addWidget(self.comboBox_mark_5)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_5)

        self.horizontalLayout_signal_6 = QHBoxLayout()
        self.horizontalLayout_signal_6.setSpacing(0)
        self.horizontalLayout_signal_6.setObjectName(u"horizontalLayout_signal_6")
        self.horizontalLayout_signal_6.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_11 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_6.addItem(self.horizontalSpacer_11)

        self.label_signal_6 = QLabel(self.centralwidget)
        self.label_signal_6.setObjectName(u"label_signal_6")
        self.label_signal_6.setMinimumSize(QSize(40, 12))
        self.label_signal_6.setMaximumSize(QSize(40, 12))
        self.label_signal_6.setFont(font)
        self.label_signal_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_6.addWidget(self.label_signal_6)

        self.horizontalSpacer_34 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_6.addItem(self.horizontalSpacer_34)

        self.graphicsView_signal_6 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_6.setObjectName(u"graphicsView_signal_6")
        self.graphicsView_signal_6.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_6.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_6.addWidget(self.graphicsView_signal_6)

        self.comboBox_mark_6 = QComboBox(self.centralwidget)
        self.comboBox_mark_6.setObjectName(u"comboBox_mark_6")
        self.comboBox_mark_6.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_6.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_6.addWidget(self.comboBox_mark_6)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_6)

        self.horizontalLayout_signal_7 = QHBoxLayout()
        self.horizontalLayout_signal_7.setSpacing(0)
        self.horizontalLayout_signal_7.setObjectName(u"horizontalLayout_signal_7")
        self.horizontalLayout_signal_7.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_12 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_7.addItem(self.horizontalSpacer_12)

        self.label_signal_7 = QLabel(self.centralwidget)
        self.label_signal_7.setObjectName(u"label_signal_7")
        self.label_signal_7.setMinimumSize(QSize(40, 12))
        self.label_signal_7.setMaximumSize(QSize(40, 12))
        self.label_signal_7.setFont(font)
        self.label_signal_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_7.addWidget(self.label_signal_7)

        self.horizontalSpacer_35 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_7.addItem(self.horizontalSpacer_35)

        self.graphicsView_signal_7 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_7.setObjectName(u"graphicsView_signal_7")
        self.graphicsView_signal_7.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_7.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_7.addWidget(self.graphicsView_signal_7)

        self.comboBox_mark_7 = QComboBox(self.centralwidget)
        self.comboBox_mark_7.setObjectName(u"comboBox_mark_7")
        self.comboBox_mark_7.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_7.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_signal_7.addWidget(self.comboBox_mark_7)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_7)

        self.horizontalLayout_signal_8 = QHBoxLayout()
        self.horizontalLayout_signal_8.setSpacing(0)
        self.horizontalLayout_signal_8.setObjectName(u"horizontalLayout_signal_8")
        self.horizontalLayout_signal_8.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_13 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_8.addItem(self.horizontalSpacer_13)

        self.label_signal_8 = QLabel(self.centralwidget)
        self.label_signal_8.setObjectName(u"label_signal_8")
        self.label_signal_8.setMinimumSize(QSize(40, 12))
        self.label_signal_8.setMaximumSize(QSize(40, 12))
        self.label_signal_8.setFont(font)
        self.label_signal_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_8.addWidget(self.label_signal_8)

        self.horizontalSpacer_36 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_8.addItem(self.horizontalSpacer_36)

        self.graphicsView_signal_8 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_8.setObjectName(u"graphicsView_signal_8")
        self.graphicsView_signal_8.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_8.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_8.addWidget(self.graphicsView_signal_8)

        self.comboBox_mark_8 = QComboBox(self.centralwidget)
        self.comboBox_mark_8.setObjectName(u"comboBox_mark_8")
        self.comboBox_mark_8.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_8.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_8.addWidget(self.comboBox_mark_8)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_8)

        self.horizontalLayout_signal_9 = QHBoxLayout()
        self.horizontalLayout_signal_9.setSpacing(0)
        self.horizontalLayout_signal_9.setObjectName(u"horizontalLayout_signal_9")
        self.horizontalLayout_signal_9.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_14 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_9.addItem(self.horizontalSpacer_14)

        self.label_signal_9 = QLabel(self.centralwidget)
        self.label_signal_9.setObjectName(u"label_signal_9")
        self.label_signal_9.setMinimumSize(QSize(40, 12))
        self.label_signal_9.setMaximumSize(QSize(40, 12))
        self.label_signal_9.setFont(font)
        self.label_signal_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_9.addWidget(self.label_signal_9)

        self.horizontalSpacer_37 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_9.addItem(self.horizontalSpacer_37)

        self.graphicsView_signal_9 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_9.setObjectName(u"graphicsView_signal_9")
        self.graphicsView_signal_9.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_9.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_9.addWidget(self.graphicsView_signal_9)

        self.comboBox_mark_9 = QComboBox(self.centralwidget)
        self.comboBox_mark_9.setObjectName(u"comboBox_mark_9")
        self.comboBox_mark_9.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_9.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_signal_9.addWidget(self.comboBox_mark_9)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_9)

        self.horizontalLayout_signal_10 = QHBoxLayout()
        self.horizontalLayout_signal_10.setSpacing(0)
        self.horizontalLayout_signal_10.setObjectName(u"horizontalLayout_signal_10")
        self.horizontalLayout_signal_10.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_15 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_10.addItem(self.horizontalSpacer_15)

        self.label_signal_10 = QLabel(self.centralwidget)
        self.label_signal_10.setObjectName(u"label_signal_10")
        self.label_signal_10.setMinimumSize(QSize(40, 12))
        self.label_signal_10.setMaximumSize(QSize(40, 12))
        self.label_signal_10.setFont(font)
        self.label_signal_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_10.addWidget(self.label_signal_10)

        self.horizontalSpacer_38 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_10.addItem(self.horizontalSpacer_38)

        self.graphicsView_signal_10 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_10.setObjectName(u"graphicsView_signal_10")
        self.graphicsView_signal_10.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_10.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_10.addWidget(self.graphicsView_signal_10)

        self.comboBox_mark_10 = QComboBox(self.centralwidget)
        self.comboBox_mark_10.setObjectName(u"comboBox_mark_10")
        self.comboBox_mark_10.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_10.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_10.addWidget(self.comboBox_mark_10)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_10)

        self.horizontalLayout_signal_11 = QHBoxLayout()
        self.horizontalLayout_signal_11.setSpacing(0)
        self.horizontalLayout_signal_11.setObjectName(u"horizontalLayout_signal_11")
        self.horizontalLayout_signal_11.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_16 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_11.addItem(self.horizontalSpacer_16)

        self.label_signal_11 = QLabel(self.centralwidget)
        self.label_signal_11.setObjectName(u"label_signal_11")
        self.label_signal_11.setMinimumSize(QSize(40, 12))
        self.label_signal_11.setMaximumSize(QSize(40, 12))
        self.label_signal_11.setFont(font)
        self.label_signal_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_11.addWidget(self.label_signal_11)

        self.horizontalSpacer_39 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_11.addItem(self.horizontalSpacer_39)

        self.graphicsView_signal_11 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_11.setObjectName(u"graphicsView_signal_11")
        self.graphicsView_signal_11.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_11.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_11.addWidget(self.graphicsView_signal_11)

        self.comboBox_mark_11 = QComboBox(self.centralwidget)
        self.comboBox_mark_11.setObjectName(u"comboBox_mark_11")
        self.comboBox_mark_11.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_11.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_11.addWidget(self.comboBox_mark_11)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_11)

        self.horizontalLayout_signal_12 = QHBoxLayout()
        self.horizontalLayout_signal_12.setSpacing(0)
        self.horizontalLayout_signal_12.setObjectName(u"horizontalLayout_signal_12")
        self.horizontalLayout_signal_12.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_17 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_12.addItem(self.horizontalSpacer_17)

        self.label_signal_12 = QLabel(self.centralwidget)
        self.label_signal_12.setObjectName(u"label_signal_12")
        self.label_signal_12.setMinimumSize(QSize(40, 12))
        self.label_signal_12.setMaximumSize(QSize(40, 12))
        self.label_signal_12.setFont(font)
        self.label_signal_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_12.addWidget(self.label_signal_12)

        self.horizontalSpacer_40 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_12.addItem(self.horizontalSpacer_40)

        self.graphicsView_signal_12 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_12.setObjectName(u"graphicsView_signal_12")
        self.graphicsView_signal_12.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_12.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_12.addWidget(self.graphicsView_signal_12)

        self.comboBox_mark_12 = QComboBox(self.centralwidget)
        self.comboBox_mark_12.setObjectName(u"comboBox_mark_12")
        self.comboBox_mark_12.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_12.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_12.addWidget(self.comboBox_mark_12)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_12)

        self.horizontalLayout_signal_13 = QHBoxLayout()
        self.horizontalLayout_signal_13.setSpacing(0)
        self.horizontalLayout_signal_13.setObjectName(u"horizontalLayout_signal_13")
        self.horizontalLayout_signal_13.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_18 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_13.addItem(self.horizontalSpacer_18)

        self.label_signal_13 = QLabel(self.centralwidget)
        self.label_signal_13.setObjectName(u"label_signal_13")
        self.label_signal_13.setMinimumSize(QSize(40, 12))
        self.label_signal_13.setMaximumSize(QSize(40, 12))
        self.label_signal_13.setFont(font)
        self.label_signal_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_13.addWidget(self.label_signal_13)

        self.horizontalSpacer_41 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_13.addItem(self.horizontalSpacer_41)

        self.graphicsView_signal_13 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_13.setObjectName(u"graphicsView_signal_13")
        self.graphicsView_signal_13.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_13.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_13.addWidget(self.graphicsView_signal_13)

        self.comboBox_mark_13 = QComboBox(self.centralwidget)
        self.comboBox_mark_13.setObjectName(u"comboBox_mark_13")
        self.comboBox_mark_13.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_13.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_13.addWidget(self.comboBox_mark_13)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_13)

        self.horizontalLayout_signal_14 = QHBoxLayout()
        self.horizontalLayout_signal_14.setSpacing(0)
        self.horizontalLayout_signal_14.setObjectName(u"horizontalLayout_signal_14")
        self.horizontalLayout_signal_14.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_19 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_14.addItem(self.horizontalSpacer_19)

        self.label_signal_14 = QLabel(self.centralwidget)
        self.label_signal_14.setObjectName(u"label_signal_14")
        self.label_signal_14.setMinimumSize(QSize(40, 12))
        self.label_signal_14.setMaximumSize(QSize(40, 12))
        self.label_signal_14.setFont(font)
        self.label_signal_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_14.addWidget(self.label_signal_14)

        self.horizontalSpacer_42 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_14.addItem(self.horizontalSpacer_42)

        self.graphicsView_signal_14 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_14.setObjectName(u"graphicsView_signal_14")
        self.graphicsView_signal_14.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_14.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_14.addWidget(self.graphicsView_signal_14)

        self.comboBox_mark_14 = QComboBox(self.centralwidget)
        self.comboBox_mark_14.setObjectName(u"comboBox_mark_14")
        self.comboBox_mark_14.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_14.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_14.addWidget(self.comboBox_mark_14)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_14)

        self.horizontalLayout_signal_15 = QHBoxLayout()
        self.horizontalLayout_signal_15.setSpacing(0)
        self.horizontalLayout_signal_15.setObjectName(u"horizontalLayout_signal_15")
        self.horizontalLayout_signal_15.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_20 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_15.addItem(self.horizontalSpacer_20)

        self.label_signal_15 = QLabel(self.centralwidget)
        self.label_signal_15.setObjectName(u"label_signal_15")
        self.label_signal_15.setMinimumSize(QSize(40, 12))
        self.label_signal_15.setMaximumSize(QSize(40, 12))
        self.label_signal_15.setFont(font)
        self.label_signal_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_15.addWidget(self.label_signal_15)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.horizontalLayout_signal_15.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_44 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_15.addItem(self.horizontalSpacer_44)

        self.graphicsView_signal_15 = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_15.setObjectName(u"graphicsView_signal_15")
        self.graphicsView_signal_15.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_15.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_signal_15.addWidget(self.graphicsView_signal_15)

        self.comboBox_mark_15 = QComboBox(self.centralwidget)
        self.comboBox_mark_15.setObjectName(u"comboBox_mark_15")
        self.comboBox_mark_15.setMinimumSize(QSize(75, 40))
        self.comboBox_mark_15.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_signal_15.addWidget(self.comboBox_mark_15)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_15)

        self.horizontalLayout_signal_time = QHBoxLayout()
        self.horizontalLayout_signal_time.setSpacing(0)
        self.horizontalLayout_signal_time.setObjectName(u"horizontalLayout_signal_time")
        self.horizontalLayout_signal_time.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalSpacer_21 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_time.addItem(self.horizontalSpacer_21)

        self.label_signal_time = QLabel(self.centralwidget)
        self.label_signal_time.setObjectName(u"label_signal_time")
        self.label_signal_time.setMinimumSize(QSize(40, 12))
        self.label_signal_time.setMaximumSize(QSize(40, 16777215))
        self.label_signal_time.setFont(font)
        self.label_signal_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_signal_time.addWidget(self.label_signal_time)

        self.horizontalSpacer_43 = QSpacerItem(6, 6, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_time.addItem(self.horizontalSpacer_43)

        self.graphicsView_signal_axis = QGraphicsView(self.centralwidget)
        self.graphicsView_signal_axis.setObjectName(u"graphicsView_signal_axis")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.graphicsView_signal_axis.sizePolicy().hasHeightForWidth())
        self.graphicsView_signal_axis.setSizePolicy(sizePolicy4)
        self.graphicsView_signal_axis.setMinimumSize(QSize(0, 40))
        self.graphicsView_signal_axis.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_signal_time.addWidget(self.graphicsView_signal_axis)

        self.horizonatal_spacer_signal_combo_mark = QSpacerItem(75, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_signal_time.addItem(self.horizonatal_spacer_signal_combo_mark)


        self.verticalLayout_signals.addLayout(self.horizontalLayout_signal_time)


        self.horizontalLayout_data.addLayout(self.verticalLayout_signals)

        self.verticalLayout_annotation_list_widget = QVBoxLayout()
        self.verticalLayout_annotation_list_widget.setObjectName(u"verticalLayout_annotation_list_widget")
        self.verticalLayout_annotation_list_widget.setSizeConstraint(QLayout.SetMaximumSize)
        self.comboBox_annotation = QComboBox(self.centralwidget)
        self.comboBox_annotation.setObjectName(u"comboBox_annotation")
        self.comboBox_annotation.setMinimumSize(QSize(300, 25))
        self.comboBox_annotation.setMaximumSize(QSize(300, 25))

        self.verticalLayout_annotation_list_widget.addWidget(self.comboBox_annotation)

        self.listWidget_annotation = QListWidget(self.centralwidget)
        self.listWidget_annotation.setObjectName(u"listWidget_annotation")
        self.listWidget_annotation.setMinimumSize(QSize(300, 0))
        self.listWidget_annotation.setMaximumSize(QSize(300, 16777215))

        self.verticalLayout_annotation_list_widget.addWidget(self.listWidget_annotation)


        self.horizontalLayout_data.addLayout(self.verticalLayout_annotation_list_widget)


        self.verticalLayout.addLayout(self.horizontalLayout_data)

        SignalWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SignalWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1282, 23))
        SignalWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SignalWindow)
        self.statusbar.setObjectName(u"statusbar")
        SignalWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SignalWindow)

        QMetaObject.connectSlotsByName(SignalWindow)
    # setupUi

    def retranslateUi(self, SignalWindow):
        SignalWindow.setWindowTitle(QCoreApplication.translate("SignalWindow", u"Signal Window", None))
        self.pushButton_sync_y.setText(QCoreApplication.translate("SignalWindow", u"Sync Y", None))
        self.pushButton_filter.setText(QCoreApplication.translate("SignalWindow", u"Filter", None))
        self.pushButton_notch.setText(QCoreApplication.translate("SignalWindow", u"Notch", None))
        self.pushButton_save.setText(QCoreApplication.translate("SignalWindow", u"Save", None))
        self.pushButton_load.setText(QCoreApplication.translate("SignalWindow", u"Load", None))
        self.pushButton_mark.setText(QCoreApplication.translate("SignalWindow", u"Mark", None))
#if QT_CONFIG(tooltip)
        self.pushButton_show_hypnogram.setToolTip(QCoreApplication.translate("SignalWindow", u"Show Hypnogram Plot", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_hypnogram.setText(QCoreApplication.translate("SignalWindow", u"Hyp", None))
#if QT_CONFIG(tooltip)
        self.pushButton_show_spectrogram_plot.setToolTip(QCoreApplication.translate("SignalWindow", u"Show Spectrogram Plot", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_spectrogram_plot.setText(QCoreApplication.translate("SignalWindow", u"Spc", None))
#if QT_CONFIG(tooltip)
        self.pushButton_show_annotation_panel.setToolTip(QCoreApplication.translate("SignalWindow", u"Show Annotation Plot", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_annotation_panel.setText(QCoreApplication.translate("SignalWindow", u"Ann", None))
        self.label_3.setText(QCoreApplication.translate("SignalWindow", u"Hypnogram", None))
#if QT_CONFIG(tooltip)
        self.pushButton_show_hypnogram_stages_in_color.setToolTip(QCoreApplication.translate("SignalWindow", u"Show Stages", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_show_hypnogram_stages_in_color.setText(QCoreApplication.translate("SignalWindow", u"Show", None))
        self.pushButton_hypnogram_legend.setText(QCoreApplication.translate("SignalWindow", u"L", None))
        self.label_mt_spacer_3.setText("")
        self.label_spectrogram.setText(QCoreApplication.translate("SignalWindow", u"Multi-Taper Spectrogram", None))
        self.label_mt_spacer_2.setText("")
        self.label_mt_spacer.setText("")
        self.pushButton_show_spectrogram.setText(QCoreApplication.translate("SignalWindow", u"Spect.", None))
        self.pushButton_spectrogram_legend.setText(QCoreApplication.translate("SignalWindow", u"L", None))
        self.pushButton_heatmap.setText(QCoreApplication.translate("SignalWindow", u"Heat", None))
        self.pushButton_heat_legend.setText(QCoreApplication.translate("SignalWindow", u"L", None))
        self.pushButton_annotation_legend.setText(QCoreApplication.translate("SignalWindow", u"Legend", None))
        self.label_epoch_numbers.setText(QCoreApplication.translate("SignalWindow", u"Epochs", None))
        self.label.setText("")
        self.pushButton_epoch_show_stages.setText(QCoreApplication.translate("SignalWindow", u"Stages", None))
        self.pushButton_first.setText(QCoreApplication.translate("SignalWindow", u"\u2759\u25c0", None))
        self.pushButton_next.setText(QCoreApplication.translate("SignalWindow", u"\u25b6", None))
        self.pushButton_update.setText(QCoreApplication.translate("SignalWindow", u"U", None))
        self.label_page.setText(QCoreApplication.translate("SignalWindow", u"1 of x pages", None))
        self.pushButton_previous.setText(QCoreApplication.translate("SignalWindow", u"\u25c0", None))
        self.pushButton_last.setText(QCoreApplication.translate("SignalWindow", u"\u25b6\u2759", None))
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
        self.label_signal_time.setText(QCoreApplication.translate("SignalWindow", u"time:", None))
    # retranslateUi

