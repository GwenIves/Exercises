#!/usr/bin/env python

from PyQt4.QtCore import pyqtSignature, QDateTime
from PyQt4.QtGui import (QApplication, QDialog, QDialogButtonBox)
import ui_ticket_order

class TicketOrder(QDialog, ui_ticket_order.Ui_Ticket_Order):

    def __init__(self, parent=None):
        super(TicketOrder, self).__init__(parent)
        self.setupUi(self)

        self.ok = self.buttonBox.button(QDialogButtonBox.Ok)
        self.ok.setEnabled(False)

        self.when.setMinimumDateTime(QDateTime.currentDateTime())

    def result(self):
        return (
            unicode(self.customer.text()),
            self.when.dateTime().toPyDateTime(),
            self.price.value(),
            self.quantity.value()
        )

    @pyqtSignature("QString")
    def on_customer_textChanged(self, _):
        self.update_UI()

    @pyqtSignature("double")
    def on_price_valueChanged(self, _):
        self.update_UI()

    @pyqtSignature("int")
    def on_quantity_valueChanged(self, _):
        self.update_UI()

    def update_UI(self):
        amount = self.price.value() * self.quantity.value()

        self.amount.setText("$ {:.2f}".format(amount))
        self.ok.setEnabled(len(self.customer.text()) != 0)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = TicketOrder()

    if form.exec_():
        print form.result()
    else:
        print "Cancelled"
