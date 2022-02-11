@ECHO OFF
REM script to publish the app as an exe file

REM Set variables here
SET envName=batch_renamer_prod
SET appName=Batch_Renamer
SET pythonScriptName=batch_renamer.py

REM ------------- shouldn't need to modify below this line ---------------------
TITLE Publish %appName%

REM change to the correct prod conda environement
CALL activate %envName%
ECHO You have activated the following environment:
CALL conda info --env

REM use pyinstaller to create a fozen version of the app as an exe
ECHO Using pyinstaller to bundle the app. This may take a while....
pyinstaller %pythonScriptName%^
    --specpath ".\util" --distpath ".\dist" --workpath ".\build"^
    --clean --noconfirm --log-level WARN --name %appName% --noconsole^
    --add-data "..\settings\default_settings.json;settings"^
    --add-data "..\qss\stylesheet.qss;qss"^
    --add-data "..\images\icon.png;images"^
    --icon "..\images\icon.ico"

REM use powershell to compress all the files except except the decompression script
ECHO using powershell Compress-Archive to create a zip folder
Powershell.exe Compress-Archive -Path '.\dist\%appName%' -DestinationPath '.\util\%appName%.zip' -Force

REM use a python program to build the setup file for iexpress cabinet maker. The syntax is
REM python writeSED.py outfileName appName sourceDir ExpandArchiveScriptName otherFile1 otherFile2 ...
python util\writeSED.py util\%appName%.SED %appName% "%CD%\util" install_%appName%.cmd %appName%.zip

REM use iexpress cabinet maker to compress all the files into a self extracting installer
REM ** this might seem kind of roundabout, but self extracting installers bundled via cabinet maker 
REM are less likely to make anti-virus programs angry!
ECHO using iexpress cabinet maker to create a self-extracting installer. This will open a seperate window (and can take several minutes). 
iexpress /N util/%appName%.SED


