from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QAbstractItemView, QMenu
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from createDict import AddDict
from model import MainTableDelegate


class OpenDict(QWidget):
    clicked = pyqtSignal()

    def __init__(self, model, parent=None):
        QWidget.__init__(self)
        self.model = model
        self.popup = AddDict()

        self.tableView = QTableView()
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.tableView.verticalHeader().setCascadingSectionResizes(False)
        self.tableView.setShowGrid(False)

        self.tableView.setModel(self.model)

        self.delegate = MainTableDelegate()
        self.tableView.setItemDelegate(self.delegate)

        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.context_menu)
        self.tableView.hideColumn(0)
        self.tableView.setColumnWidth(1, 80)
        self.tableView.setColumnWidth(2, 80)
        self.tableView.setColumnWidth(3, 80)
        self.tableView.setColumnWidth(4, 50)

        self.tableView.doubleClicked.connect(lambda: self.double_click())

        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.addWidget(self.tableView)
        self.setLayout(self.vboxlayout)

    def context_menu(self):
        if self.model.table_name == 'listofdicts':
            menu = QMenu()
            if self.tableView.selectedIndexes():
                open_data = menu.addAction("Open Dictionary")
                open_data.triggered.connect(lambda: self.open_dict())
                remove_data = menu.addAction("Delete Dictionary")
                remove_data.triggered.connect(
                    lambda: self.delete_dict(self.tableView.currentIndex()))
            add_data = menu.addAction("Add New Dictionary")
            add_data.triggered.connect(lambda: self.show_popup())
            cursor = QCursor
            menu.exec_(cursor.pos())
        else:
            menu = QMenu()
            add_entry = menu.addAction("Add New Row")
            add_entry.triggered.connect(lambda: self.model.insertRows())
            cursor = QCursor
            menu.exec_(cursor.pos())

    # @pyqtSlot("QModelIndex")
    # what?
    def double_click(self):
        if self.model.table_name == 'listofdicts':
            if self.tableView.selectedIndexes():
                self.open_dict()
        else:
            if self.tableView.selectedIndexes():
                pass
            else:
                self.model.insertRows()

    def show_popup(self):
        self.popup.show()
        if self.popup.exec():
            self.write_new_dict(self.popup.getInputs())

    def open_dict(self):
        row = self.tableView.currentIndex().row()
        table_name = str(self.model.dict_data[row][1])
        self.model.updateTable(table_name)
        self.clicked.emit()

    def delete_dict(self, position):
        self.model.db.drop_table(self.model.dict_data[position.row()][1])
        self.model.removeRows(position)

    def write_new_dict(self, list_of_values):
        # https://forum.qt.io/topic/94170/how-to-modify-the-data-in-the-model-and-update-the-view-when-new-data-is-received-from-external/26
        self.model.insertRows()
        rownumber = len(self.model.dict_data) - 1
        for x in range(3):
            index = self.model.createIndex(rownumber, (x+1))
            self.model.setData(index, list_of_values[x])
        name = list_of_values[0]
        from_lang = list_of_values[1]
        to_lang = list_of_values[2]
        self.model.db.create_table(name, from_lang, to_lang)
