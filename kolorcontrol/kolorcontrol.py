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
        subprocess.check_call(command)
        textcommands.append(" ".join(command))

    return "\n".join(textcommands)

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

        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas)
        #self.plotLayout.addWidget(self.toolbar)
        self.plotLayout.addWidget(self.canvas)

    def _spin_gammaexp_updater(self,  spin):
       def f(gamma):
           if self.spin_updater_enabled:
               print(gamma)
               spin.setValue(gammaexp(gamma))
       return f

    def _slider_gammalog_updater(self,  slider):
       def f(gamma):
           print(gamma)
           self.spin_updater_enabled = False
           slider.setValue(gammalog(gamma))
           self.spin_updater_enabled = True
       return f

    def do_xcalib(self):
        textcommands = set_xcalib(self.spinR_B.value(),  self.spinR_C.value(),  self.spinR_G.value(),
        self.spinG_B.value(),  self.spinG_C.value(),  self.spinG_G.value(),
        self.spinB_B.value(),  self.spinB_C.value(),  self.spinB_G.value(),)

        self.textBrowser.setText(textcommands)
