#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import sys, sip
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSplitter, QStyleFactory, QGridLayout,
     QPushButton, QApplication, QLineEdit, QFrame, QLabel, QVBoxLayout, QMainWindow,
     QMessageBox)
from PyQt5.QtGui import (QIntValidator, QDoubleValidator)
from PyQt5.QtCore import (Qt, pyqtSignal, QObject, QSize)

from heapq import *

class Communicate(QObject):
    landChanged = pyqtSignal()

class PathFinder(QWidget):
    c = Communicate()
    width = 7
    height = 7
    def __init__(self):
        super().__init__()
        self.box = QHBoxLayout(self)

        self.grid = Grid(self.width, self.height)
        self.grid.setFrameShape(QFrame.StyledPanel)

        self.right = Settings()
        self.right.setFrameShape(QFrame.StyledPanel)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.grid)
        self.splitter.addWidget(self.right)

        self.box.addWidget(self.splitter)
        self.setLayout(self.box)
        self.setWindowTitle('Path Finder')

        self.reDo()
        self.c.landChanged.connect(self.reDo)

        self.show()

    def reDo(self):
        if self.grid.width != self.width or self.grid.height != self.height:            
            self.destroy()
            self.grid.width = self.width
            self.grid.height = self.height
            self.grid.initUI()
        else: 
            self.grid.clean()

        # came_from, cost_so_far = self.aStar(self.grid)
        # self.backTrackAStar(self.grid, came_from)

        shortest = self.dfs(self.grid, self.grid.begin, self.grid.finish)
        self.backTrackDfs(shortest)

    def destroy(self):
        for position in Grid.positions:
            (x,y) = position
            landT = self.grid.map.itemAtPosition(x, y)
            if landT is not None:
                land = landT.widget()
                if land is not None:
                    self.grid.map.removeWidget(land)
                    land.deleteLater()

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
                if (next.isValid()) and (
                    next not in cost_so_far or new_cost < cost_so_far[next]):
                    
                    cost_so_far[next] = new_cost
                    next.setText(str(new_cost))
                    priority = new_cost + self.heuristic(grid.finish.position, next.position)
                    heappush(frontier,(priority, next))
                    came_from[next] = current[1]
                    next.safeSetColor("DarkCyan")
                    current[1].safeSetColor("DarkSlateGray")
        return came_from, cost_so_far

    def backTrackAStar(self, grid, came_from):
        if grid.finish in came_from:
            land = grid.finish
            while came_from[land] != grid.begin:
                came_from[land].setColor("black")
                land = came_from[land]

    def backTrackDfs(self,shortest):
        previous = self.grid.begin
        cost_so_far = {}
        cost_so_far[previous] = 0
        previous.setText(str(cost_so_far[previous]))
        for next in shortest:
            if next.kind != 'Begin' and next.kind != "Finish":
                next.setColor("black")
            cost_so_far[next] = self.grid.getCost(previous, next) + cost_so_far[previous]
            next.setText(str(cost_so_far[next]))
            previous = next

    def dfs(self, grid, start, end, path = [], shortest = None):
        path = path + [start]
        if start == end:
            return path
        for next in grid.getNeighbors(start):
            if next not in path and next.isValid():
                next.safeSetColor("DarkSlateGray")
                if shortest == None or len(path) < len(shortest):
                    newPath = self.dfs(grid, next, end, path, shortest)
                    if newPath != None:
                        shortest = newPath
        return shortest

    def setSize(width, height):
        PathFinder.width = width
        PathFinder.height = height

class Land(QPushButton):
    colorMap = {'Edge': ('gray', 9999999), 'Default': ('green', 0), 'Wall': ('gray', 9999999), 'Begin': ('red', 0), 'Finish': ('blue',0)}

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

    def safeSetColor(self, color):
        if self.isValid and self.kind != 'Begin' and self.kind != 'Finish':
            self.setStyleSheet("background-color:" + color + "; color: white;")
    
    def isValid(self):
        if self.kind != 'Edge' and self.kind != 'Wall':
            return True
        else:
            return False

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
    width = 4
    height = 4

    def __init__(self, w, h):
        super().__init__()
        Grid.width = w
        Grid.height = h

        self.map = QGridLayout()
        self.map.setHorizontalSpacing(0)
        self.map.setVerticalSpacing(0)
        self.setLayout(self.map)
        
        self.initUI()

    def initUI(self):
        Grid.positions = [(i,j) for i in range(self.width) for j in range(self.height)]
        
        for position in Grid.positions:
            if position[0] == 10 and position[1] < 15:
                land = Land(position, 'Wall')
            # elif position[0] == self.width - 1 or position[0] == 0 or position[1] == self.height - 1 or position[1] == 0 :
            #     land = Land(position,'Edge')
            else:
                land = Land(position,'Default')
            self.map.addWidget(land, *position)
            land.clicked.connect(self.landClicked)

        self.finish = self.getLand(self.width - 2 , self.height - 2)
        self.finish.setKind("Finish")

        self.begin = self.getLand(1,1)
        self.begin.setKind("Begin")

    def getLand(self, x, y):
        return self.map.itemAtPosition(x, y).widget()

    def getNeighbors(self,land):
        neighbors = []
        if land:
            neighbors.append(self.getLand(land.position[0]-1, land.position[1]-1))
            neighbors.append(self.getLand(land.position[0]-1, land.position[1]))
            neighbors.append(self.getLand(land.position[0]-1, land.position[1]+1))
            neighbors.append(self.getLand(land.position[0], land.position[1]-1))
            neighbors.append(self.getLand(land.position[0], land.position[1]+1))
            neighbors.append(self.getLand(land.position[0]+1, land.position[1]-1))
            neighbors.append(self.getLand(land.position[0]+1, land.position[1]))
            neighbors.append(self.getLand(land.position[0]+1, land.position[1]+1))
        return neighbors

    def setCost(cost):
        Grid.cost = cost

    def getCost(self, land1, land2):
        if land1 == land2:
            return 0
        elif land1.position[0] - land2.position[0] == 0:
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
        validator = QIntValidator(1, 200)
        validatorSize = QIntValidator(1, 30)

        lblWidth = QLabel('Width')
        self.width = QLineEdit('20')
        self.width.setValidator(validatorSize)
        box.addWidget(lblWidth)
        box.addWidget(self.width)

        lblHeight = QLabel('Height')
        self.height = QLineEdit('20')
        self.height.setValidator(validatorSize)
        box.addWidget(lblHeight)
        box.addWidget(self.height)

        lblH = QLabel('Horizontal')
        self.costH = QLineEdit('1')
        self.costH.setValidator(validator)
        box.addWidget(lblH)
        box.addWidget(self.costH)

        lblV = QLabel('Vertical')
        self.costV = QLineEdit('1')
        self.costV.setValidator(validator)
        box.addWidget(lblV)
        box.addWidget(self.costV)

        lblD = QLabel('Diagonal')
        self.costD = QLineEdit('1')
        self.costD.setValidator(validator)
        box.addWidget(lblD)
        box.addWidget(self.costD)

        self.btnSend = QPushButton('Send', self)
        self.btnSend.clicked.connect(self.sendClicked)
        box.addWidget(self.btnSend)

    def sendClicked(self):
        if (self.costH.text() != '' and self.costV.text() != '' and self.costD.text() != '' and
            self.width.text() != '' and self.height.text() != ''):
            value = [float(self.costH.text()), float(self.costV.text()), float(self.costD.text())]
            Grid.setCost(value)
            if int(self.width.text()) > 3 and int(self.height.text()) > 3:
                PathFinder.setSize(int(self.height.text()), int(self.width.text()))
            else:
                QMessageBox.question(self, 'ERRO:',
                "Width and Height has to be bigger than 3!", QMessageBox.Ok)
            PathFinder.c.landChanged.emit()
        else:
            QMessageBox.question(self, 'ERRO:',
            "Some field is blank!", QMessageBox.Ok)

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    draw = PathFinder()
    sys.exit(app.exec_())
