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

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from .ui.main_ui import Ui_MainWindow

def set_xcalib(rb,  rc,  rg,  gb,  gc,  gg,  bb,  bc,  bg):
    commands = [["xcalib",  "-a",  "-c"],
                ["xcalib",  "-a",  "-red",  str(rg),  str(rb),  str(rc),
                                   "-green",  str(gg),  str(gb),  str(gc),
                                   "-blue",  str(bg),  str(bb),  str(bc)]
                ]

    textcommands = []

    for command in commands:
        textcommands.append(" ".join(command))
        command.insert(2, "-p")
        output = subprocess.check_output(command)

    output = np.loadtxt(output.splitlines(), comments="W")

    return "\n".join(textcommands), output

def gammalog(gamma):
    return int(round(math.log(gamma, 10)*100))

def gammaexp(gamma):
    return round(10**(gamma/100),  2)

class KCMainWindow(Ui_MainWindow):
    def __init__(self,  *args,  **kwargs):
        super().__init__(*args,  **kwargs)
        self.spin_updater_enabled = True

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
        self.plotLayout.addWidget(self.canvas)

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
        self.ax.plot(np.linspace(0,1,256), data[:,0]/65279, color="red")
        self.ax.plot(np.linspace(0,1,256), data[:,1]/65279, color="green")
        self.ax.plot(np.linspace(0,1,256), data[:,2]/65279, color="blue")
        self.canvas.draw()

    def do_xcalib(self):
        textcommands, output = set_xcalib(self.spinR_B.value(),  self.spinR_C.value(),  self.spinR_G.value(),
        self.spinG_B.value(),  self.spinG_C.value(),  self.spinG_G.value(),
        self.spinB_B.value(),  self.spinB_C.value(),  self.spinB_G.value(),)

        self.update_graph(output)
        self.textBrowser.setText(textcommands)
