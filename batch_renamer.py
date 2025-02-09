# Author:   Nadia Ahlborg
#   
#       This is a stand-alone GUI to help rename many files at once. It's really goot for correcting 
#       typos in logfile names, or adding additional information to auto-generated files.

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from src.GUI import GUI as Gui
from info.version import version

import logging
logger = logging.getLogger("Batch Renamer")

def main():
    app = QApplication([])
    window = Gui()
    window.setWindowTitle("Batch Renamer | " + version)
    window.show()
    icon = QIcon("images\icon.png")
    window.setWindowIcon(icon)

    app.exec_()

if __name__ == "__main__":
    main()