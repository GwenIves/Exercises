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
from PyQt4.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData,
        QPoint, QSize, QString, Qt)
from PyQt4.QtGui import (QApplication, QColor, QDialog, QDrag,
        QFontMetricsF, QGridLayout, QIcon, QLineEdit, QListWidget,
        QListWidgetItem, QPainter, QWidget)

def set_drop_action(event):
    if QApplication.keyboardModifiers() & Qt.ControlModifier:
        event.setDropAction(Qt.CopyAction)
    else:
        event.setDropAction(Qt.MoveAction)

class DropLineEdit(QLineEdit):

    def __init__(self, parent=None):
        super(DropLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)


    @staticmethod
    def dragEnterEvent(event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()


    @staticmethod
    def dragMoveEvent(event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            set_drop_action(event)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = QString()
            stream >> text
            self.setText(text)
            set_drop_action(event)
            event.accept()
        else:
            event.ignore()


class DnDListWidget(QListWidget):

    def __init__(self, parent=None):
        super(DnDListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)


    @staticmethod
    def dragEnterEvent(event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()


    @staticmethod
    def dragMoveEvent(event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            set_drop_action(event)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = QString()
            icon = QIcon()
            stream >> text >> icon
            item = QListWidgetItem(text, self)
            item.setIcon(icon)
            set_drop_action(event)
            event.accept()
        else:
            event.ignore()


    def startDrag(self, _):
        item = self.currentItem()
        icon = item.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << item.text() << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        if drag.exec_(Qt.MoveAction|Qt.CopyAction) == Qt.MoveAction:
            self.takeItem(self.row(item))


class DnDWidget(QWidget):

    def __init__(self, text, icon=QIcon(), parent=None):
        super(DnDWidget, self).__init__(parent)
        self.default_text = text
        self.setAcceptDrops(True)
        self.text = QString(text)
        self.icon = icon


    def minimumSizeHint(self):
        fm = QFontMetricsF(self.font())
        if self.icon.isNull():
            return QSize(fm.width(self.text), fm.height() * 1.5)
        return QSize(34 + fm.width(self.text), max(34, fm.height() * 1.5))


    def paintEvent(self, _):
        height = QFontMetricsF(self.font()).height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.fillRect(self.rect(), QColor(Qt.yellow).light())
        if self.icon.isNull():
            painter.drawText(10, height, self.text)
        else:
            pixmap = self.icon.pixmap(24, 24)
            painter.drawPixmap(0, 5, pixmap)
            painter.drawText(34, height,
                             self.text + " (Drag to or from me!)")


    @staticmethod
    def dragEnterEvent(event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()


    @staticmethod
    def dragMoveEvent(event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            set_drop_action(event)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            self.text = QString()
            self.icon = QIcon()
            stream >> self.text >> self.icon
            set_drop_action(event)
            event.accept()
            self.updateGeometry()
            self.update()
        else:
            event.ignore()


    def mouseMoveEvent(self, event):
        self.startDrag()
        QWidget.mouseMoveEvent(self, event)


    def startDrag(self):
        icon = self.icon
        if icon.isNull():
            return
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << self.text << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        if drag.exec_(Qt.MoveAction|Qt.CopyAction) == Qt.MoveAction:
            self.text = QString(self.default_text)
            self.icon = QIcon()
            self.updateGeometry()
            self.update()


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        dndListWidget = DnDListWidget()
        path = os.path.dirname(__file__)
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png"):
                item = QListWidgetItem(image.split(".")[0].capitalize())
                item.setIcon(QIcon(os.path.join(path,
                                   "images/{0}".format(image))))
                dndListWidget.addItem(item)
        dndIconListWidget = DnDListWidget()
        dndIconListWidget.setViewMode(QListWidget.IconMode)
        dndWidget = DnDWidget("Drag to me!")
        dropLineEdit = DropLineEdit()

        layout = QGridLayout()
        layout.addWidget(dndListWidget, 0, 0)
        layout.addWidget(dndIconListWidget, 0, 1)
        layout.addWidget(dndWidget, 1, 0)
        layout.addWidget(dropLineEdit, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle("Custom Drag and Drop")


def main():
    app = QApplication(sys.argv)
    form = Form()
    form.setWindowFlags(Qt.Window)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
