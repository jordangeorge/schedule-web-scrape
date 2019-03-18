import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

import gui_funcs

class FirstWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "MyUK Schedule Google Calendar Importer"
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # set background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.filePath = ""
        cursor = QCursor(Qt.PointingHandCursor)

        chooseFileButton = QPushButton("Choose file", self)
        chooseFileButton.setCursor(cursor)
        chooseFileButton.clicked.connect(self.singleBrowse)

        self.chosenFileLabel = QLabel("", self)

        calendarIdLabel = QLabel("Calendar ID:", self)

        self.calendarIdTextBox = QLineEdit(self)
        self.calendarIdTextBox.setText("primary")

        addToCalButton = QPushButton("Add to calendar", self)
        addToCalButton.clicked.connect(self.addToCal)
        addToCalButton.setCursor(cursor)
        addToCalButton.setStyleSheet("QPushButton { \
                                    background-color: #4285F4; \
                                    color: #FFF; \
                                    font: 15pt Arial; \
                                    padding: 6px; \
                                    border: none; \
                                    border-radius: 10px; \
                                    }")

        self.output = ""
        self.outputLabel = QLabel(self.output, self)

        # self.deleteButton = QPushButton("Delete most recently added courses", self)
        # self.deleteButton.clicked.connect(self.delete)
        # self.deleteButton.setCursor(cursor)
        # self.deleteButton.setStyleSheet("QPushButton { \
        #                                 background-color: #EA4235; \
        #                                 color: #FFF; \
        #                                 font: 15pt Arial; \
        #                                 padding: 6px; \
        #                                 border: none; \
        #                                 border-radius: 10px; \
        #                                 }")

        numberLabelStyling = "QLabel { \
                                color: #000; \
                                font: 15pt Arial; \
                                }"
        oneLabel = QLabel("1.", self)
        oneLabel.setStyleSheet(numberLabelStyling)
        twoLabel = QLabel("2.", self)
        twoLabel.setStyleSheet(numberLabelStyling)
        threeLabel = QLabel("3.", self)
        threeLabel.setStyleSheet(numberLabelStyling)

        layout = QGridLayout()
        layout.addWidget(oneLabel, 0, 0)
        layout.addWidget(chooseFileButton, 0, 1)
        layout.addWidget(self.chosenFileLabel, 0, 2)
        layout.addWidget(twoLabel, 1, 0)
        layout.addWidget(calendarIdLabel, 1, 1)
        layout.addWidget(self.calendarIdTextBox, 1, 2)
        layout.addWidget(threeLabel, 2, 0)
        layout.addWidget(addToCalButton, 2, 1)
        layout.addWidget(self.outputLabel, 3, 1)
        # layout.addWidget(self.deleteButton, 4, 2)
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
        if self.filePath:
            self.output = gui_funcs.addToCalendar(self.filePath, self.calendarIdTextBox.text())
            self.outputLabel.setText(self.output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWindow()
    sys.exit(app.exec_())
