from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QComboBox, QLineEdit, QMessageBox,
                             QDialog, QDialogButtonBox)


class AddDict(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add a Dictionary")
        # Create widgets
        self.addInfoLabel = QLabel(
            "Create a new dictionary by selecting the languages and name of the new dictionary.", self)
        self.addInfoLabel.setWordWrap(True)
        self.nameLabel = QLabel("Name:")
        validator = QRegExpValidator(QRegExp(r'\w*'))
        self.nameInput = QLineEdit()
        self.nameInput.setMaxLength(20)
        self.nameInput.setValidator(validator)
        self.fromLabel = QLabel("From:")
        self.fromLangBox = QComboBox(self)
        self.fromLangBox.setObjectName("From")
        self.fromLangBox.addItem("English")
        self.fromLangBox.addItem("French")
        self.fromLangBox.addItem("German")
        self.toLabel = QLabel("To:")
        self.toLangBox = QComboBox(self)
        self.toLangBox.addItem("English")
        self.toLangBox.addItem("French")
        self.toLangBox.addItem("German")
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.addInfoLabel)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.fromLabel)
        layout.addWidget(self.fromLangBox)
        layout.addWidget(self.toLabel)
        layout.addWidget(self.toLangBox)
        layout.addWidget(self.buttonBox)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to either accept or reject
        self.buttonBox.accepted.connect(lambda: self.check_input())
        self.buttonBox.rejected.connect(self.reject)

    def check_input(self):
        if self.nameInput.text() == '':
            self.noNamePopup()
        if self.fromLangBox.currentText() == self.toLangBox.currentText():
            self.sameLangPopup()
        else:
            self.accept()

    def noNamePopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Missing name")
        msg.setText("Please insert a name for the new dictionary!")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Retry)
        x = msg.exec_()

    def sameLangPopup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Same Languages selected")
        msg.setText("Please select varying languages!")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Retry)
        x = msg.exec_()

    def getInputs(self):
        return [self.nameInput.text(), str(self.fromLangBox.currentText()), str(self.toLangBox.currentText())]


"""
class CreateDict(QWidget):
	clicked = pyqtSignal()
	def __init__(self, parent=None):
		QWidget.__init__(self)
		self.setWindowTitle("Speek - Create Dictionary")

		self.vboxlayout = QVBoxLayout()

		self.addInfoLabel = QLabel("Create a new dictionary by selecting the languages and name of the new dictionary.", self)
		self.addInfoLabel.setWordWrap(True)
		self.vboxlayout.addWidget(self.addInfoLabel)

		self.nameLabel = QLabel("Name:")
		self.vboxlayout.addWidget(self.nameLabel)
		
		validator = QRegExpValidator(QRegExp(r'\w*'))
		self.nameInput = QLineEdit()
		self.nameInput.setMaxLength(20)
		self.nameInput.setValidator(validator)
		self.vboxlayout.addWidget(self.nameInput)

		self.fromLabel = QLabel("From:")
		self.vboxlayout.addWidget(self.fromLabel)

		self.fromLangBox = QComboBox(self)
		self.fromLangBox.setObjectName("From")
		self.fromLangBox.addItem("English")
		self.fromLangBox.addItem("French")
		self.fromLangBox.addItem("German")
		self.vboxlayout.addWidget(self.fromLangBox)
		
		self.toLabel = QLabel("To:")
		self.vboxlayout.addWidget(self.toLabel)

		self.toLangBox = QComboBox(self)
		self.toLangBox.addItem("English")
		self.toLangBox.addItem("French")
		self.toLangBox.addItem("German")
		self.vboxlayout.addWidget(self.toLangBox)

		self.createDictButton = QPushButton("Create Dictionary", self)
		self.createDictButton.setGeometry(QRect(20, 100, 360, 50))
		self.createDictButton.setMinimumHeight(50)
		self.createDictButton.clicked.connect(lambda: self.createNewDict(self.nameInput.text(), str(self.fromLangBox.currentText()), str(self.toLangBox.currentText())))
		self.vboxlayout.addWidget(self.createDictButton)

		self.vboxlayout.addStretch()

		self.layout = QHBoxLayout()
		self.layout.addLayout(self.vboxlayout)
		self.setLayout(self.layout)


	def createNewDict(self, dictName, fromLang, toLang):		
		if dictName == '':
			self.noNamePopup()
		else:
			newDict = shelve.open('dicts\\' + str(dictName))
			newDict['languages'] = [str(fromLang), str(toLang)]
			newDict.close()
			self.clicked.emit()
"""
