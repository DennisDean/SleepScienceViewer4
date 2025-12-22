# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CreateBatchFileDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(564, 368)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plainTextEdit_selected_folder = QPlainTextEdit(Dialog)
        self.plainTextEdit_selected_folder.setObjectName(u"plainTextEdit_selected_folder")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plainTextEdit_selected_folder.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_selected_folder.setSizePolicy(sizePolicy1)
        self.plainTextEdit_selected_folder.setMinimumSize(QSize(0, 30))
        self.plainTextEdit_selected_folder.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.plainTextEdit_selected_folder)

        self.pushButton_select_batch_folder = QPushButton(Dialog)
        self.pushButton_select_batch_folder.setObjectName(u"pushButton_select_batch_folder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_select_batch_folder.sizePolicy().hasHeightForWidth())
        self.pushButton_select_batch_folder.setSizePolicy(sizePolicy2)
        self.pushButton_select_batch_folder.setMinimumSize(QSize(75, 25))
        self.pushButton_select_batch_folder.setMaximumSize(QSize(75, 25))

        self.horizontalLayout.addWidget(self.pushButton_select_batch_folder)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_subject_extraction_id = QGroupBox(Dialog)
        self.groupBox_subject_extraction_id.setObjectName(u"groupBox_subject_extraction_id")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_subject_extraction_id.sizePolicy().hasHeightForWidth())
        self.groupBox_subject_extraction_id.setSizePolicy(sizePolicy3)
        self.groupBox_subject_extraction_id.setMinimumSize(QSize(300, 75))
        self.groupBox_subject_extraction_id.setMaximumSize(QSize(16777215, 75))
        self.radioButton_edf = QRadioButton(self.groupBox_subject_extraction_id)
        self.radioButton_edf.setObjectName(u"radioButton_edf")
        self.radioButton_edf.setGeometry(QRect(220, 40, 71, 25))
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.radioButton_edf.sizePolicy().hasHeightForWidth())
        self.radioButton_edf.setSizePolicy(sizePolicy4)
        self.radioButton_edf.setMinimumSize(QSize(50, 25))
        self.radioButton_edf.setMaximumSize(QSize(16777215, 25))
        self.radioButton_generate = QRadioButton(self.groupBox_subject_extraction_id)
        self.radioButton_generate.setObjectName(u"radioButton_generate")
        self.radioButton_generate.setGeometry(QRect(10, 40, 90, 25))
        sizePolicy4.setHeightForWidth(self.radioButton_generate.sizePolicy().hasHeightForWidth())
        self.radioButton_generate.setSizePolicy(sizePolicy4)
        self.radioButton_generate.setMinimumSize(QSize(90, 25))
        self.radioButton_generate.setMaximumSize(QSize(16777215, 25))
        self.radioButton_extract = QRadioButton(self.groupBox_subject_extraction_id)
        self.radioButton_extract.setObjectName(u"radioButton_extract")
        self.radioButton_extract.setGeometry(QRect(120, 40, 81, 25))
        sizePolicy4.setHeightForWidth(self.radioButton_extract.sizePolicy().hasHeightForWidth())
        self.radioButton_extract.setSizePolicy(sizePolicy4)
        self.radioButton_extract.setMinimumSize(QSize(60, 25))
        self.radioButton_extract.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_3.addWidget(self.groupBox_subject_extraction_id)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_extract_subject_id_function = QVBoxLayout()
        self.verticalLayout_extract_subject_id_function.setObjectName(u"verticalLayout_extract_subject_id_function")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy5)
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_extract_subject_id_function.addWidget(self.label_2, 0, Qt.AlignTop)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.plainTextEdit_subject_id_function = QPlainTextEdit(Dialog)
        self.plainTextEdit_subject_id_function.setObjectName(u"plainTextEdit_subject_id_function")
        sizePolicy1.setHeightForWidth(self.plainTextEdit_subject_id_function.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_subject_id_function.setSizePolicy(sizePolicy1)
        self.plainTextEdit_subject_id_function.setMinimumSize(QSize(0, 30))
        self.plainTextEdit_subject_id_function.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_6.addWidget(self.plainTextEdit_subject_id_function)

        self.pushButton_select_subject_id_function = QPushButton(Dialog)
        self.pushButton_select_subject_id_function.setObjectName(u"pushButton_select_subject_id_function")
        self.pushButton_select_subject_id_function.setMinimumSize(QSize(25, 25))
        self.pushButton_select_subject_id_function.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_6.addWidget(self.pushButton_select_subject_id_function)


        self.verticalLayout_extract_subject_id_function.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_3.addLayout(self.verticalLayout_extract_subject_id_function)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_generate_options = QVBoxLayout()
        self.verticalLayout_generate_options.setObjectName(u"verticalLayout_generate_options")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_generate_options.addWidget(self.label, 0, Qt.AlignTop)

        self.plainTextEdit_subject_prefix = QPlainTextEdit(Dialog)
        self.plainTextEdit_subject_prefix.setObjectName(u"plainTextEdit_subject_prefix")
        sizePolicy1.setHeightForWidth(self.plainTextEdit_subject_prefix.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_subject_prefix.setSizePolicy(sizePolicy1)
        self.plainTextEdit_subject_prefix.setMinimumSize(QSize(0, 30))
        self.plainTextEdit_subject_prefix.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_generate_options.addWidget(self.plainTextEdit_subject_prefix, 0, Qt.AlignTop)


        self.horizontalLayout_2.addLayout(self.verticalLayout_generate_options)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_load = QPushButton(Dialog)
        self.pushButton_load.setObjectName(u"pushButton_load")
        self.pushButton_load.setMinimumSize(QSize(75, 25))
        self.pushButton_load.setMaximumSize(QSize(75, 25))

        self.horizontalLayout_4.addWidget(self.pushButton_load, 0, Qt.AlignRight)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        sizePolicy5.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy5)
        self.label_4.setMinimumSize(QSize(0, 25))
        self.label_4.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_5.addWidget(self.label_4)

        self.lineEditload_message = QLineEdit(Dialog)
        self.lineEditload_message.setObjectName(u"lineEditload_message")
        self.lineEditload_message.setMinimumSize(QSize(0, 30))
        self.lineEditload_message.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_5.addWidget(self.lineEditload_message)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.verticalLayout_6)

        self.line_3 = QFrame(Dialog)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.comboBox_load_results = QComboBox(Dialog)
        self.comboBox_load_results.setObjectName(u"comboBox_load_results")

        self.verticalLayout_5.addWidget(self.comboBox_load_results)

        self.textEdit_result_box = QTextEdit(Dialog)
        self.textEdit_result_box.setObjectName(u"textEdit_result_box")

        self.verticalLayout_5.addWidget(self.textEdit_result_box)


        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Create  Batch File", None))
        self.pushButton_select_batch_folder.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.groupBox_subject_extraction_id.setTitle(QCoreApplication.translate("Dialog", u"File Subject ID", None))
        self.radioButton_edf.setText(QCoreApplication.translate("Dialog", u"EDF", None))
        self.radioButton_generate.setText(QCoreApplication.translate("Dialog", u"Generate", None))
        self.radioButton_extract.setText(QCoreApplication.translate("Dialog", u"Extract", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"ID Extract", None))
        self.pushButton_select_subject_id_function.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Save Prefix", None))
        self.pushButton_load.setText(QCoreApplication.translate("Dialog", u"Load", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Message:", None))
    # retranslateUi

