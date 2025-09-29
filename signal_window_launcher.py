import sys
from PySide6.QtWidgets import QApplication
from SignalWindowClass import SignalWindow
from EdfFileClass import EdfFile
from AnnotationXmlClass import AnnotationXml

if __name__ == '__main__':
    signal_combobox_index = int(sys.argv[1])
    edf_filepath = sys.argv[2]
    xml_filepath = sys.argv[3]

    # Create new application instance
    app = QApplication(sys.argv)

    # Load objects fresh in this process
    edf_obj = EdfFile(edf_filepath)
    edf_obj.load()

    xml_obj = AnnotationXml(xml_filepath)
    xml_obj.load()

    window = SignalWindow(edf_obj=edf_obj,
                          xml_obj=xml_obj,
                          signal_combobox_index=signal_combobox_index)
    window.show()

    sys.exit(app.exec())