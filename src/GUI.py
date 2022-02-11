# Author:   Nadia Ahlborg
#           nahlborg@quantumscape.com
#   
#       This is a stand-alone GUI to help rename many files at once. It's really goot for correcting 
#       typos in logfile names, or adding additional information to auto-generated files.


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, \
    QListWidget, QLineEdit, QGroupBox, QLabel, QCheckBox, QFileDialog, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from os.path import isfile
import json
import sys

from src.renamer import Renamer

import logging
from logging import StreamHandler
logger = logging.getLogger("Batch Renamer")
logger.addHandler(StreamHandler(stream=sys.stdout))

class GUI(QWidget):
    '''
    A nice interface
    '''

    def __init__(self, onlyLocalFiles=True):
        super(GUI, self).__init__()

        #set attribuites
        self.onlyLocalFiles = onlyLocalFiles
        self._openButton = QPushButton("Open")
        self._openButton.setFixedWidth(100)
        self._clearButton = QPushButton("Clear")
        self._clearButton.setFixedWidth(100)
        self._executeRenameButton = QPushButton("Execute Rename")
        self._fileListBox = QListWidget()
        self._fileListBox.setMinimumHeight(350)
        self._replaceThisText = QLineEdit()
        self._replaceThisText.setMaximumHeight(30)
        self._replaceWithText = QLineEdit()
        self._replaceWithText.setMaximumHeight(30)
        self._useRegex = QCheckBox()
        self._caseSensitive = QCheckBox()
        self._changeExtension = QCheckBox()

        self._Renamer = Renamer()

        #draw layout
        self.drawLayout()

        #load default check options from settings file
        self.loadSettings()

        #connect signals
        self._openButton.clicked.connect(self.onOpenButtonPush)
        self._clearButton.clicked.connect(self.onClearButtonPush)
        self._executeRenameButton.clicked.connect(self.onExecuteButtonPush)

        #set navigation
        self.setNavigation()

        #set style
        with open(r"qss\stylesheet.qss") as fid:
            raw = fid.read()
            self.setStyleSheet(raw)

    def drawLayout(self):
        topBox = QHBoxLayout()
        topBox.addStretch(1)
        topBox.addWidget(self._openButton)
        topBox.addWidget(self._clearButton)
        topBox.addStretch(1)

        botBox = QGroupBox()
        checkBoxes = QHBoxLayout()
        checkBoxes.addWidget(QLabel("Use Regex?"))
        checkBoxes.addWidget(self._useRegex)
        checkBoxes.addSpacing(1)
        checkBoxes.addWidget(QLabel("Case Sensitive?"))
        checkBoxes.addWidget(self._caseSensitive)
        checkBoxes.addSpacing(1)
        checkBoxes.addWidget(QLabel("Change Extension?"))
        checkBoxes.addWidget(self._changeExtension)
        checkBoxes.addStretch(1)
        textEdits = QGridLayout()
        textEdits.addWidget(QLabel("Replace This Text:"), 1,0)
        textEdits.addWidget(self._replaceThisText, 1,2)
        textEdits.addWidget(QLabel("Replace With Text:"), 2,0)
        textEdits.addWidget(self._replaceWithText, 2,2)
        subBox = QVBoxLayout()
        subBox.addLayout(checkBoxes)
        subBox.addLayout(textEdits)
        subBox.addStretch(1)
        botBox.setLayout(subBox)

        sigBox = QHBoxLayout()
        sigBox.addStretch(1)
        signature = QLabel("Created by Nadia Ahlborg")
        signature.setObjectName("signature")
        sigBox.addWidget(signature)

        mainBox = QVBoxLayout()
        mainBox.addLayout(topBox)
        mainBox.addWidget(self._fileListBox)
        mainBox.addWidget(botBox)
        mainBox.addWidget(self._executeRenameButton)
        mainBox.addStretch(1)
        mainBox.addLayout(sigBox)
        self.setLayout(mainBox)

    def setNavigation(self):
        self.setTabOrder(self._openButton, self._clearButton)
        self.setTabOrder(self._clearButton, self._useRegex)
        self.setTabOrder(self._useRegex, self._caseSensitive)
        self.setTabOrder(self._caseSensitive, self._changeExtension)
        self.setTabOrder(self._changeExtension, self._replaceThisText)
        self.setTabOrder(self._replaceThisText, self._replaceWithText)
        self.setTabOrder(self._replaceWithText, self._executeRenameButton)

        self._openButton.setShortcut(QKeySequence(Qt.CTRL+Qt.Key_O))
        self._openButton.setToolTip("Ctrl+O")
        self._executeRenameButton.setAutoDefault(True)
    
    def loadSettings(self):
        settings = {}
        if isfile(r"settings\user_settings.json"):
            with open(r"settings\user_settings.json", "r") as fid:
                settings = json.load(fid)
        elif isfile(r"settings\default_settings.json"):
            with open(r"settings\default_settings.json", "r") as fid:
                settings = json.load(fid)
        else:
            logger.warning("No settings file found.")

        if "useRegex" in settings:
            self._useRegex.setChecked(bool(settings["useRegex"]))
        else:
            logger.warning("'useRegex' not found in settings file.")
        if "caseSensitive" in settings:
            self._caseSensitive.setChecked(bool(settings["caseSensitive"]))
        else:
            logger.warning("'caseSensitive' not found in settings file.")
        if "changeExtension" in settings:
            self._changeExtension.setChecked(bool(settings["changeExtension"]))
        else:
            logger.warning("'changeExtension' not found in settings file.")

    def saveSettings(self):
        settings = {}
        if self._useRegex.checkState():
            settings["useRegex"] = 1
        else:
            settings["useRegex"] = 0
        if self._caseSensitive.checkState():
            settings["caseSensitive"] = 1
        else:
            settings["caseSensitive"] = 0
        if self._changeExtension.checkState():
            settings["changeExtension"] = 1
        else:
            settings["changeExtension"] = 0

        with open(r"settings\user_settings.json", "w+") as fid:
            json.dump(settings, fid)

    def onOpenButtonPush(self):
        paths = QFileDialog.getOpenFileNames()[0]

        #restrict to only files on the C drive
        if self.onlyLocalFiles:
            badLoadFlag = False
            temp = []
            for path in paths:
                if path.startswith("C:"):
                    temp.append(path)
                else:
                    badLoadFlag = True

            paths = temp
            if badLoadFlag:
                warnUser("Renaming is only permitted on local ('C:') drive. Files selected from other drives not loaded")

        self._Renamer.setFileNamesMap(paths=paths)
        names = self._Renamer.getFileNames()
        self._fileListBox.clear()
        self._fileListBox.addItems(names)

    def onClearButtonPush(self):
        self.clear()

    def onExecuteButtonPush(self):
        oldText = self._replaceThisText.text()
        newText = self._replaceWithText.text()
        useRegex = self._useRegex.checkState()
        caseSensitive = self._caseSensitive.checkState()
        changeExtension = self._changeExtension.checkState()
        errorLists = self._Renamer.rename(oldText=oldText, newText=newText, regex=useRegex, caseSensitive=caseSensitive, changeExtension=changeExtension)
        if any([bool(x) for x in errorLists]):
            extraText = ""
            if errorLists[0]:
                extraText += "Permission Error for the following files:\n" + "\n".join(errorLists[0]) + "\n\n"
            if errorLists[1]:
                extraText += "The following files would have identical names after rename. Please change your regex search to be more specific:\n" + "\n".join(errorLists[1])
            warnUser(message="Some files were not renamed due to an error. See Details below.", extraText=extraText)
                

        names = self._Renamer.getFileNames()
        self._fileListBox.clear()
        self._fileListBox.addItems(names)

    def clear(self):
        self._fileListBox.clear()
        self._replaceThisText.clear()
        self._replaceWithText.clear()
        self._Renamer.clear()

    def closeEvent(self, event):
        self.saveSettings()
        super(GUI, self).closeEvent(event)

def warnUser(message, extraText=""):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setWindowTitle("Batch Renamer Warning")
    msgBox.setText(message)
    if extraText:
        msgBox.setDetailedText(extraText)
    msgBox.exec()