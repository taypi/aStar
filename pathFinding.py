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

class Communicate(QObject): # cria aum sinal para mudanca da land
    landChanged = pyqtSignal()
    settingChanged = pyqtSignal()

class PathFinder(QWidget):
    c = Communicate() # cria  um sinal quando a land muda
    width = 5
    height = 5
    def __init__(self): #construtor da classe
        super().__init__() # super prover o uso dos metodos da classe herdada
        self.doIt()

    def doIt(self):
        self.box = QHBoxLayout(self) # cria uma box para receber os widgets

        self.gridAStar = Grid(self.width, self.height) # cria um grid para admin os widgets
        self.gridAStar.changed.connect(self.reDoAStar) # quando a land muda chama o reDo
        self.gridAStar.setFrameShape(QFrame.StyledPanel) # seta o formato do frame para um quadrado

        self.gridDfs = Grid(self.width, self.height)
        self.gridDfs.changed.connect(self.reDoDfs) # quando a land muda chama o reDo
        self.dfsDestroyed = False
        self.gridDfs.setFrameShape(QFrame.StyledPanel)

        self.right = Settings(self.gridAStar, self.gridDfs)  # right rrecebe as congiguracoes de campo
        self.right.changed.connect(self.reDo) # quando a land muda chama o reDo
        self.right.setFrameShape(QFrame.StyledPanel) # seta o formato do frame para um quadrado

        self.splitterV = QSplitter(Qt.Vertical) #reorganiza os qFrame's de acordo com o splitter
        self.splitterV.addWidget(self.gridAStar)
        self.splitterV.addWidget(self.gridDfs)

        self.splitterH = QSplitter(Qt.Horizontal)
        self.splitterH.addWidget(self.splitterV)
        self.splitterH.addWidget(self.right)

        self.box.addWidget(self.splitterH) # adiciona o splitter ao boox
        self.setLayout(self.box) # organiza tudo de acordo com o layout da box
        self.setWindowTitle('Path Finder')

        self.reDo() #  chama a classe para refazer
        self.show()

    def reDo(self):        
        self.reDoAStar()
        self.reDoDfs()

    def reDoAStar(self):  # reconstroi a UI
        if self.sizeHasChangeAStar():  # reconstroi tudo quando o box muda de tamanho
            self.destroy(self.gridAStar)
            self.gridAStar.width = self.width
            self.gridAStar.height = self.height
            self.gridAStar.initUI()

        else:
            self.gridAStar.clean()

        came_from, cost_so_far = self.aStar(self.gridAStar)
        self.backTrackAStar(self.gridAStar, came_from)


    def reDoDfs(self):
        if self.width < 8 and self.height < 8:
            if self.sizeHasChangeDfs() or self.dfsDestroyed:
                if not self.dfsDestroyed:
                    self.destroy(self.gridDfs)
                    self.dfsDestroyed = True
                self.gridDfs.width = self.width
                self.gridDfs.height = self.height
                self.gridDfs.initUI()
                self.dfsDestroyed = False
            else:
                self.gridDfs.clean()
            cost_so_far = {}
            cost_so_far[self.gridDfs.begin] = 0
            shortest, best_cost = self.dfs(self.gridDfs, cost_so_far, self.gridDfs.begin, self.gridDfs.finish) #roda a dfs
            self.backTrackDfs(shortest, best_cost) # chama o backtrack da dfs
        elif not self.dfsDestroyed:
            self.destroy(self.gridDfs)
            self.dfsDestroyed = True
    
    def sizeHasChangeAStar(self):
        return (self.gridAStar.width != self.width or self.gridAStar.height != self.height)

    def sizeHasChangeDfs(self):
        return (self.gridDfs.width != self.width or self.gridDfs.height != self.height)


    def destroy(self, grid): # deleta o todos os lands do campo
        for position in grid.positions:
            (x,y) = position
            landT = grid.map.itemAtPosition(x, y)
            if landT is not None:
                land = landT.widget()
                if land is not None:
                    grid.map.removeWidget(land)
                    land.deleteLater()

    def heuristic(self, a, b): # calcula o H ( F = G + H)
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def aStar(self, grid):
        frontier = []
        heappush(frontier,(0, grid.begin)) # push do começo
        came_from = {} #dicionario de onde as lands vieram
        cost_so_far = {} # dicionario do custo das lands ate entao
        cost_so_far[grid.begin] = 0 # custo da land de start

        while frontier: # enquanto o frontier nao for vazio
            current = heappop(frontier) # iterador que consome o frontier

            if current[1] == grid.finish: # passo base -- sai do while se o current for o finish
                break

            for next in grid.getNeighbors(current[1]):  # itera com o vizinhos do start
                new_cost = cost_so_far[current[1]] + grid.getCost(current[1], next) # recalcula o novo custo
                if (next.isValid()) and ( # nao eh parede nem fronteira &&
                    next not in cost_so_far or new_cost < cost_so_far[next]): #o next nao foi visitado ou novo custo menor que custo ate o next
                    cost_so_far[next] = new_cost # atualiza o custo da proxima land
                    next.setText(str(new_cost)) # mostra esse custo na land
                    priority = new_cost + grid.getGridCost() * self.heuristic(grid.finish.position, next.position) # analisa o melhor caminho para ir, atraves do peso da heurista + peso do caminho
                    heappush(frontier,(priority, next)) # adiciona em frontier a aproxima land com sua prioridade
                    came_from[next] = current[1] # atualiza o path, indicando o novo "pai" da land
                    next.safeSetColor("DarkCyan") # nao iterou os "vizinhos"
                    current[1].safeSetColor("DarkSlateGray") # iterou os "vizinhos"
        return came_from, cost_so_far

    def backTrackAStar(self, grid, came_from):
        if grid.finish in came_from: # se o path achou o final
            land = grid.finish       # start do iterador
            while came_from[land] != grid.begin: # enquanto ele nao chegar ao comeco
                came_from[land].setColor("black") # pinta de onde ele veio
                land = came_from[land] # itera
                
    def backTrackDfs(self, shortest, best_cost):
        if shortest: # se shortest nao eh vazio
            last_cost = 0
            last = shortest.pop(0) # retorna o primeiro elemento do menor caminho 
            last_cost = [best_cost[last]].pop()
            last.setText(str(last_cost)) # imprime o custo da land
            while shortest: # enquanto ele nao for vazio
                next = shortest.pop(0) # itera pelo menor caminho
                next.safeSetColor("black") # pinta de "menor caminho"
                last_cost = self.gridDfs.getCost(last, next) + last_cost  # atualiza o custo  da land
                next.setText(str(last_cost)) # imprime o valor dessa land do menor caminho
                last = next

    def dfs(self, grid, cost_so_far, start, end, path = [], shortest = None, best_cost = None):
        path = path + [start] # atualiza o path
        if start != grid.begin: # begin nao tem antecessor
            cost_so_far[start] = grid.getCost(path[-2], start) + cost_so_far[path[-2]] # custo[start] = custo entre as lands + custo até a anterior
        if start == end:
            return path, cost_so_far # se achou o final retorna o caminho com seu custo 
        for next in grid.getNeighbors(start): # itera todos os vizinhos desse start especifico
            if next not in path and next.isValid(): # se o essa land nao esta no caminho passado, para evitar ciclos
                next.safeSetColor("DarkSlateGray") # pisou
                if shortest == None or cost_so_far[start] < best_cost[grid.finish]: # se a primeira vez que roda ou se o custo da até a land eh menor que o custo do melhor caminho
                    newPath, new_cost_so_far = self.dfs(grid, cost_so_far, next, end, path, shortest, best_cost) # atualiza o novo caminho e seu custo
                    if newPath != None: # se a recursao retornou um caminho, quer dizer que econtrou um caminho melhor que o anterior
                        shortest = newPath #atualiza o path e seu custo
                        best_cost = new_cost_so_far
        return shortest, best_cost

    def setSize(width, height):
        PathFinder.width = width
        PathFinder.height = height

class Land(QPushButton):
    colorMap = {'Edge': ('gray', 1), 'Default': ('green', 1), 'Wall': ('gray', 1), 'Begin': ('red', 1), 'Finish': ('blue', 1), 'Sand': ('Tan', 2),'Water': ('DodgerBlue', 3)}

    def __init__(self, position, kind):
        super().__init__()
        self.position = position
        self.setKind(kind)
        self.setFixedSize(30,30)

    def setKind(self,kind):
        self.kind = kind
        self.setColor(self.colorMap[kind][0])
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
    positions = 0
    changed = pyqtSignal()

    def __init__(self, w, h):
        super().__init__()
        self.width = w
        self.height = h
        self.cost_so_far = {}
        self.cost_so_far[self.begin] = 0
        self.map = QGridLayout()
        self.map.setHorizontalSpacing(0)
        self.map.setVerticalSpacing(0)
        self.setLayout(self.map)

        self.initUI()

    def initUI(self):
        self.positions = [(i,j) for i in range(self.width) for j in range(self.height)]

        for position in self.positions:
            # Coloca uma parede no meio do mapa para teste
            # if position[0] == 10 and position[1] < 15:
            #     land = Land(position, 'Wall')
            if position[0] == self.width - 1 or position[0] == 0 or position[1] == self.height - 1 or position[1] == 0 :
                land = Land(position,'Edge')
            else:
                land = Land(position,'Default')
            self.map.addWidget(land, *position)
            land.clicked.connect(self.landClicked)

        self.finish = self.getLand(self.width - 2 , self.height - 2)
        # self.finish = self.getLand(18 ,15)
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

    def getGridCost(self):
        return (self.cost[0] + self.cost[1] + self.cost[2])/3

    def getCost(self, land1, land2):
        if land1 == land2:
            return 0
        elif land1.position[0] - land2.position[0] == 0:
            return self.cost[1]*land2.colorMap[land2.kind][1]
        else:
            if land1.position[1] - land2.position[1] == 0:
                return self.cost[0]*land2.colorMap[land2.kind][1]
            else:
                return self.cost[2]*land2.colorMap[land2.kind][1]

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
            elif land.kind == "Default":
                land.setKind("Wall")
            elif land.kind == "Wall":
                land.setKind("Water")
            elif land.kind == "Water":
                land.setKind("Sand")
            elif land.kind == "Sand":
                land.setKind("Default")
            self.changed.emit()

    def clean(self):
        for position in self.positions:
            (x, y) = position
            land = self.getLand(x, y)
            land.setKind(land.kind)

class Settings(QFrame):
    changed = pyqtSignal()
    def __init__(self, gridAStar, gridDfs):
        super().__init__()
        self.gridAStar = gridAStar
        self.gridDfs = gridDfs
        self.initUI()

    def initUI(self):

        box = QVBoxLayout(self)
        validator = QIntValidator(1, 200)
        validatorSize = QIntValidator(1, 30)

        lblWidth = QLabel('Width')
        self.width = QLineEdit('')
        self.width.setValidator(validatorSize)
        box.addWidget(lblWidth)
        box.addWidget(self.width)

        lblHeight = QLabel('Height')
        self.height = QLineEdit('')
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
            value = [int(self.costH.text()), int(self.costV.text()), int(self.costD.text())]
            Grid.setCost(value)
            if int(self.width.text()) > 3 and int(self.height.text()) > 3:
                PathFinder.setSize(int(self.height.text()), int(self.width.text()))
            else:
                QMessageBox.question(self, 'ERRO:',
                "Width and Height has to be bigger than 3!", QMessageBox.Ok)
            self.changed.emit()
        else:
            QMessageBox.question(self, 'ERRO:',
            "Some field is blank!", QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    draw = PathFinder()
    sys.exit(app.exec_())
