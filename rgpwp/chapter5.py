#!/bin/env python3

import sys
import pprint

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import (
    QDialog, QApplication, QGridLayout,
    QListWidget, QPushButton, QInputDialog
)

class Form(QDialog):
    accepted = pyqtSignal(list)

    def __init__(self, title, stringlist, parent=None):
        super(Form, self).__init__(parent)

        self.stringlist = stringlist[:]

        self.strings = QListWidget()
        self.strings.insertItems(0, stringlist)

        if stringlist:
            self.strings.setCurrentRow(0)

        self.add = QPushButton("&Add...")
        self.edit = QPushButton("&Edit...")
        self.remove = QPushButton("&Remove...")
        self.up = QPushButton("&Up")
        self.down = QPushButton("&Down")
        self.sort = QPushButton("&Sort")
        self.close = QPushButton("&Close")

        layout = QGridLayout()
        layout.addWidget(self.strings, 0, 0, 7, 1)
        layout.addWidget(self.add, 0, 1)
        layout.addWidget(self.edit, 1, 1)
        layout.addWidget(self.remove, 2, 1)
        layout.addWidget(self.up, 3, 1)
        layout.addWidget(self.down, 4, 1)
        layout.addWidget(self.sort, 5, 1)
        layout.addWidget(self.close, 6, 1)

        self.setLayout(layout)
        self.setWindowTitle(title)

        self.add.clicked.connect(self.add_item)
        self.edit.clicked.connect(self.edit_item)
        self.remove.clicked.connect(self.remove_item)
        self.up.clicked.connect(self.move_up)
        self.down.clicked.connect(self.move_down)
        self.sort.clicked.connect(self.strings.sortItems)
        self.close.clicked.connect(self.accept)

        self.reject = self.accept

    def accept(self):
        self.stringlist = []

        for i in range(self.strings.count()):
            self.stringlist.append(self.strings.item(i).text())

        self.accepted.emit(self.stringlist)
        super(Form, self).accept()

    def move_down(self):
        row = self.strings.currentRow()

        if row in (-1, self.strings.count() - 1):
            return

        item = self.strings.takeItem(row)

        row += 1
        self.strings.insertItem(row, item)
        self.strings.setCurrentRow(row)

    def move_up(self):
        row = self.strings.currentRow()

        if row in (-1, 0):
            return

        item = self.strings.takeItem(row)

        row -= 1
        self.strings.insertItem(row, item)
        self.strings.setCurrentRow(row)

    def remove_item(self):
        row = self.strings.currentRow()

        if row != -1:
            self.strings.takeItem(row)

    def edit_item(self):
        row = self.strings.currentRow()

        if row == -1:
            return

        d = QInputDialog()

        if d.exec_():
            text = d.textValue()

            if text:
                self.strings.item(row).setText(text)

    def add_item(self):
        d = QInputDialog()

        if d.exec_():
            text = d.textValue()

            if text:
                row = self.strings.currentRow()
                self.strings.insertItem(row + 1, text)

def main():
    fruits = [
        "Banana", "Apple", "Elderberry", "Clementine", "Fig",
        "Guava", "Mango", "Honeydew Melon", "Date", "Watermelon",
        "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi", "Lemon",
        "Nectarine", "Plum", "Raspberry", "Strawberry", "Orange"
    ]

    def print_from_signal(strings):
        print(strings)

    app = QApplication(sys.argv)
    form = Form("Edit Fruit List", fruits)
    form.accepted.connect(print_from_signal)
    form.exec_()

    pprint.pprint(form.stringlist)

if __name__ == '__main__':
    main()
