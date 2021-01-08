from PyQt5.QtWidgets import QItemDelegate
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from dbOps import Database
import config


class CustomTableModel(QAbstractTableModel):
    def __init__(self, table_name):
        QAbstractTableModel.__init__(self)
        self.db = Database(config)
        self.dict_data = self.db.get_multiple_data(table_name)
        self.columns = self.db.get_columns(table_name)  # list of column names
        self.table_name = table_name
        self.get_word_count()

    def get_word_count(self):
        if self.table_name == 'listofdicts':
            for x in range(len(self.dict_data)):
                if type(self.dict_data[x][1]) == str:
                    self.dict_data[x][4] = self.db.get_rowcount(
                        self.dict_data[x][1])
#				print(str(self.dict_data[x][1]))

    def flags(self, index):
        # manages the attributes of the columns' fields
        if self.table_name == 'listofdicts':
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def rowCount(self, *args, **kwargs):
        # returns the number of rows
        return len(self.dict_data)

    def columnCount(self, *args, **kwargs):
        # returns the number of columns
        return len(self.columns)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # returns a list with the languages as header
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section]

    def data(self, index, role):
        # displays the data
        row = self.dict_data[index.row()]
        column = index.column()
        try:
            if role == Qt.DisplayRole:
                return str(row[column])
        except:
            return None

    def setData(self, index, value, role=Qt.EditRole):
        # edits data
        try:
            if index.isValid():
                selected_row = self.dict_data[index.row()]
                selected_column = index.column()
                selected_row[selected_column] = value
                self.dataChanged.emit(index, index, (Qt.DisplayRole, ))
                status = self.db.update_existing(self.table_name,
                                                 self.columns[selected_column],
                                                 selected_row[0],
                                                 value)
                if status:
                    return True
        except:
            return False

    def updateTable(self, table_name):
        # updates the whole model
        self.beginResetModel()
        self.dict_data = self.db.get_multiple_data(table_name)
        self.columns = self.db.get_columns(table_name)
        self.table_name = table_name
        self.get_word_count()
        self.endResetModel()

    def insertRows(self):
        # inserts an empty row
        row_count = len(self.dict_data)
        self.beginInsertRows(QModelIndex(), row_count, row_count)
        new_row_id = self.db.insert_data(self.table_name,
                                         self.columns[1],
                                         None)
        columns_count = len(self.columns)
        new_row = [None for x in range(columns_count)]
        new_row[0] = new_row_id[0]
        self.dict_data.append(new_row)
        row_count += 1
        self.endInsertRows()
        return True

    def removeRows(self, position):
        # removes a row
        row_count = self.rowCount()
        row_count -= 1
        self.beginRemoveRows(QModelIndex(), row_count, row_count)
        model_row_id = position.row()
        db_row_id = self.dict_data[model_row_id][0]
        self.db.remove_data(self.table_name, db_row_id)
        self.dict_data.pop(model_row_id)
        self.endRemoveRows()
        return True


class MainTableDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        return super(MainTableDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        text = index.data(Qt.EditRole) or index.data(Qt.DisplayRole)
        editor.setText(str(text))
