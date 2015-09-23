#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

This example shows text which 
is entered in a QLineEdit
in a QLabel widget.
 
author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, 
    QLineEdit, QApplication)


class Example():
  varTest = "1"  

  def setVar(self,string):
    Example.varTest = string

  def getVar(self):
    return Example.varTest

if __name__ == '__main__':
    ex = Example()
    print (ex.getVar())
    ab = Example()
    ab.setVar(2)
    print (ex.getVar())
    print (ab.getVar())