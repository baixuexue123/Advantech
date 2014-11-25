#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------


from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import numpy as np


class QwtChart(Qwt.QwtPlot):
    def __init__(self, *args):
        super(QwtPlot, self).__init__(*args)
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
        self.setAxisScale(Qwt.QwtPlot.xBottom, 0.0, 3600.0)
        self.setAxisScale(Qwt.QwtPlot.yLeft, 0.0, 30.0)

        # insert a few curves
        self.curveA = Qwt.QwtPlotCurve(u'curveA')
        self.curveA.setPen(Qt.QPen(Qt.Qt.red))
        self.curveA.attach(self)

        self.curveB = Qwt.QwtPlotCurve(u'curveB')
        self.curveB.setPen(Qt.QPen(Qt.Qt.blue))
        self.curveB.attach(self)

        # insert a horizontal marker at y = 0
        mY = Qwt.QwtPlotMarker()
        mY.setLabel(Qwt.QwtText('y = 0'))
        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setYValue(0.0)
        mY.attach(self)

        # insert a vertical marker at x = 2 pi
        mX = Qwt.QwtPlotMarker()
        mX.setLabel(Qwt.QwtText('x = 2 pi'))
        mX.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mX.setLineStyle(Qwt.QwtPlotMarker.VLine)
        mX.setXValue(2*math.pi)
        mX.attach(self)

        #Initialize data
        self.x = np.arange(0.0, 101.0, 1.0)
        self.curveAData = np.array
        self.curveBData = np.array

    def setData(self, AData, BData):
        self.curveA.setData(self.x, AData)
        self.curveB.setData(self.x, BData)
        self.replot()

    def appendData(self, AData, BData):
        self.curveAData = np.concatenate((self.curevAData, AData), 1)
        self.curveBData = np.concatenate((self.curevBData, BData), 1)
        self.curveA.setData(self.x, self.curveAData)
        self.curveB.setData(self.x, self.curveBData)
        self.replot()

    def clear(self):
        self.curveA.setData(self.x, [])
        self.curveB.setData(self.x, [])
        self.replot()



if __name__ == "__main__":
    pass
