@ECHO OFF
REM this script unzips an compressed archive to a predefined installation location
REM on the user's computer and creates a shortcut in the start menu.

REM Variables
SET appName=Batch_Renamer
SET dest=C:\Program Files\SIC_Python

REM ------------------- shouldn't need to change anything below this line ----------------

REM extract the archive that was created by compress-archive in the publish app_name script 
ECHO Extracting files to the installation directory %dest% ... 
Powershell.exe $global:ProgressPreference = 'SilentlyContinue'; Expand-Archive -Path '%appName%.zip' -DestinationPath '%dest%' -Force
ECHO Extraction complete.

REM create a start menu shortcut
ECHO Creating a shortcut in the start menu
Powershell.exe $WScriptShell = New-Object -ComObject WScript.Shell;^
    $Shortcut = $WScriptShell.CreateShortcut('C:\Users\%UserName%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\%appName%.lnk');^
    $Shortcut.TargetPath = '%dest%\%appName%\%appName%.exe';^
    $Shortcut.WorkingDirectory = '%dest%\%appName%';^
    $Shortcut.Save()
