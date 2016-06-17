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

import re
from PyQt4.QtCore import (QAbstractTableModel, QDataStream, QFile,
        QIODevice, QModelIndex, QRegExp, QSize, QString, QVariant, Qt,
        SIGNAL)
from PyQt4.QtGui import (QApplication, QColor, QComboBox, QLineEdit,
        QSpinBox, QStyle, QStyledItemDelegate, QTextDocument, QTextEdit)
import richtextlineedit


NAME, OWNER, COUNTRY, DESCRIPTION, TEU = range(5)

MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1


class Ship(object):

    def __init__(self, name, owner, country, teu=0, description=""):
        self.name = QString(name)
        self.owner = QString(owner)
        self.country = QString(country)
        self.teu = teu
        self.description = QString(description)


    def __hash__(self):
        return super(Ship, self).__hash__()


    def __lt__(self, other):
        r = QString.localeAwareCompare(self.name.toLower(),
                                       other.name.toLower())
        return True if r < 0 else False


    def __eq__(self, other):
        return 0 == QString.localeAwareCompare(self.name.toLower(),
                                               other.name.toLower())


class ShipContainer(object):

    def __init__(self, filename=QString()):
        self.filename = QString(filename)
        self.dirty = False
        self.ships = {}
        self.owners = set()
        self.countries = set()


    def ship(self, identity):
        return self.ships.get(identity)


    def addShip(self, ship):
        self.ships[id(ship)] = ship
        self.owners.add(unicode(ship.owner))
        self.countries.add(unicode(ship.country))
        self.dirty = True


    def removeShip(self, ship):
        del self.ships[id(ship)]
        del ship
        self.dirty = True


    def __len__(self):
        return len(self.ships)


    def __iter__(self):
        for ship in self.ships.values():
            yield ship

class ShipTableModel(QAbstractTableModel):
    re_tags = re.compile(r'<[^>]+>')

    def __init__(self, filename=QString()):
        super(ShipTableModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.ships = []
        self.owners = set()
        self.countries = set()


    def sortByName(self):
        self.ships = sorted(self.ships)
        self.reset()


    def sortByCountryOwner(self):
        self.ships = sorted(self.ships,
                            key=lambda x: (x.country, x.owner, x.name))
        self.reset()

    def sortByTEU(self):
        self.ships = sorted(self.ships,
                            key=lambda x: x.teu)
        self.reset()


    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
                QAbstractTableModel.flags(self, index)|
                Qt.ItemIsEditable)


    def data(self, index, role=Qt.DisplayRole):
        def data_value(column, ship, verbose=False, raw=False):
            if column == NAME:
                return QVariant(ship.name)
            elif column == OWNER:
                return QVariant(ship.owner)
            elif column == COUNTRY:
                return QVariant(ship.country)
            elif column == DESCRIPTION:
                desc = unicode(ship.description)
                if raw:
                    desc = self.re_tags.sub('', desc)

                return QVariant(QString(desc))
            elif column == TEU:
                if raw:
                    return QVariant(QString(str(ship.teu)))
                elif verbose:
                    return QVariant(QString("%L1 twenty foot equivalents").arg(ship.teu))
                else:
                    return QVariant(QString("%L1").arg(ship.teu))

        if (not index.isValid() or
            not (0 <= index.row() < len(self.ships))):
            return QVariant()
        ship = self.ships[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            return data_value(column, ship)
        elif role == Qt.ToolTipRole:
            return data_value(column, ship, verbose=True)
        elif role == Qt.UserRole:
            return data_value(column, ship, raw=True)
        elif role == Qt.TextAlignmentRole:
            if column == TEU:
                return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        elif role == Qt.TextColorRole and column == TEU:
            if ship.teu < 80000:
                return QVariant(QColor(Qt.black))
            elif ship.teu < 100000:
                return QVariant(QColor(Qt.darkBlue))
            elif ship.teu < 120000:
                return QVariant(QColor(Qt.blue))
            else:
                return QVariant(QColor(Qt.red))
        elif role == Qt.BackgroundColorRole:
            if ship.country in ("Bahamas", "Cyprus", "Denmark",
                    "France", "Germany", "Greece"):
                return QVariant(QColor(250, 230, 250))
            elif ship.country in ("Hong Kong", "Japan", "Taiwan"):
                return QVariant(QColor(250, 250, 230))
            elif ship.country in ("Marshall Islands",):
                return QVariant(QColor(230, 250, 250))
            else:
                return QVariant(QColor(210, 230, 230))

        return QVariant()


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == NAME:
                return QVariant("Name")
            elif section == OWNER:
                return QVariant("Owner")
            elif section == COUNTRY:
                return QVariant("Country")
            elif section == DESCRIPTION:
                return QVariant("Description")
            elif section == TEU:
                return QVariant("TEU")
        return QVariant(int(section + 1))


    def rowCount(self, index=QModelIndex()):
        return len(self.ships)


    def columnCount(self, index=QModelIndex()):
        return 5


    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.ships):
            ship = self.ships[index.row()]
            column = index.column()
            if column == NAME:
                ship.name = value.toString()
            elif column == OWNER:
                ship.owner = value.toString()
            elif column == COUNTRY:
                ship.country = value.toString()
            elif column == DESCRIPTION:
                ship.description = value.toString()
            elif column == TEU:
                value, ok = value.toInt()
                if ok:
                    ship.teu = value
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            return True
        return False


    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.ships.insert(position + row,
                              Ship(" Unknown", " Unknown", " Unknown"))
        self.endInsertRows()
        self.dirty = True
        return True


    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.ships = (self.ships[:position] +
                      self.ships[position + rows:])
        self.endRemoveRows()
        self.dirty = True
        return True


    def load(self):
        exception = None
        fh = None
        try:
            if self.filename.isEmpty():
                raise IOError, "no filename specified for loading"
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            magic = stream.readInt32()
            if magic != MAGIC_NUMBER:
                raise IOError, "unrecognized file type"
            fileVersion = stream.readInt16()
            if fileVersion != FILE_VERSION:
                raise IOError, "unrecognized file type version"
            self.ships = []
            while not stream.atEnd():
                name = QString()
                owner = QString()
                country = QString()
                description = QString()
                stream >> name >> owner >> country >> description
                teu = stream.readInt32()
                self.ships.append(Ship(name, owner, country, teu,
                                       description))
                self.owners.add(unicode(owner))
                self.countries.add(unicode(country))
            self.dirty = False
        except IOError, e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


    def save(self):
        exception = None
        fh = None
        try:
            if self.filename.isEmpty():
                raise IOError, "no filename specified for saving"
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            stream = QDataStream(fh)
            stream.writeInt32(MAGIC_NUMBER)
            stream.writeInt16(FILE_VERSION)
            stream.setVersion(QDataStream.Qt_4_1)
            for ship in self.ships:
                stream << ship.name << ship.owner << ship.country \
                       << ship.description
                stream.writeInt32(ship.teu)
            self.dirty = False
        except IOError, e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


class ShipDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(ShipDelegate, self).__init__(parent)


    def paint(self, painter, option, index):
        if index.column() == DESCRIPTION:
            text = index.model().data(index).toString()
            palette = QApplication.palette()
            document = QTextDocument()
            document.setDefaultFont(option.font)
            if option.state & QStyle.State_Selected:
                document.setHtml(QString("<font color=%1>%2</font>")
                        .arg(palette.highlightedText().color().name())
                        .arg(text))
            else:
                document.setHtml(text)
            color = (palette.highlight().color()
                     if option.state & QStyle.State_Selected
                     else QColor(index.model().data(index,
                                 Qt.BackgroundColorRole)))
            painter.save()
            painter.fillRect(option.rect, color)
            painter.translate(option.rect.x(), option.rect.y())
            document.drawContents(painter)
            painter.restore()
        else:
            QStyledItemDelegate.paint(self, painter, option, index)


    def sizeHint(self, option, index):
        fm = option.fontMetrics
        if index.column() == TEU:
            return QSize(fm.width("9,999,999"), fm.height())
        if index.column() == DESCRIPTION:
            text = index.model().data(index).toString()
            document = QTextDocument()
            document.setDefaultFont(option.font)
            document.setHtml(text)
            return QSize(document.idealWidth() + 5, fm.height())
        return QStyledItemDelegate.sizeHint(self, option, index)


    def createEditor(self, parent, option, index):
        if index.column() == TEU:
            spinbox = QSpinBox(parent)
            spinbox.setRange(0, 200000)
            spinbox.setSingleStep(1000)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        elif index.column() == OWNER:
            combobox = QComboBox(parent)
            combobox.addItems(sorted(index.model().owners))
            combobox.setEditable(True)
            return combobox
        elif index.column() == COUNTRY:
            combobox = QComboBox(parent)
            combobox.addItems(sorted(index.model().countries))
            combobox.setEditable(True)
            return combobox
        elif index.column() == NAME:
            editor = QLineEdit(parent)
            self.connect(editor, SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor
        elif index.column() == DESCRIPTION:
            editor = richtextlineedit.RichTextLineEdit(parent)
            self.connect(editor, SIGNAL("returnPressed()"),
                         self.commitAndCloseEditor)
            return editor
        else:
            return QStyledItemDelegate.createEditor(self, parent, option,
                                                    index)


    def commitAndCloseEditor(self):
        editor = self.sender()
        if isinstance(editor, (QTextEdit, QLineEdit)):
            self.emit(SIGNAL("commitData(QWidget*)"), editor)
            self.emit(SIGNAL("closeEditor(QWidget*)"), editor)


    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole).toString()
        if index.column() == TEU:
            value = text.replace(QRegExp("[., ]"), "").toInt()[0]
            editor.setValue(value)
        elif index.column() in (OWNER, COUNTRY):
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)
        elif index.column() == NAME:
            editor.setText(text)
        elif index.column() == DESCRIPTION:
            editor.setHtml(text)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)


    def setModelData(self, editor, model, index):
        data = None
        min_len = -1

        if index.column() == TEU:
            data = editor.value()
        elif index.column() in (OWNER, COUNTRY):
            data = editor.currentText()
            min_len = 3
        elif index.column() == NAME:
            data = editor.text()
            min_len = 3
        elif index.column() == DESCRIPTION:
            data = editor.toSimpleHtml()

        if data is None:
            QStyledItemDelegate.setModelData(self, editor, model, index)
        elif min_len > 0 and len(data) >= min_len:
            model.setData(index, QVariant(data))


def generateFakeShips():
    for name, owner, country, teu, description in (
(u"Emma M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"<b>W\u00E4rtsil\u00E4-Sulzer RTA96-C</b> main engine,"
 u"<font color=green>109,000 hp</font>"),
(u"MSC Pamela", u"MSC", u"Liberia", 90449,
 u"Draft <font color=green>15m</font>"),
(u"Colombo Express", u"Hapag-Lloyd", u"Germany", 93750,
 u"Main engine, <font color=green>93,500 hp</font>"),
(u"Houston Express", u"Norddeutsche Reederei", u"Germany", 95000,
 u"Features a <u>twisted leading edge full spade rudder</u>. "
 u"Sister of <i>Savannah Express</i>"),
(u"Savannah Express", u"Norddeutsche Reederei", u"Germany", 95000,
 u"Sister of <i>Houston Express</i>"),
(u"MSC Susanna", u"MSC", u"Liberia", 90449, ""),
(u"Eleonora M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"Captain <i>Hallam</i>"),
(u"Estelle M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
 u"Captain <i>Wells</i>"),
(u"Evelyn M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 151687,
  u"Captain <i>Byrne</i>"),
(u"Georg M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, ""),
(u"Gerd M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, ""),
(u"Gjertrud M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, ""),
(u"Grete M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, ""),
(u"Gudrun M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, ""),
(u"Gunvor M\u00E6rsk", u"M\u00E6rsk Line", u"Denmark", 97933, ""),
(u"CSCL Le Havre", u"Danaos Shipping", u"Cyprus", 107200, ""),
(u"CSCL Pusan", u"Danaos Shipping", u"Cyprus", 107200,
 u"Captain <i>Watts</i>"),
(u"Xin Los Angeles", u"China Shipping Container Lines (CSCL)",
 u"Hong Kong", 107200, ""),
(u"Xin Shanghai", u"China Shipping Container Lines (CSCL)", u"Hong Kong",
 107200, ""),
(u"Ever Chivalry", u"NSB Niederelbe", u"Marshall Islands", 90449, ""),
(u"Ever Conquest", u"NSB Niederelbe", u"Marshall Islands", 90449, ""),
(u"Ital Contessa", u"NSB Niederelbe", u"Marshall Islands", 90449, ""),
(u"Lt Cortesia", u"NSB Niederelbe", u"Marshall Islands", 90449, ""),
(u"OOCL Asia", u"OOCL", u"Hong Kong", 89097, ""),
(u"OOCL Atlanta", u"OOCL", u"Hong Kong", 89000, ""),
(u"OOCL Europe", u"OOCL", u"Hong Kong", 89097, ""),
(u"OOCL Hamburg", u"OOCL", u"Marshall Islands", 89097, ""),
(u"OOCL Long Beach", u"OOCL", u"Marshall Islands", 89097, ""),
(u"OOCL Ningbo", u"OOCL", u"Marshall Islands", 89097, ""),
(u"OOCL Shenzhen", u"OOCL", u"Hong Kong", 89097, ""),
(u"OOCL Tianjin", u"OOCL", u"Marshall Islands", 89097, ""),
(u"OOCL Tokyo", u"OOCL", u"Hong Kong", 89097, "")):
        yield Ship(name, owner, country, teu, description)
