# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all PySide6 and matplotlib resources
mpl_datas, mpl_binaries, mpl_hiddenimports = collect_all("matplotlib")
qt_datas, qt_binaries, qt_hiddenimports = collect_all("PySide6")

# Analysis: gather everything needed
a = Analysis(
    ['../src/SleepScienceViewerApp.py'],   # Path to your main script
    pathex=['../src'],                     # Path to source folder
    binaries=qt_binaries + mpl_binaries,
    datas=qt_datas + mpl_datas,
    hiddenimports=(
        qt_hiddenimports
        + mpl_hiddenimports
        + [
            "matplotlib.backends.backend_qtagg",
            "matplotlib.backends.backend_qt5agg",
        ]
    ),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Package pure Python code
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the executable (onefile mode)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="SleepScienceViewerApp",
    debug=False,
    strip=False,
    upx=True,
    console=True,  # Set False if you don't want a console window
)

# Onefile wrapper
from PyInstaller.building.api import COLLECT
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="SleepScienceViewerApp"
)
