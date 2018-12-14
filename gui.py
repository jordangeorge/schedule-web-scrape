import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QFileDialog

import ws

class FirstWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "MyUK Schedule Web Scrape"
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        chooseFileButton = QPushButton("Choose file", self)
        chooseFileButton.clicked.connect(self.singleBrowse)

        self.chosenFileLabel = QLabel("", self)

        calendarIdLabel = QLabel("Calendar ID:", self)

        self.calendarIdTextBox = QLineEdit(self)
        self.calendarIdTextBox.setText("primary")

        addToCalButton = QPushButton("Add to calendar", self)
        addToCalButton.clicked.connect(self.addToCal)

        self.output = ""
        self.outputLabel = QLabel(self.output, self)

        layout = QGridLayout()
        layout.addWidget(chooseFileButton, 0, 0)
        layout.addWidget(self.chosenFileLabel, 0, 1)
        layout.addWidget(calendarIdLabel, 1, 0)
        layout.addWidget(self.calendarIdTextBox, 1, 1)
        layout.addWidget(addToCalButton, 2, 0)
        layout.addWidget(self.outputLabel, 3, 0)
        self.setLayout(layout)

        self.show()

    def singleBrowse(self):
        self.filePath = QFileDialog.getOpenFileName(self,
                                               "Single File",
                                               "~/Desktop",
                                              "*.html")[0]
        lastSlashIndex = self.filePath.rfind('/')
        fileName = self.filePath[lastSlashIndex+1:]
        self.chosenFileLabel.setText(fileName)

    def addToCal(self):
        self.output = ws.addToCalendar(self.filePath, self.calendarIdTextBox.text())
        self.outputLabel.setText(self.output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWindow()
    sys.exit(app.exec_())
