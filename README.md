# kolorcontrol
Simple GUI front-end to xcalib

This little GUI tool is intended to set your screen brightness, contrast and gamma levels for each color channel. It is implemented as a front-end to `xcalib`, a command line utility. It will also display the actual `xcalib` command line, suitible for copy-pasting to a script to run automatically on login to activate your desired settings.

## Installation and dependencies

This utility is a front-end to the command line utility `xcalib`, which you will need to install manually according to your distribution.

This utility is written for `Python 3`. Before installation make sure you also have the following python packages installed:
* setuptools
* pyqt5
* pyqt_distutils
* matplotlib

To install this utility directly from github use

```
pip3 install --user git+https://github.com/Ablinne/kolorcontrol.git
```

## Usage

Just run `kolorcontrol` and adjust your screen!
