# Author:   Nadia Ahlborg
#           nahlborg@quantumscape.com
#   
#       This is a set of functions for renaming a lot of files at once

import pandas as pd
from os.path import splitext, split, join
from os import rename
import re

class Renamer():
    def __init__(self, verbose=False):
        
        self._fileNamesMap = pd.DataFrame({"fullpath":[], "basepath": [], "name":[]})   

    def setFileNamesMap(self, paths):
        df = pd.DataFrame({"fullpath":[], "basepath": [], "name":[]})   
        df["fullpath"] = paths
        df["name"] = df["fullpath"].apply(lambda x: split(x)[-1])
        df["basepath"] = df["fullpath"].apply(lambda x: split(x)[0])

        df = pd.concat([ self._fileNamesMap, df])
        df = df.drop_duplicates(ignore_index=True)
        df.sort_values("name", axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        self._fileNamesMap = df

    def rename(self, oldText, newText, regex=False, caseSensitive=False, changeExtension=False):
        permissionErrorList = []
        fileExistsErrorList = []
        for idx in range(len(self._fileNamesMap)):
            if changeExtension:
                oldName = self._fileNamesMap.iloc[idx].loc["name"]
                ext = ""
            else:
                oldName, ext = splitext(self._fileNamesMap.iloc[idx].loc["name"])
            
            if oldText.lower() in oldName.lower() or re.search(oldText, oldName, flags=re.IGNORECASE):
                if regex:
                    if caseSensitive:
                        newName = re.sub(oldText, newText, oldName)
                    else:
                        newName = re.sub(oldText, newText, oldName, flags=re.IGNORECASE)

                else:
                    if not(caseSensitive):
                        oldName = oldName.lower()
                        oldText = oldText.lower()
                        newText = newText.lower()

                    newName = oldName.replace(oldText, newText)
                
                #add extension back
                newName = newName + ext

                oldPath = self._fileNamesMap.iloc[idx].loc["fullpath"]
                newPath = join(self._fileNamesMap.iloc[idx].loc["basepath"], newName)

                try:
                    rename(oldPath, newPath)
                    self._fileNamesMap.iloc[idx].loc["name"] = newName
                    self._fileNamesMap.iloc[idx].loc["fullpath"] = newPath     
                except PermissionError:
                    permissionErrorList.append(oldName)
                except FileExistsError:
                    fileExistsErrorList.append(oldName)

        return permissionErrorList, fileExistsErrorList

    def getFileNamesMap(self):
        return self._fileNamesMap

    def getFileNames(self):
        return self._fileNamesMap["name"].values

    def clear(self):
        self._fileNamesMap = pd.DataFrame({"fullpath":[], "basepath": [], "name":[]})   
