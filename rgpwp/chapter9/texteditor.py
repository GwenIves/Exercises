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

import sys
from PyQt4.QtCore import (QFile, QFileInfo, QSettings,
        QString, QStringList, QTimer, QVariant, SIGNAL)
from PyQt4.QtGui import (QAction, QApplication, QFileDialog, QIcon,
        QKeySequence, QMainWindow, QMessageBox, QTextEdit, QTabWidget,
        QShortcut)
import textedit
import qrc_resources

__version__ = "1.0.0"

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        fileNewAction = self.createAction("&New", self.fileNew,
                QKeySequence.New, "filenew", "Create a text file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing text file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save the text")
        fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the text using a new filename")
        fileSaveAllAction = self.createAction("Save A&ll",
                self.fileSaveAll, "filesave",
                tip="Save all the files")
        fileCloseAction = self.createAction("&Close", self.closeTab,
                "Ctrl+W")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
        editCopyAction = self.createAction("&Copy", self.editCopy,
                QKeySequence.Copy, "editcopy",
                "Copy text to the clipboard")
        editCutAction = self.createAction("Cu&t", self.editCut,
                QKeySequence.Cut, "editcut",
                "Cut text to the clipboard")
        editPasteAction = self.createAction("&Paste", self.editPaste,
                QKeySequence.Paste, "editpaste",
                "Paste in the clipboard's text")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, fileSaveAllAction,
                None, fileCloseAction, fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editCopyAction, editCutAction,
                                   editPasteAction))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        self.addActions(editToolbar, (editCopyAction, editCutAction,
                                      editPasteAction))

        QShortcut(QKeySequence.PreviousChild, self, self.previousTab)
        QShortcut(QKeySequence.NextChild, self, self.nextTab)

        settings = QSettings()
        self.restoreGeometry(
                settings.value("MainWindow/Geometry").toByteArray())
        self.restoreState(
                settings.value("MainWindow/State").toByteArray())

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.setWindowTitle("Text Editor")
        QTimer.singleShot(0, self.loadFiles)


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    @staticmethod
    def addActions(target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
        failures = []
        for i in range(self.tabs.count()):
            textEdit = self.tabs.widget(i)

            if textEdit.isModified():
                try:
                    textEdit.save()
                except IOError, e:
                    failures.append(unicode(e))
        if (failures and
            QMessageBox.warning(self, "Text Editor -- Save Error",
                    "Failed to save{0}\nQuit anyway?".format(
                    "\n\t".join(failures)),
                    QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.No):
            event.ignore()
            return
        settings = QSettings()
        settings.setValue("MainWindow/Geometry",
                          QVariant(self.saveGeometry()))
        settings.setValue("MainWindow/State",
                          QVariant(self.saveState()))
        files = QStringList()

        while self.tabs.count() > 0:
            textEdit = self.tabs.widget(0)
            self.tabs.removeTab(0)

            if not textEdit.filename.startsWith("Unnamed"):
                files.append(textEdit.filename)

            textEdit.close()
        settings.setValue("CurrentFiles", QVariant(files))


    def loadFiles(self):
        if len(sys.argv) > 1:
            for filename in sys.argv[1:11]:
                filename = QString(filename)
                if QFileInfo(filename).isFile():
                    self.loadFile(filename)
                    QApplication.processEvents()
        else:
            settings = QSettings()
            files = settings.value("CurrentFiles").toStringList()
            for filename in files:
                filename = QString(filename)
                if QFile.exists(filename):
                    self.loadFile(filename)
                    QApplication.processEvents()


    def nextTab(self):
        index = self.tabs.currentIndex() + 1
        if index >= self.tabs.count():
            index = 0

        self.tabs.setCurrentIndex(index)


    def previousTab(self):
        index = self.tabs.currentIndex() - 1
        if index <= 0:
            index = 0

        self.tabs.setCurrentIndex(index)


    def fileNew(self):
        textEdit = textedit.TextEdit()
        self.tabs.addTab(textEdit, textEdit.title)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)


    def fileOpen(self):
        filename = QFileDialog.getOpenFileName(self,
                "Text Editor -- Open File")
        if not filename.isEmpty():
            for i in range(self.tabs.count()):
                textEdit = self.tabs.widget(i)

                if textEdit.filename == filename:
                    self.tabs.setCurrentIndex(i)
                    break
            else:
                self.loadFile(filename)


    def loadFile(self, filename):
        textEdit = textedit.TextEdit(filename)
        try:
            textEdit.load()
        except (IOError, OSError), e:
            QMessageBox.warning(self, "Text Editor -- Load Error",
                    "Failed to load {0}: {1}".format(filename, e))
            textEdit.close()
            del textEdit
        else:
            self.tabs.addTab(textEdit, textEdit.title)
            self.tabs.setCurrentIndex(self.tabs.count() - 1)


    def fileSave(self):
        textEdit = self.tabs.widget(self.tabs.currentIndex())
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return True
        try:
            textEdit.save()
            return True
        except (IOError, OSError), e:
            QMessageBox.warning(self, "Text Editor -- Save Error",
                    "Failed to save {0}: {1}".format(textEdit.filename, e))
            return False


    def fileSaveAs(self):
        textEdit = self.tabs.widget(self.tabs.currentIndex())
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        filename = QFileDialog.getSaveFileName(self,
                        "Text Editor -- Save File As",
                        textEdit.filename, "Text files (*.txt *.*)")
        if not filename.isEmpty():
            textEdit.filename = filename
            return self.fileSave()
        return True


    def fileSaveAll(self):
        errors = []
        for i in range(self.tabs.count()):
            textEdit = self.tabs.widget(i)

            if textEdit.isModified():
                try:
                    textEdit.save()
                except (IOError, OSError), e:
                    errors.append("{0}: {1}".format(textEdit.filename, e))
        if errors:
            QMessageBox.warning(self,
                    "Text Editor -- Save All Error",
                    "Failed to save\n{0}".format("\n".join(errors)))


    def closeTab(self):
        index = self.tabs.currentIndex()

        if index != -1:
            tab = self.tabs.widget(index)
            self.tabs.removeTab(index)
            tab.close()


    def editCopy(self):
        textEdit = self.tabs.widget(self.tabs.currentIndex())
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if not text.isEmpty():
            clipboard = QApplication.clipboard()
            clipboard.setText(text)


    def editCut(self):
        textEdit = self.tabs.widget(self.tabs.currentIndex())
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        cursor = textEdit.textCursor()
        text = cursor.selectedText()
        if not text.isEmpty():
            cursor.removeSelectedText()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)


    def editPaste(self):
        textEdit = self.tabs.widget(self.tabs.currentIndex())
        if textEdit is None or not isinstance(textEdit, QTextEdit):
            return
        clipboard = QApplication.clipboard()
        textEdit.insertPlainText(clipboard.text())


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(":/icon.png"))
app.setOrganizationName("Qtrac Ltd.")
app.setOrganizationDomain("qtrac.eu")
app.setApplicationName("Text Editor")
form = MainWindow()
form.show()
app.exec_()
