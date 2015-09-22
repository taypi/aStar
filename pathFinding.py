#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QStyleFactory, QGridLayout,
    QPushButton, QApplication, QLineEdit, QFrame, QLabel, QVBoxLayout)
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
        self.show()

        print(left.getNeighbors(Land.begin))

class Land(QPushButton):
    colorMap = {'Edge': 'gray', 'Default': 'green', 'Wall': 'gray', 'Begin': 'red', 'Finish': 'blue'}
    flagBegin = False
    flagFinish = False
    finish = 0
    begin = 0

    def __init__(self, position, kind):
        super().__init__('')
        self.position = position
        self.setKind(kind)
        self.setFixedSize(30,30)
        self.clicked.connect(self.landClicked)

    def landClicked(self):
        if self.kind == "Begin":
            Land.flagBegin = True
            Land.flagFinish = False
        elif self.kind == "Finish":
            Land.flagFinish = True
            Land.flagBegin = False
        elif self.kind != "Edge":
            if Land.flagBegin:
                Land.begin.setKind("Default")
                self.setKind("Begin")
                Land.begin = self
                Land.flagBegin = False
            elif Land.flagFinish:
                Land.finish.setKind("Default")
                self.setKind("Finish")
                Land.finish = self
                Land.flagFinish = False
            elif self.kind == "Wall":
                self.setKind("Default")
            elif self.kind == "Default":
                self.setKind("Wall")
        print(self.position)

    def setKind(self,kind):
        self.kind = kind
        self.setStyleSheet("background-color:" + self.colorMap[kind])


class Grid(QFrame):

    #custo = [Horizonta, Vertical, Diagonal]
    cost = [1,1,1]

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.map = QGridLayout()
        self.map.setHorizontalSpacing(0)
        self.map.setVerticalSpacing(0)

        self.setLayout(self.map)

        height = 20
        width = 20

        positions = [(i,j) for i in range(width) for j in range(height)]

        for position in positions:
            if position[0] == width - 1 or position[0] == 0 or position[1] == height - 1 or position[1] == 0 :
                land = Land(position,'Edge')
            else:
                land = Land(position,'Default')
            self.map.addWidget(land, *position)

        Land.finish = self.getLand(width - 2 , height - 2)
        Land.finish.setKind("Finish")
        Land.begin = self.getLand(1,1)
        # self.getLand(0,0).setKind("Begin")
        Land.begin.setKind("Begin")
        # print(self.getNeighbors(land))

    def getLand(self, x, y):
        return self.map.itemAtPosition(x, y).widget()

    def getNeighbors(self,land):
        neighbors = []
        # x = land.position[0]-1
        # y = land.position[1]-1
        # a = self.getLand(x,y)
        # neighbors.append(a)
        neighbors.append(self.getLand(land.position[0]-1, land.position[1]-1))
        neighbors.append(self.getLand(land.position[0]-1, land.position[1]))
        neighbors.append(self.getLand(land.position[0]-1, land.position[1]+1))
        neighbors.append(self.getLand(land.position[0], land.position[1]-1))
        neighbors.append(self.getLand(land.position[0], land.position[1]+1))
        neighbors.append(self.getLand(land.position[0]+1, land.position[1]-1))
        neighbors.append(self.getLand(land.position[0]+1, land.position[1]))
        neighbors.append(self.getLand(land.position[0]+1, land.position[1]+1))
        return neighbors

    def setCost(self, cost):
        self.cost = cost
        print(self.cost)

class Settings(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        box = QVBoxLayout(self)
        lblH = QLabel('Horizontal')
        self.costH = QLineEdit()
        lblV = QLabel('Vertical')
        self.costV = QLineEdit()
        lblD = QLabel('Diagonal')
        self.costD = QLineEdit()
        box.addWidget(lblH)
        box.addWidget(self.costH)
        box.addWidget(lblV)
        box.addWidget(self.costV)
        box.addWidget(lblD)
        box.addWidget(self.costD)

        self.btnSend = QPushButton('Send', self)
        self.btnSend.clicked.connect(self.sendClicked)
        box.addWidget(self.btnSend)

    def sendClicked(self):
        value = [self.costH.text(), self.costV.text(), self.costD.text()]
        Grid().setCost(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    draw = PathFinder()
    sys.exit(app.exec_())

