#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QStyleFactory, QGridLayout,
    QPushButton, QApplication, QLineEdit, QFrame, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt

from heapq import *

class PathFinder(QWidget):
    def __init__(self):
        super().__init__()
        box = QHBoxLayout(self)

        grid = Grid()
        grid.setFrameShape(QFrame.StyledPanel)

        right = Settings()
        right.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(grid)
        splitter.addWidget(right)

        box.addWidget(splitter)
        self.setLayout(box)
        self.setWindowTitle('Path Finder')
        self.show()

        came_from, cost_so_far = self.aStar(grid)
        # print("Cost so far: ", cost_so_far)
        # print(grid.getNeighbors(grid.begin))

    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def aStar(self, grid):
        frontier = []
        heappush(frontier,(0, grid.begin))
        came_from = {}
        cost_so_far = {}
        cost_so_far[grid.begin] = 0

        while frontier:
            current = heappop(frontier)

            if current[1] == grid.finish:
                break

            for next in grid.getNeighbors(current[1]):
                new_cost = cost_so_far[current[1]] + grid.getCost(current[1], next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    next.setText(str(new_cost))
                    priority = new_cost + PathFinder.heuristic(grid.finish.position, next.position)
                    heappush(frontier,(priority, next))
                    came_from[next] = current[1]
                    next.setColor("DarkCyan")
                    current[1].setColor("DarkSlateGray")
        return came_from, cost_so_far

class Land(QPushButton):
    colorMap = {'Edge': ('gray', 9999999), 'Default': ('green', 1), 'Wall': ('gray', 9999999), 'Begin': ('red', 1), 'Finish': ('blue',1)}

    def __init__(self, position, kind):
        super().__init__('')
        self.position = position
        self.setKind(kind)
        self.setFixedSize(30,30)

    def setKind(self,kind):
        self.kind = kind
        self.setColor(self.colorMap[kind][0])
        self.envCost = self.colorMap[kind][1]

    def setColor(self, color):
        self.setStyleSheet("background-color:" + color + "; color: white;")

    def __lt__(self, other):
        return self.position < other.position


class Grid(QFrame):
    finish = 0
    begin = 0
    flagBegin = False
    flagFinish = False
    #custo = [Horizontal, Vertical, Diagonal]
    cost = [1,1,1]
    envCost = 0

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
            if position[0] == 10 and position[1] < 15:
                land = Land(position, 'Wall')
            elif position[0] == width - 1 or position[0] == 0 or position[1] == height - 1 or position[1] == 0 :
                land = Land(position,'Edge')
            else:
                land = Land(position,'Default')
            self.map.addWidget(land, *position)
            land.clicked.connect(self.landClicked)

        self.finish = self.getLand(width - 2 , height - 2)
        # self.finish = self.getLand(18 ,15)
        self.finish.setKind("Finish")

        self.begin = self.getLand(1,1)
        self.begin.setKind("Begin")

    def getLand(self, x, y):
        return self.map.itemAtPosition(x, y).widget()

    def getNeighbors(self,land):
        neighbors = []
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

    def getCost(self, land1, land2):
        if land1.position[0] - land2.position[0] == 0:
            return self.cost[1] + land2.envCost
        else:
            if land1.position[1] - land2.position[1] == 0:
                return self.cost[0] + land2.envCost
            else:
                return self.cost[2] + land2.envCost


    def landClicked(self):
        land = self.sender()
        if land.kind == "Begin":
            self.flagBegin = True
            self.flagFinish = False
        elif land.kind == "Finish":
            self.flagFinish = True
            self.flagBegin = False
        elif land.kind != "Edge":
            if self.flagBegin:
                self.begin.setKind("Default")
                land.setKind("Begin")
                self.begin = land
                self.flagBegin = False
            elif self.flagFinish:
                self.finish.setKind("Default")
                land.setKind("Finish")
                self.finish = land
                self.flagFinish = False
            elif land.kind == "Wall":
                land.setKind("Default")
            elif land.kind == "Default":
                land.setKind("Wall")
        # print(land.position)

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

