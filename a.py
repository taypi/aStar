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
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, 
    QVBoxLayout, QApplication)

import time

# Subclassing QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QThread):

    def run(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("Increasing")
            count += 1

# Subclassing QObject and using moveToThread
# http://blog.qt.digia.com/blog/2007/07/05/qthreads-no-longer-abstract
class SomeObject(QObject):

    finished = pyqtSignal()

    def longRunning(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("Increasing")
            count += 1
        self.finished.emit()

# Using a QRunnable
# http://qt-project.org/doc/latest/qthreadpool.html
# Note that a QRunnable isn't a subclass of QObject and therefore does
# not provide signals and slots.
class Runnable(QRunnable):

    def run(self):
        count = 0
        app = QCoreApplication.instance()
        while count < 5:
            print("Increasing")
            time.sleep(1)
            count += 1
        app.quit()


def usingQThread():
    app = QCoreApplication([])
    thread = AThread()
    thread.finished.connect(app.exit)
    thread.start()
    sys.exit(app.exec_())

def usingMoveToThread():
    app = QCoreApplication([])
    objThread = QtCore.QThread()
    obj = SomeObject()
    obj.moveToThread(objThread)
    obj.finished.connect(objThread.quit)
    objThread.started.connect(obj.longRunning)
    objThread.finished.connect(app.exit)
    objThread.start()
    sys.exit(app.exec_())

def usingQRunnable():
    app = QCoreApplication([])
    runnable = Runnable()
    QtCore.QThreadPool.globalInstance().start(runnable)
    sys.exit(app.exec_())

if __name__ == "__main__":
    usingQThread()
    #usingMoveToThread()
    #usingQRunnable()