#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,
    QPushButton, QApplication)


class Grid(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        positions = [(i,j) for i in range(10) for j in range(10)]

        for position in positions:
            button = QPushButton('')
            button.setFixedSize(30,30)
            grid.addWidget(button, *position)

        self.move(300, 150)
        self.setWindowTitle('Grid')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Grid()
    sys.exit(app.exec_())