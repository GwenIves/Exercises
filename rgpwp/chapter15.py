#!/usr/bin/env python
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import os
import sys
from PyQt4.QtCore import (QFile,
        QString, QVariant, Qt, SIGNAL)
from PyQt4.QtGui import (QApplication, QCursor, QDialog,
        QMessageBox,
        QTableView,
        QVBoxLayout, QDialogButtonBox, QMenu)
from PyQt4.QtSql import (QSqlDatabase, QSqlQuery,
        QSqlTableModel)

(ID, CATEGORY, SHORT_DESC, LONG_DESC) = range(4)

def createFakeData():
    import random

    query = QSqlQuery()
    query.exec_("DROP TABLE reference")
    QApplication.processEvents()

    query.exec_("""CREATE TABLE reference (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                category VARCHAR(30) NOT NULL,
                short_desc VARCHAR(20) NOT NULL,
                long_desc  VARCHAR(80))""")
    QApplication.processEvents()

    query.exec_("INSERT INTO reference (category, short_desc, long_desc) "
                "VALUES ('Actions', 'Wait', 'Wait for information')")
    query.exec_("INSERT INTO reference (category, short_desc, long_desc) "
                "VALUES ('Actions', 'Escalate', 'Send to supervisor')")
    query.exec_("INSERT INTO reference (category, short_desc, long_desc) "
                "VALUES ('Actions', 'Progress', 'Progress to next stage')")
    QApplication.processEvents()

class ReferenceDataDlg(QDialog):

    def __init__(self, table, title, parent=None):
        super(ReferenceDataDlg, self).__init__(parent)

        self.model = QSqlTableModel(self)
        self.model.setTable(table)
        self.model.setSort(SHORT_DESC, Qt.AscendingOrder)
        self.model.setHeaderData(ID, Qt.Horizontal, QVariant("ID"))
        self.model.setHeaderData(CATEGORY, Qt.Horizontal, QVariant("Category"))
        self.model.setHeaderData(SHORT_DESC, Qt.Horizontal, QVariant("Short description"))
        self.model.setHeaderData(LONG_DESC, Qt.Horizontal, QVariant("Long description"))
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setColumnHidden(ID, True)
        self.view.resizeColumnsToContents()
        self.view.horizontalHeader().setStretchLastSection(True)

        buttonBox = QDialogButtonBox()
        addButton = buttonBox.addButton("&Add", QDialogButtonBox.ActionRole)
        deleteButton = buttonBox.addButton("&Delete", QDialogButtonBox.ActionRole)
        sortButton = buttonBox.addButton("&Sort", QDialogButtonBox.ActionRole)
        closeButton = buttonBox.addButton(QDialogButtonBox.Close)

        sortMenu = QMenu(self)
        sort_by_cat = sortMenu.addAction("Sort by category")
        sort_by_desc = sortMenu.addAction("Sort by description")
        sortButton.setMenu(sortMenu)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(addButton, SIGNAL("clicked()"), self.addRecord)
        self.connect(deleteButton, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(closeButton, SIGNAL("clicked()"), self.accept)
        self.connect(sort_by_cat, SIGNAL("triggered()"), lambda: self.sort(CATEGORY))
        self.connect(sort_by_desc, SIGNAL("triggered()"), lambda: self.sort(SHORT_DESC))

        self.setWindowTitle(title)

    def sort(self, column, order=Qt.AscendingOrder):
        self.model.setSort(column, order)
        self.model.select()

    def addRecord(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, CATEGORY)
        self.view.setCurrentIndex(index)
        self.view.edit(index)


    def deleteRecord(self):
        index = self.view.currentIndex()
        if not index.isValid():
            return
        record = self.model.record(index.row())
        if QMessageBox.question(
                self,
                QString("Delete reference"),
                QString("Delete %1 - %2").arg(record.value(CATEGORY).toString()).arg(record.value(SHORT_DESC).toString()),
                QMessageBox.Yes|QMessageBox.No
        ) == QMessageBox.Yes:
            self.model.removeRow(index.row())
            self.model.submitAll()

def main():
    app = QApplication(sys.argv)

    filename = os.path.join(os.path.dirname(__file__), "reference.db")
    create = not QFile.exists(filename)
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "Reference",
            QString("Database Error: %1")
            .arg(db.lastError().text()))
        sys.exit(1)

    if create:
        app.setOverrideCursor(QCursor(Qt.WaitCursor))
        createFakeData()

    form = ReferenceDataDlg("reference", "Reference")
    form.resize(400, 300)
    form.show()

    if create:
        app.restoreOverrideCursor()

    app.exec_()
    del form
    del db

main()
