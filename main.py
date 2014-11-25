#!/usr/bin/env python
# -*- coding: utf-8 -*-

__autor__ = 'baixue'

import math
from PyQt4 import QtCore, QtGui, Qt
import PyQt4.Qwt5 as Qwt
import numpy as np


class Chart(Qwt.QwtPlot):
    def __init__(self, *args):
        super(Chart, self).__init__(*args)
        #set title
        self.setTitle(u'<h4><font color=red>图表</font></h4>')
        #背景色
        self.setCanvasBackground(Qt.Qt.white)
        #插入图例--曲线名
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend)

        # a variation on the C++ example
        self.plotLayout().setAlignCanvasToScales(True)
        
        #创建网格
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        grid.setPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.DotLine))
        
        # set axis titles
        self.setAxisTitle(Qwt.QwtPlot.xBottom, u'Time(s)')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, u'Values')
        
        # set Scale Range
        self.setAxisScale(Qwt.QwtPlot.xBottom, 0.0, 10000.0)
        self.setAxisScale(Qwt.QwtPlot.yLeft, -10.0, 10.0)

        # insert a few curves
        self.curveA = Qwt.QwtPlotCurve(u'curveA')
        self.curveA.setPen(Qt.QPen(Qt.Qt.red))
        self.curveA.attach(self)

        self.curveB = Qwt.QwtPlotCurve(u'curveB')
        self.curveB.setPen(Qt.QPen(Qt.Qt.blue))
        self.curveB.attach(self)

        # insert a horizontal marker at y = xxx
        mY = Qwt.QwtPlotMarker()
        mY.setLabel(Qwt.QwtText('Maker:Y'))
        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setYValue(0.0)
        mY.setLinePen(Qt.QPen(Qt.Qt.green, 1, Qt.Qt.DashDotLine))
        mY.attach(self)

        # insert a vertical marker
        mX = Qwt.QwtPlotMarker()
        mX.setLabel(Qwt.QwtText('Maker:X'))
        mX.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mX.setLineStyle(Qwt.QwtPlotMarker.VLine)
        mX.setXValue(500)
        mX.setLinePen(Qt.QPen(Qt.Qt.green, 1, Qt.Qt.DashDotLine))
        mX.attach(self)


        #Initialize data
        self.x = np.arange(0.0, 10001.0, 1.0)
        self.curveAData = np.zeros(len(self.x), Float)
        self.curveBData = np.zeros(len(self.x), Float)

        
    def setData(self, AData, BData):
        self.curveA.setData(self.x, AData)
        self.curveB.setData(self.x, BData)
        self.replot()

    def appendData(self, AData, BData):
        self.curveAData = np.concatenate((self.curveAData[len(AData):], AData), 1)
        self.curveBData = np.concatenate((self.curveBData[len(BData):], BData), 1)
        self.curveA.setData(self.x, self.curveAData)
        self.curveB.setData(self.x, self.curveBData)
        self.replot()

    def clear(self):
        self.curveA.setData(self.x, [])
        self.curveB.setData(self.x, [])
        self.replot()

    
class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(Qt.QIcon(":/images/images/logo.png"))
        self.setWindowOpacity(1.0)
        self.setMinimumSize(800,600)
        self.chart = Chart()
        self.setCentralWidget(self.chart)
        #data
        self.count = 0
        self.start(50)

    def start(self, interval):
        self.timerId = self.startTimer(interval)

    def stop(self):
        self.killTimer(self.timerId)
        
    def timerEvent(self, e):
        index = self.count%500
        #aData = [2*math.sin(i) for i in sineData[index : index+10]]
        AData = sineData[index : index+10]
        BData = np.ones(10)
        self.chart.appendData(AData, BData)
        self.count += 10
        
    def closeEvent(self, event):
        self.stop()
        self.close()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())






