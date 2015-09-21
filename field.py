class WindowSapper(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.resize(450,350)
        self.centralwidget = QtGui.QWidget()
        self.setCentralWidget(self.centralwidget)

        self.vLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.hLayout = QtGui.QHBoxLayout()

        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(0)

        # center the grid with stretch on both sides
        self.hLayout.addStretch(1)
        self.hLayout.addLayout(self.gridLayout)
        self.hLayout.addStretch(1)

        self.vLayout.addLayout(self.hLayout)
        # push grid to the top of the window
        self.vLayout.addStretch(1)

        self.buttons = []
        for i in xrange(10):
            l=[]
            for j in xrange(10):
                b=QtGui.QPushButton()
                b.setFixedSize(40,30)
                l.append(b)
                self.gridLayout.addWidget(b, i, j)
                self.gridLayout.setColumnMinimumWidth(j, 40)
            self.buttons.append(l)
            self.gridLayout.setRowMinimumHeight(i, 26)
