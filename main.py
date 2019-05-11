# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
from scipy.integrate import *
import numpy as np

class UiForm(object):
    def __init__(self):
        self.r = QtWidgets.QDoubleSpinBox(Form)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_3 = QtWidgets.QLabel(Form)
        self.L = QtWidgets.QDoubleSpinBox(Form)
        self.btn_pause = QtWidgets.QPushButton(Form)
        self.btn_start = QtWidgets.QPushButton(Form)
        self.label_2 = QtWidgets.QLabel(Form)
        self.R = QtWidgets.QDoubleSpinBox(Form)
        self.label = QtWidgets.QLabel(Form)
        self.M = QtWidgets.QDoubleSpinBox(Form)
        self.chartView = QtChart.QChartView(Form)
        self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)

        self.chart = self.chartView.chart()
        self.chart.legend().setVisible(False)
        self.axisX = QtChart.QValueAxis()
        self.axisY = QtChart.QValueAxis()

        self.axis_series = QtChart.QLineSeries()
        self.ring_series = QtChart.QLineSeries()
        self.rope_series = QtChart.QLineSeries()
        self.dot_series = QtChart.QScatterSeries()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.total_time = .0

        self.runge_kutta = ode(self.f)
        self.runge_kutta.set_integrator('dopri5')

        self.dest = +1
        self.flag = True

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 600)
        self.M.setGeometry(QtCore.QRect(90, 550, 61, 22))
        self.M.setDecimals(3)
        self.M.setMinimum(0.001)
        self.M.setMaximum(100.99)
        self.M.setProperty("value", 0.05)
        self.M.setObjectName("M")
        self.label.setGeometry(QtCore.QRect(90, 530, 61, 13))
        self.label.setObjectName("label")
        self.R.setGeometry(QtCore.QRect(160, 550, 61, 22))
        self.R.setDecimals(2)
        self.R.setMinimum(0.001)
        self.R.setProperty("value", 1)
        self.R.setObjectName("R")
        self.label_2.setGeometry(QtCore.QRect(160, 530, 61, 13))
        self.label_2.setObjectName("label_2")
        self.btn_start.setGeometry(QtCore.QRect(379, 540, 100, 23))
        self.btn_start.setObjectName("btn_start")
        self.btn_pause.setGeometry(QtCore.QRect(379, 570, 100, 23))
        self.btn_pause.setObjectName("btn_pause")
        self.L.setGeometry(QtCore.QRect(20, 550, 61, 22))
        self.L.setDecimals(2)
        self.L.setMinimum(0.01)
        self.L.setMaximum(50)
        self.L.setProperty("value", 10)
        self.L.setObjectName("L")
        self.label_3.setGeometry(QtCore.QRect(20, 530, 61, 13))
        self.label_3.setObjectName("label_3")
        self.label_4.setGeometry(QtCore.QRect(230, 530, 61, 13))
        self.label_4.setObjectName("label_4")
        self.r.setGeometry(QtCore.QRect(230, 550, 61, 22))
        self.r.setDecimals(2)
        self.r.setMinimum(0.001)
        self.r.setProperty("value", 0.5)
        self.r.setObjectName("r")
        self.chartView.setGeometry(QtCore.QRect(10, 10, 471, 511))
        self.chartView.setObjectName("chartView")

        # add Axis
        self.chart.addAxis(self.axisX, QtCore.Qt.AlignBottom)
        self.chart.addAxis(self.axisY, QtCore.Qt.AlignLeft)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.r.editingFinished.connect(self.on_r_editing_finished)
        self.R.editingFinished.connect(self.on_RL_editing_finished)
        self.L.editingFinished.connect(self.on_RL_editing_finished)
        self.btn_start.clicked.connect(self.onStart)
        self.btn_pause.clicked.connect(self.onStop)
        self.timer.timeout.connect(self.onTimer)

        self.chart.addSeries(self.axis_series)
        self.axis_series.attachAxis(self.axisX)
        self.axis_series.attachAxis(self.axisY)

        self.chart.addSeries(self.ring_series)
        self.ring_series.attachAxis(self.axisX)
        self.ring_series.attachAxis(self.axisY)

        self.chart.addSeries(self.rope_series)
        self.rope_series.attachAxis(self.axisX)
        self.rope_series.attachAxis(self.axisY)
        self.rope_series.setColor(QtGui.QColor("blue"))

        self.chart.addSeries(self.dot_series)
        self.dot_series.attachAxis(self.axisX)
        self.dot_series.attachAxis(self.axisY)
        self.dot_series.setMarkerShape(QtChart.QScatterSeries.MarkerShapeCircle)
        self.dot_series.setMarkerSize(10)

        self.on_RL_editing_finished()

        self.btn_pause.setDisabled(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Маятник максвелла"))
        self.label.setText(_translate("Form", "M, кг"))
        self.label_2.setText(_translate("Form", "R, м"))
        self.btn_start.setText(_translate("Form", "Старт"))
        self.btn_pause.setText(_translate("Form", "Пауза"))
        self.label_3.setText(_translate("Form", "L, м"))
        self.label_4.setText(_translate("Form", "r, м"))

    def redraw(self, y, fi):
        self.rope_series.clear()
        self.ring_series.clear()
        self.axis_series.clear()
        self.dot_series.clear()
        dx = 2 * self.r.value() * self.dest
        dy = self.L.value() - y
        self.rope_series.append(0, self.L.value())
        self.rope_series.append(0, dy)

        for i in np.arange(-np.pi - 0.1, np.pi, 0.1):
            self.ring_series.append(dx + 2 * self.R.value() * np.cos(i), 2 * self.R.value() * np.sin(i) + dy)
            self.axis_series.append(dx + 2 * self.r.value() * np.cos(i), 2 * self.r.value() * np.sin(i) + dy)
        self.dot_series.append(dx + 2 * self.R.value() * np.cos(-fi), 2 * self.R.value() * np.sin(-fi) + dy)
        self.dot_series.append(dx + 2 * self.r.value() * np.cos(-fi), 2 * self.r.value() * np.sin(-fi) + dy)

    def on_r_editing_finished(self):
        if self.r.value() > self.R.value():
            self.r.setValue(self.R.value())
        self.redraw(0, 0)

    def on_RL_editing_finished(self):
        self.chart.axisY().setRange(-self.R.value() - 5, self.L.value() + self.R.value() + 5)
        self.chart.axisX().setRange(-self.R.value() - 5 - self.L.value() / 2, self.L.value() / 2 + self.R.value() + 5)
        self.redraw(0, 0)

    def onTimer(self):
        self.runge_kutta.integrate(self.total_time)
        self.total_time += self.timer.interval() / 1000
        self.redraw(self.runge_kutta.y[0], self.runge_kutta.y[2])

    def onStart(self):
        if not self.btn_pause.isEnabled():
            self.runge_kutta.set_initial_value([0, 0, 0, 0])
        self.set_disabled_splin_boxes(True)
        self.timer.start()
        self.btn_start.setDisabled(True)
        self.btn_pause.setText("Пауза")
        self.btn_pause.setDisabled(False)

    def onStop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_start.setDisabled(False)
            self.btn_pause.setText("Стоп")
        else:
            self.btn_pause.setDisabled(True)
            self.btn_start.setDisabled(False)
            self.btn_pause.setText("Пауза")
            self.set_disabled_splin_boxes(False)
            self.total_time = .0
            self.redraw(0, 0)

    def set_disabled_splin_boxes(self, value):
        self.L.setDisabled(value)
        self.r.setDisabled(value)
        self.R.setDisabled(value)
        self.M.setDisabled(value)

    # система уравнений
    def f(self, t, Y):
        FY = []
        # Y[0] x
        # Y[1] Vx
        # Y[2] fi
        # Y[3] w

        j = 0.5 * self.M.value() * self.R.value() ** 2
        g = 9.81

        FY.append(self.dest * Y[1])
        FY.append(self.dest * g * (1 - 1 / (1 + self.M.value() * self.r.value() ** 2 / j)))
        FY.append(Y[3])
        FY.append(self.dest * self.M.value() * g * self.r.value() / (j + self.M.value() * self.r.value() ** 2))

        if (Y[0] > self.L.value()) and self.flag:
            self.dest = -self.dest
            self.flag = False

        if Y[0] < 1:
            self.flag = True

        return FY


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = UiForm()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
