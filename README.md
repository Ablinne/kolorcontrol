# kolorcontrol
Simple GUI front-end to xcalib

This little GUI tool is intended to set your screen brightness, contrast and gamma levels for each color channel. It is implemented as a front-end to `xcalib`, a command line utility. It will also display the actual `xcalib` command line, suitible for copy-pasting to a script to run automatically on login to activate your desired settings.

## Install

To install this utility directly from github use

```
pip3 install git@github.com:Ablinne/kolorcontrol.git
```

However this requires you to have `pyqt_distutils` and `pyuic5` installed beforehand.
If you do not wish to install these, you can download a tarball from
<http://www.blinne.net/files/kolorcontrol/> and install KolorControl from that using

```
tar xfz KolorControl-*.tar.gz
cd KolorControl-*
python3 setup.py install
```

## Usage

Just run `kolorcontrol` and adjust your screen!
