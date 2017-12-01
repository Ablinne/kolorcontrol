
import subprocess
import math

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
