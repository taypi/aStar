#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QStyleFactory, QGridLayout,
    QPushButton, QApplication, QFrame)
from PyQt5.QtCore import Qt

class PathFinder(QWidget):
    def __init__(self):
        super().__init__()
        box = QHBoxLayout(self)

        left = Grid()
        left.setFrameShape(QFrame.StyledPanel)
 
        right = Settings()
        right.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        box.addWidget(splitter)

        self.setLayout(box)
        self.setWindowTitle('Path Finder')
        self.showFullScreen()
        self.show()
        
class Grid(QFrame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.map = QGridLayout()
        self.map.setHorizontalSpacing(0)
        self.map.setVerticalSpacing(0)

        self.setLayout(self.map)

        positions = [(i,j) for i in range(20) for j in range(20)]

        for position in positions:
            land = QPushButton('')
            land.setFixedSize(30,30)
            self.map.addWidget(land, *position)
            if (position == (0,0)):
                self.begin = land
                self.begin.flag = False
                land.cat = 0
                land.setStyleSheet("background-color: red")
            elif (position == (9,9)):
                self.finish = land
                self.finish.flag = False
                land.cat = 1
                land.setStyleSheet("background-color: blue")
            else:
                land.cat = 2
                land.setStyleSheet("background-color: green")
            land.cost = 1
            land.clicked.connect(self.landClicked)

    def landClicked(self):
        land = self.sender()
        if (land.cat == 2):
            if (self.begin.flag):
                land.setStyleSheet("background-color: red")
                self.begin.setStyleSheet("background-color: green")
                self.begin.cat = 2
                self.begin = land
                self.begin.cat = 0
                self.begin.flag = False
            elif (self.finish.flag):
                land.setStyleSheet("background-color: blue")
                self.finish.setStyleSheet("background-color: green")
                self.finish.cat = 2
                self.finish = land
                self.finish.cat = 1
                self.finish.flag = False
            elif land.cost < 10000:
                land.setStyleSheet("background-color: gray")
                land.cost = 10000
            else:
                land.setStyleSheet("background-color: green")
                land.cost = 1
        else:
            if (land.cat == 0):
                self.begin.flag = True
            elif (land.cat == 1):
                self.finish.flag = True
        idx = self.map.indexOf(land)
        location = self.map.getItemPosition(idx)
        print (location[:2], "-", land.cost)
        print (self.getNeighbors(land), "-", land)

    def getNeighbors(self, land):
        neighbors = []
        location = self.map.getItemPosition(self.map.indexOf(land))
        
        neighbors.append(land)

        return neighbors

class Settings(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btnSend = QPushButton('Send', self)
        btnSend.move(300,300)      

if __name__ == '__main__':
    app = QApplication(sys.argv)
    draw = PathFinder()
    sys.exit(app.exec_())        

