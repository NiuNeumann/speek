# https://doc.qt.io/qtforpython/tutorials/expenses/expenses.html

# To-Do:	Change to work only with one shelve file in which the dictionaries are being stored in one python dict
# To-Do:	Further investige https://doc.qt.io/qtforpython/overviews/model-view-programming.html#model-view-programming
# 			to maybe use QAbstractItemModel, QAbstractListModel or QAbstractTableModel with QTreeView to visualize
#			Maybe with MongoDB? Overkill?

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMenuBar, QAction, QWidget, QGroupBox,
							QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit,
							QStackedWidget)
import sys
from CreateDict import CreateDict
from Landing import Landing

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setGeometry(100, 100, 400, 300)
		self.setWindowIcon(QtGui.QIcon("icon.png"))

		self.central_widget = QStackedWidget()
		self.setCentralWidget(self.central_widget)
		self.landing = Landing(self)
		self.createDict = CreateDict(self)
		self.central_widget.addWidget(self.landing)
		self.central_widget.addWidget(self.createDict)
		self.central_widget.setCurrentWidget(self.landing)

		self.menu = self.menuBar()
		self.file_menu = self.menu.addMenu("File")
		self.add_menu = self.menu.addMenu("Add")
		self.learn_menu = self.menu.addMenu("Learn")

		new_dict = QAction("Create new Dictionary", self)
		new_dict.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.createDict))
		self.add_menu.addAction(new_dict)
		open_dict = QAction("Open existing Dictionary", self)
		self.add_menu.addAction(open_dict)
		exit_action = QAction("Exit", self)
		exit_action.setShortcut("Ctrl+Q")
		exit_action.triggered.connect(self.exit_app)
		self.file_menu.addAction(exit_action)

		self.createDict.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.landing))

		self.show()

	def exit_app(self):
		QApplication.quit()


if __name__ == "__main__":
      app = QApplication(sys.argv)
      window = MainWindow()
      sys.exit(app.exec_())