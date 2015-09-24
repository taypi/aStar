#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we connect a signal
of a QSlider to a slot of a QLCDNumber. 

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
from PyQt5.QtCore import (Qt, pyqtSignal, QObject)
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, 
    QVBoxLayout, QApplication)


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        path1 = []
        start = "a"
        path1.append(start)
        path1.append("b")
        path1.append("c")
        print(path1)

        path2 = []
        path2 = path2 + [start]
        path2 = path2 + ["b"]
        path2 = path2 + ["c"]
        print(path2)

        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())