from PyQt5.QtWidgets import QTableView, QItemDelegate
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
import shelve

class CustomTableModel(QAbstractTableModel):
	def __init__(self, data):
		QAbstractTableModel.__init__(self)
		self.dict_data = data
		self.columns = list(self.dict_data.keys())	# Keys from first row, might not work since different dicts
#		klist = self.dict_data.keys()
#		subklist = []
#		for keys in klist:
#			subklist.append(list(self.dict_data[keys].values))
#			eventuell schauen: wenn key kein weiteres dict enthält, dann zur klist hinzufügen, ansonsten das dict aus
#			dem key öffnen und dann für alle keys in dem dict erneut checken und ggnfalls hinzufügen oder weiter machen 

	def flags(self, index):
		# if index.column() > 0:
		return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
		
	def rowCount(self, *args, **kwargs):
		return len(self.dict_data)

	def columnCount(self, *args, **kwargs):
		return len(self.columns)

#	def headerData(self, section, orientation, role=Qt.DisplayRole):
#		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
#			return self.columns[section].title()

	def data(self, index, role):
		row = self.dict_data[index.row()]
		column = self.columns[index.column()]

		try:
			if role == Qt.DisplayRole:
				return str(row[column])
		except KeyError:
			return None

	def setData(self, index, value, role=Qt.EditRole):
		if index.isValid():
			selected_row = self.dict_data(index.row())
			selected_column = self.dict_data(index.column())
			selected_row[selected_column] = value
			self.dataChanged.emit(index, index, (Qt.DisplayRole, ))
			ok = databaseOperations.update_existing(selected_row['_id'], selected_row)
			if ok:
				return True
		return False

	def insertRows(self):
		row_count = len(self.dict_data)
		self.beginInsertRows(QModelIndex(), row_count, row_count)
		empty_data = { key: None for key in self.columns if not key == '_id'}
		document_id = databaseOperations.insert_data(empty_data)
		new_data = databaseOperations.get_single_data(document_id)
		self.dict_data.append(new_data)
		row_count += 1
		self.endInsertRows()
		return True

	def removeRows(self, position):
		row_count = self.rowCount()
		row_count -= 1
		self.beginRemoveRows(QModelIndex(), row_count, row_count)
		row_id = position.row()
		document_id = self.dict_data[row_id]['_id']
		databaseOperations.remove_data(document_id)
		self.dict_data.pop(row_id)
		self.endRemoveRows()
		return True

class InLineEditDelegate(QItemDelegate):
	def CreateEditor(self, parent, option, index):
		return super(InLineEditDelegate, self).createEditor(parent, option, index)

	def setEditorData(self, editor, data):
		text = index.data(Qt.EditRole) or index.data(Qt.DisplayRole)
		editor.setText(str(text))










