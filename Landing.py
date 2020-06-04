from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

class Landing(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self)
		self.setWindowTitle("Speek")

		self.vboxlayout = QVBoxLayout()

		self.vboxlayout.addStretch()

		self.landingLabel = QLabel("\"Learn hard and you shall taste the sweet scent of success!\"\nNiklas S. Heuer")
		self.landingLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.vboxlayout.addWidget(self.landingLabel)

		self.vboxlayout.addStretch()

		self.layout = QHBoxLayout()
		self.layout.addLayout(self.vboxlayout)
		self.setLayout(self.layout)