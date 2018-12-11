# KolorControl - Python Qt GUI to xcalib
# Copyright (C) 2017 Alexander Blinne

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import math

import numpy as np

from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

try:
    from .ui.main_ui import Ui_MainWindow
except ImportError:
    from . import ui
    from PyQt5 import uic
    import os.path as osp
    Ui_MainWindow, QtBaseClass = uic.loadUiType(osp.join(ui.__path__[0], "main.ui"))

def reset_xcalib(screennum):
    command = ["xcalib",  "-a",  "-s", str(screennum), "-c"]
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        pass
    return " ".join(command)

def set_xcalib(screennum, rb,  rc,  rg,  gb,  gc,  gg,  bb,  bc,  bg):
    command = ["xcalib",  "-a",  "-s", str(screennum),
                        "-red",  str(rg),  str(rb),  str(rc),
                        "-green",  str(gg),  str(gb),  str(gc),
                        "-blue",  str(bg),  str(bb),  str(bc)]
    textcommand = " ".join(command)
    command.insert(2, "-p")
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        output = None
    if output is None:
        raise ValueError('Invalid Parameters')
    output = np.loadtxt(output.splitlines(), comments="W")
    return textcommand, np.atleast_2d(output)

def gammalog(gamma):
    return int(round(math.log(gamma, 10)*100))

def gammaexp(gamma):
    return round(10**(gamma/100),  2)

class KCMainWindow(Ui_MainWindow):
    def __init__(self,  *args,  **kwargs):
        super().__init__(*args,  **kwargs)
        self.spin_updater_enabled = True
        self.xcalib_enabled = True

    def setupUi(self,  MainWindow):
        super().setupUi(MainWindow)
        self.spinR_G.setValue(1.0)
        self.spinG_G.setValue(1.0)
        self.spinB_G.setValue(1.0)

        self.sliderR_G.valueChanged['int'].connect(self._spin_gammaexp_updater(self.spinR_G))
        self.spinR_G.valueChanged['double'].connect(self._slider_gammalog_updater(self.sliderR_G))
        self.sliderG_G.valueChanged['int'].connect(self._spin_gammaexp_updater(self.spinG_G))
        self.spinG_G.valueChanged['double'].connect(self._slider_gammalog_updater(self.sliderG_G))
        self.sliderB_G.valueChanged['int'].connect(self._spin_gammaexp_updater(self.spinB_G))
        self.spinB_G.valueChanged['double'].connect(self._slider_gammalog_updater(self.sliderB_G))

        self.spinR_B.valueChanged['int'].connect(self.do_xcalib)
        self.spinR_C.valueChanged['int'].connect(self.do_xcalib)
        self.spinR_G.valueChanged['double'].connect(self.do_xcalib)
        self.spinG_B.valueChanged['int'].connect(self.do_xcalib)
        self.spinG_C.valueChanged['int'].connect(self.do_xcalib)
        self.spinG_G.valueChanged['double'].connect(self.do_xcalib)
        self.spinB_B.valueChanged['int'].connect(self.do_xcalib)
        self.spinB_C.valueChanged['int'].connect(self.do_xcalib)
        self.spinB_G.valueChanged['double'].connect(self.do_xcalib)

        # a figure instance to plot on
        self.figure = Figure()
        self.ax = None

        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        self.canvas.setMinimumSize(QtCore.QSize(200, 100))
        self.plotLayout.addWidget(self.canvas)

        self.resetButton.clicked.connect(self.on_resetButton_clicked)

    def _spin_gammaexp_updater(self,  spin):
       def f(gamma):
           if self.spin_updater_enabled:
               spin.setValue(gammaexp(gamma))
       return f

    def _slider_gammalog_updater(self,  slider):
       def f(gamma):
           self.spin_updater_enabled = False
           slider.setValue(gammalog(gamma))
           self.spin_updater_enabled = True
       return f

    def update_graph(self, data):
        if not self.ax:
            self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.figure.tight_layout()
        n, _ = data.shape
        scale = math.floor(65535*(n-1)/n)
        x = np.linspace(0,1,n)
        self.ax.plot(x, data[:,0]/scale, color="red")
        self.ax.plot(x, data[:,1]/scale, color="green")
        self.ax.plot(x, data[:,2]/scale, color="blue")
        self.canvas.draw()

    def do_xcalib(self):
        if self.xcalib_enabled:
            textcommands = []
            textcommands.append(reset_xcalib(self.spinScreen.value()))
            try:
                c, output = set_xcalib(self.spinScreen.value(),
                                                self.spinR_B.value(),  self.spinR_C.value(),  self.spinR_G.value(),
                                                self.spinG_B.value(),  self.spinG_C.value(),  self.spinG_G.value(),
                                                self.spinB_B.value(),  self.spinB_C.value(),  self.spinB_G.value(),)

                textcommands.append(c)
                self.update_graph(output)
                self.textBrowser.setText("\n".join(textcommands))
            except ValueError:
                pass

    def on_resetButton_clicked(self):
        self.xcalib_enabled = False
        self.spinR_B.setValue(0)
        self.spinG_B.setValue(0)
        self.spinB_B.setValue(0)
        self.spinR_C.setValue(100)
        self.spinG_C.setValue(100)
        self.spinB_C.setValue(100)
        self.spinR_G.setValue(1.0)
        self.spinG_G.setValue(1.0)
        self.spinB_G.setValue(1.0)
        self.xcalib_enabled = True
        textcommand = reset_xcalib(self.spinScreen.value())
        self.ax.clear()
        self.canvas.draw()
        self.textBrowser.setText(textcommand)
