#!/usr/bin/env python

import sys

from PyQt4.QtCore import (QSize, Qt, QRectF)
from PyQt4.QtGui import (QApplication, QSizePolicy, QWidget, QPainter, QBrush)

class CounterWidget(QWidget):
    STATES = 3

    def __init__(self, size=3, parent=None):
        super(CounterWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setMinimumSize(self.minimumSizeHint())

        self.size = size
        self.active = (0, 0)
        self.grid = []

        for _ in range(self.size):
            self.grid.append([0] * self.size)

    @staticmethod
    def minimumSizeHint():
        return QSize(100, 100)

    sizeHint = minimumSizeHint

    def inc_cell(self, x, y):
        self.grid[x][y] += 1

        if self.grid[x][y] >= self.STATES:
            self.grid[x][y] = 0

    def move_active(self, dx, dy):
        x, y = self.active
        x = self.validate_cell(x + dx)
        y = self.validate_cell(y + dy)

        self.active = (x, y)

    def validate_cell(self, index):
        return min(max(0, index), self.size - 1)

    def mousePressEvent(self, event):
        cell_size_x = self.width() / self.size
        cell_x = event.x() / cell_size_x
        cell_size_y = self.height() / self.size
        cell_y = event.y() / cell_size_y

        cell_x = self.validate_cell(cell_x)
        cell_y = self.validate_cell(cell_y)

        self.inc_cell(cell_x, cell_y)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Space:
            self.inc_cell(*self.active)
            self.update()
        elif event.key() == Qt.Key_Right:
            self.move_active(1, 0)
            self.update()
        elif event.key() == Qt.Key_Left:
            self.move_active(-1, 0)
            self.update()
        elif event.key() == Qt.Key_Up:
            self.move_active(0, -1)
            self.update()
        elif event.key() == Qt.Key_Down:
            self.move_active(0, 1)
            self.update()
        else:
            super(CounterWidget, self).keyPressEvent(event)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QBrush(Qt.gray))

        width = self.width()
        height = self.height()

        step_x = self.width() / self.size
        step_y = self.height() / self.size

        painter.setPen(Qt.black)

        for step in range(1, self.size):
            painter.drawLine(0, step * step_y, width, step * step_y)
            painter.drawLine(step * step_x, 0, step * step_x, height)

        for x in range(self.size):
            for y in range(self.size):
                painter.save()

                rect = QRectF(
                    x * step_x,
                    y * step_y,
                    step_x,
                    step_y
                )
                rect.adjust(1.0, 1.0, -1.0, -1.0)

                if (x, y) == self.active:
                    painter.setPen(Qt.blue)
                    painter.drawRect(rect)

                rect.adjust(3.0, 3.0, -3.0, -3.0)
                painter.setPen(Qt.black)

                state = self.grid[x][y]

                if state == 0:
                    pass
                elif state == 1:
                    painter.setBrush(Qt.yellow)
                    painter.drawEllipse(rect)
                elif state == 2:
                    painter.setBrush(Qt.red)
                    painter.drawEllipse(rect)

                painter.restore()

def main():
    app = QApplication(sys.argv)

    form = CounterWidget()
    form.setWindowTitle("Counter")
    form.resize(500, 500)

    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
