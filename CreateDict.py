from PyQt5.QtCore import QRegExp, QRect, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox
import shelve

class CreateDict(QWidget):
	clicked = pyqtSignal()
	def __init__(self, parent=None):
		QWidget.__init__(self)
		self.setWindowTitle("Speek - Create Dictionary")

		self.vboxlayout = QVBoxLayout()

		self.addInfoLabel = QLabel("Create a new dictionary by selecting the languages and name of the new dictionary.\n\nFrom:", self)
		self.addInfoLabel.setWordWrap(True)
		self.vboxlayout.addWidget(self.addInfoLabel)

		self.fromLangBox = QComboBox(self)
		self.fromLangBox.setObjectName("From")
		self.fromLangBox.addItem("English")
		self.fromLangBox.addItem("Deutsch")
		self.vboxlayout.addWidget(self.fromLangBox)

		self.fromtoLabel = QLabel("To:")
		self.vboxlayout.addWidget(self.fromtoLabel)

		self.toLangBox = QComboBox(self)
		self.toLangBox.addItem("English")
		self.toLangBox.addItem("Deutsch")
		self.vboxlayout.addWidget(self.toLangBox)

		self.nameLabel = QLabel("Name of the Dictionary:")
		self.vboxlayout.addWidget(self.nameLabel)

		validator = QRegExpValidator(QRegExp(r'\w*'))

		self.nameInput = QLineEdit()
		self.nameInput.setMaxLength(20)
		self.nameInput.setValidator(validator)
		self.vboxlayout.addWidget(self.nameInput)

		self.createDictButton = QPushButton("Create Dictionary", self)
		self.createDictButton.setGeometry(QRect(20, 100, 360, 50))
		self.createDictButton.setMinimumHeight(50)
		self.createDictButton.clicked.connect(lambda: self.createNewDict(str(self.fromLangBox.currentText()), str(self.toLangBox.currentText()), self.nameInput.text()))
		self.vboxlayout.addWidget(self.createDictButton)

		self.vboxlayout.addStretch()

		self.layout = QHBoxLayout()
		self.layout.addLayout(self.vboxlayout)
		self.setLayout(self.layout)


	def createNewDict(self, fromLang, toLang, dictName):
		if dictName == '':
			self.noNamePopup()
		else:
			newDict = shelve.open('dicts\\' + str(dictName))
			newDict['languages'] = [str(fromLang), str(toLang)]
			newDict.close()
			self.clicked.emit()

	def noNamePopup(self):
		msg = QMessageBox()
		msg.setWindowTitle("Missing name")
		msg.setText("Please insert a name for the new dictionary!")
		msg.setIcon(QMessageBox.Information)
		msg.setStandardButtons(QMessageBox.Retry)

		x = msg.exec_()