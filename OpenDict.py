from PyQt5.Widgets import QTableView
from PyQt5.Core import QAbstractTableModel, Qt
import shelve

class CustomTableModel(QAbstractTableModel):
	def __init__(self, data):
		QAbstractTableModel.__init__(self)
		self.dict_data = data
		self.columns = list(self.dict_data[0].keys())	# Keys from first row, might not work since different dicts

	def flags(self, index):
		if index.column() > 0:
			return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
		
	def rowCount(self, *args, **kwargs):
		return len(self.dict_data)

	def columnCount(self. *args, **kwargs):
		return len(self.columns)

	def headerData(self, section, orientation, role=Qt.DisplayRole):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.columns[section].title()

	def data(self, index, role):
