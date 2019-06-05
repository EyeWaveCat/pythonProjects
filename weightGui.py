from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
import datetime
import time
import pandas as pd

class weightGui(QWidget):
    def __init__(self,fileName):
        QWidget.__init__(self)
        self.file = fileName
        self.setWindowTitle("WeightGui")
        
        m_layout = QHBoxLayout()
        self.setLayout(m_layout)
        m_rx = QRegExp("^([0-9]+)(\\.[0-9]+)?$")
        m_reg = QRegExpValidator(m_rx)
        self.weightEdit = QLineEdit()
        self.weightEdit.setValidator(m_reg)
        self.pushButton = QPushButton("OK")
        self.pushButton.clicked.connect(self.storgeWeight)

        m_layout.addWidget(self.weightEdit)
        m_layout.addWidget(self.pushButton)
    
    def storgeWeight(self):
        weightFile = open(self.file,'a')
        today = datetime.date.today()
        text = self.weightEdit.text()
        weightFile.write(str(today)+" "+text+"\n")
        weightFile.flush()
        self.buildWeightCurve()

    def buildWeightCurve(self):
        weightFile = open(self.file,'r')

        lines = weightFile.readlines()

        x=[]
        y=[]
        for line in lines:
            line = line.strip('\n')
            line = line.split(" ")
            if line != "":
                x.append(pd.to_datetime(line[0]))
                y.append(float(line[1]))

        plt.plot(x,y)
        plt.title("Weight Change")
        plt.xlabel("Time")
        plt.ylabel("Weight")
        plt.gcf().autofmt_xdate()

        plt.xticks(x)

        for a,b in zip(x,y):
                plt.text(a,b,b,ha='center',va='bottom',fontsize =10)

        plt.show()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wgui = weightGui(".\\weightData.txt")
    wgui.show()
    sys.exit(app.exec_())
