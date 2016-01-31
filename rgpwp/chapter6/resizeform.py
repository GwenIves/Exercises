#!/usr/bin/env python

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (
    QApplication, QDialog, QSpinBox,
    QDialogButtonBox, QLabel, QFormLayout
)

class ResizeForm(QDialog):

    def __init__(self, width, height, parent=None):
        super(ResizeForm, self).__init__(parent)

        def make_spin(val):
            if val < 4:
                val = 4

            spin = QSpinBox()
            spin.setAlignment(Qt.AlignRight)
            spin.setRange(4, 4 * val)
            spin.setValue(val)

            return spin

        def add_row(layout, text, widget):
            label = QLabel(text)
            label.setBuddy(widget)
            layout.addRow(label, widget)

        self.width = make_spin(width)
        self.height = make_spin(height)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        layout = QFormLayout()

        add_row(layout, "&Width:", self.width)
        add_row(layout, "&Height:", self.height)
        layout.addRow(buttons)

        self.setLayout(layout)

        self.setWindowTitle("{0} - Resize".format(
            QApplication.applicationName()))

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def result(self):
        return self.width.value(), self.height.value()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = ResizeForm(200, 200)

    if form.exec_():
        print form.result()
    else:
        print "Rejected"
