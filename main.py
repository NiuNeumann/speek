"""
To-Do
General
	- Check into seperating gui from main.py into an own file
	- Find secure way of storing login-string on system
	- Create a signal(?) in OpenDict for a doubleclick on a dictionary row which opens the dict
	- Add self.setStyleSheet() in main
	- after implementing availability-check for db create offline mode with shelve
createDict
	- create restriction that the same language cannot be selected in both QComboBoxes
dbOps
	- Limits für cursors
	- Check connection open/close
		- connection stays open, write manual close?
"""
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QStackedWidget
from openDict import OpenDict
from workDict import WorkDict
from model import CustomTableModel


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Speek")
        self.setGeometry(200, 150, 400, 500)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        # Creating the model and later handing it to the QWidgets
        self.start_table = 'listofdicts'
        self.model = CustomTableModel(self.start_table)

        # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.open_dict = OpenDict(self.model)
        self.work_dict = WorkDict(self.model)
        self.central_widget.addWidget(self.open_dict)
        self.central_widget.addWidget(self.work_dict)
        self.central_widget.setCurrentWidget(self.open_dict)

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.dict_menu = self.menu.addMenu("Dictionaries")
        self.learn_menu = self.menu.addMenu("Practice")

        new_dict = QAction("Create new Dictionary", self)
        new_dict.triggered.connect(lambda: self.open_dict.show_popup())
        self.dict_menu.addAction(new_dict)
        open_dict = QAction("Browse Dictionaries", self)
        open_dict.triggered.connect(
            lambda: self.central_widget.setCurrentWidget(self.open_dict))
        open_dict.triggered.connect(
            lambda: self.model.updateTable('listofdicts'))
        self.dict_menu.addAction(open_dict)
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)

        self.open_dict.clicked.connect(
            lambda: self.central_widget.setCurrentWidget(self.work_dict))
        self.open_dict.clicked.connect(
            lambda: self.work_dict.dictnameLabel.setText(self.model.table_name))
        self.work_dict.clicked.connect(
            lambda: self.central_widget.setCurrentWidget(self.open_dict))
        self.work_dict.clicked.connect(
            lambda: self.model.updateTable('listofdicts'))

        self.show()
    """
    def setcentralWidget(self, widget_name):
        write function for setting the central widget with all additional functionalies
    """

    def exit_app(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
