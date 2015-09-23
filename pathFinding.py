#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QStyleFactory, QGridLayout,
    QPushButton, QApplication, QLineEdit, QFrame, QLabel, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import (Qt, pyqtSignal, QObject)

from heapq import *

class Communicate(QObject):
    landChanged = pyqtSignal()

class PathFinder(QWidget):
    c = Communicate()
    def __init__(self):
        super().__init__()
        box = QHBoxLayout(self)

        self.grid = Grid()
        self.grid.setFrameShape(QFrame.StyledPanel)

        right = Settings()
        right.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.grid)
        splitter.addWidget(right)

        box.addWidget(splitter)
        self.setLayout(box)
        self.setWindowTitle('Path Finder')
        self.show()


        self.reDo()
        self.c.landChanged.connect(self.reDo)

    def reDo(self):
        self.grid.clean()
        came_from, cost_so_far = self.aStar(self.grid)
        self.backTrack(self.grid, came_from)

    def heuristic(self, a, b):
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
                if (next.kind != 'Wall' and next.kind != 'Edge') and (
                    next not in cost_so_far or new_cost < cost_so_far[next]):
                    
                    cost_so_far[next] = new_cost
                    next.setText(str(new_cost))
                    priority = new_cost + self.heuristic(grid.finish.position, next.position)
                    heappush(frontier,(priority, next))
                    came_from[next] = current[1]

                    if next.kind != 'Begin' and next.kind != 'Finish':
                        next.setColor("DarkCyan")
                    if current[1].kind != 'Begin' and current[1].kind != 'Finish':
                        current[1].setColor("DarkSlateGray")
        return came_from, cost_so_far

    def backTrack(self, grid, came_from):
        if grid.finish in came_from:
            land = grid.finish
            while came_from[land] != grid.begin:
                came_from[land].setColor("black")
                land = came_from[land]

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
        self.setText('')

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
    positions = 0

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

        Grid.positions = [(i,j) for i in range(width) for j in range(height)]

        for position in Grid.positions:
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
        Grid.cost = cost

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
        PathFinder.c.landChanged.emit()

    def clean(self):
        for position in Grid.positions:
            (x, y) = position
            land = self.getLand(x, y)
            land.setKind(land.kind)
            # if land.kind != 'Wall' and land.kind != 'Begin' and land.kind != 'Finish' and land.kind != 'Edge':
            #     land.setKind('Default')

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
        value = [int(self.costH.text()), int(self.costV.text()), int(self.costD.text())]
        Grid().setCost(value)
        PathFinder.c.landChanged.emit()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    draw = PathFinder()
    sys.exit(app.exec_())

