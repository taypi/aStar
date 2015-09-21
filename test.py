#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,
    QPushButton, QApplication)


class Grid(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.map = QGridLayout()
        self.map.setHorizontalSpacing(0)
        self.map.setVerticalSpacing(0)

        self.setLayout(self.map)

        positions = [(i,j) for i in range(10) for j in range(10)]

        for position in positions:
            land = QPushButton('')
            land.setFixedSize(30,30)
            self.map.addWidget(land, *position)
            land.cost = 1
            land.setStyleSheet("background-color: green")
            land.clicked.connect(self.landClicked)

        self.setWindowTitle('Grid')
        self.show()

    def landClicked(self):
        land = self.sender()
        if land.cost < 10000:
            land.setStyleSheet("background-color: gray")
            land.cost = 10000
        else:
            land.setStyleSheet("background-color: green")
            land.cost = 1
        idx = self.map.indexOf(land)
        location = self.map.getItemPosition(idx)
        print (location[:2], "-", land.cost)
        print (self.neighbors(land), "-", land)

    def neighbors(self, land):
        neighbors = []
        location = self.map.getItemPosition(self.map.indexOf(land))
        neighbors.append(land)
        return neighbors



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Grid()
    sys.exit(app.exec_())