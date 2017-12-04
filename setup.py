from setuptools import setup

try:
    from pyqt_distutils.build_ui import build_ui
    from setuptools.command.sdist import sdist
    from setuptools.command.install import install
    from setuptools.command.develop import develop

    class custom_sdist(sdist):
        def run(self):
            self.run_command('build_ui')
            return sdist.run(self)

    class custom_develop(develop):
        def run(self):
            self.run_command('build_ui')
            return develop.run(self)

    class custom_install(install):
        def run(self):
            self.run_command('build_ui')
            return install.run(self)

    cmdclass = {"build_ui": build_ui,
                "sdist": custom_sdist,
                "develop": custom_develop,
                "install": custom_install}

except ImportError:
    cmdclass = {}

setup(
    name="KolorControl",
    author="Alexander Blinne",
    author_email="alexander@blinne.net",
    url="https://github.com/Ablinne/kolorcontrol",
    python_requires=">= 3.4",
    version="0.2",
    packages=["kolorcontrol", "kolorcontrol.ui"],
    scripts=["scripts/kolorcontrol"],
    cmdclass=cmdclass,
)

