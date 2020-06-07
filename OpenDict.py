from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QAbstractItemView, QMenu
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor
from Model import *

class OpenDict(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self)
		self.setWindowTitle("Speek - Open Dictionary")

		self.vboxlayout = QVBoxLayout()

		self.tableView = QTableView()
		self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
		self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableView.setIconSize(QSize(50, 50))
		self.tableView.setSortingEnabled(True)
		self.tableView.setObjectName("tableView")
		self.tableView.horizontalHeader().setCascadingSectionResizes(True)
		self.tableView.horizontalHeader().setStretchLastSection(True)
		self.tableView.verticalHeader().setCascadingSectionResizes(False)

		self.dict_data = {"name": "MyDict1", "fromLang": "English", "toLang": "English"} #dataBaseOperations.get_multiple_data()
		self.model = CustomTableModel(self.dict_data)
		self.tableView.setModel(self.model)
		self.tableView.setItemDelegate(InLineEditDelegate())

		self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableView.customContextMenuRequested.connect(self.context_menu)

		self.vboxlayout.addWidget(self.tableView)

		self.layout = QHBoxLayout()
		self.layout.addLayout(self.vboxlayout)
		self.setLayout(self.layout)

	def context_menu(self):
		menu = QMenu()
		add_data = menu.addAction("Add New Data")
		add_data.triggered.connect(lambda: self.model.insertRows())
		if self.tableView.selectedIndexes():
			remove_data = menu.addAction("Remove Data")
			remove_data.triggered.connect(lambda: self.model.removeRows(self.tableView.currentindex()))
		cursor = QCursor
		menu.exec_(cursor.pos())