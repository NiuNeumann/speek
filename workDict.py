from PyQt5.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QTableView, QAbstractItemView,
                             QMenu, QLabel, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QCursor
from model import MainTableDelegate


class WorkDict(QWidget):
    clicked = pyqtSignal()

    def __init__(self, model, parent=None):
        QWidget.__init__(self)

        self.model = model

        self.backtobrowseBtn = QPushButton("<<<", self)
        self.backtobrowseBtn.setGeometry(QRect(0, 0, 20, 20))
        self.backtobrowseBtn.setMinimumHeight(20)
        self.backtobrowseBtn.clicked.connect(lambda: self.clicked.emit())

        # problem here is that the button gets created in the beginning and then the label doesnt update
        self.dictnameLabel = QLabel(self.model.table_name)

        self.tableView = QTableView()
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.horizontalHeader().setStretchLastSection(False)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableView.verticalHeader().setCascadingSectionResizes(False)
        self.tableView.setShowGrid(False)
        # set model
        self.tableView.setModel(self.model)
        # set delegate
        self.delegate = MainTableDelegate()
        self.tableView.setItemDelegate(self.delegate)
        # set context menu
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.context_menu)
        self.tableView.hideColumn(0)
        self.tableView.setColumnWidth(1, 60)
        self.tableView.setColumnWidth(2, 60)

        self.addInfoLabel = QLabel(
            "Workbench in the works.", self)
        self.addInfoLabel.setWordWrap(True)

        self.addrowBtn = QPushButton('Add New Entry', self)
        self.addrowBtn.clicked.connect(lambda: self.model.insertRows())

        # layout with gridlayout
        self.layout = QGridLayout()
        self.layout.addWidget(self.backtobrowseBtn, 0, 0, 1, 1)
        self.layout.addWidget(self.dictnameLabel, 0, 1, 1, 2)
        self.layout.addWidget(self.tableView, 1, 0, 7, 3)
        self.layout.addWidget(self.addInfoLabel, 0, 3, 8, 3)
        self.layout.addWidget(self.addrowBtn, 8, 0, 1, 6)
        self.setLayout(self.layout)

    def context_menu(self):
        menu = QMenu()
        if self.tableView.selectedIndexes():
            remove_data = menu.addAction("Delete Entry")
            remove_data.triggered.connect(
                lambda: self.model.removeRows(self.tableView.currentIndex()))
        add_entry = menu.addAction("Add New Entry")
        add_entry.triggered.connect(lambda: self.model.insertRows())
        cursor = QCursor
        menu.exec_(cursor.pos())
