#!/bin/env python3

import sys

from PyQt4.QtGui import (
    QDialog, QDoubleSpinBox, QComboBox, QLabel,
    QFormLayout, QApplication
)

class Form(QDialog):
    def __init__(self, parent=None):
        def make_spin_box(decimals, end, step, value):
            box = QDoubleSpinBox()
            box.setDecimals(decimals)
            box.setSingleStep(step)
            box.setMaximum(end)
            box.setValue(value)

            return box

        super(Form, self).__init__(parent)

        self.principal = make_spin_box(0, 1000000, 100, 100)
        self.principal.setPrefix("$ ")

        self.rate = make_spin_box(2, 100, 0.1, 3.00)
        self.rate.setSuffix(" %")

        self.years = QComboBox()
        for year in range(41):
            self.years.addItem("{} year{}".format(year, "" if year == 1 else "s"))

        self.amount = QLabel()

        self.principal.valueChanged.connect(self.update_UI)
        self.rate.valueChanged.connect(self.update_UI)
        self.years.currentIndexChanged.connect(self.update_UI)

        form = QFormLayout()
        form.addRow("Principal", self.principal)
        form.addRow("Rate", self.rate)
        form.addRow("Years", self.years)
        form.addRow("Amount", self.amount)

        self.setLayout(form)
        self.setWindowTitle("Interest")

        self.update_UI()

    def update_UI(self):
        principal = self.principal.value()
        rate = self.rate.value()
        years = self.years.currentIndex()

        amount = principal * (1 + rate / 100.0) ** years

        self.amount.setText("$ {:.2f}".format(amount))


def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
