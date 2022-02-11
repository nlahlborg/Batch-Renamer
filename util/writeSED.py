# Author:   Nadia Ahlborg
#           nahlborg@quantumscape.com
#   
#       This script writes an IExpress Self Extraction Directive File to create a 
#       self-extracting installer. This installer ban be distributed to colleagues 
#       who do not have python installed so that they can use python applications

import sys
'''
arguments count: 4+
Argument 0: writeSED.py
Argument 1: SED file name (ex. sample.SED)
Arguement 2: App name (ex. myapp)
Argument 3: post-installation batch script
Argument 4+: other files to add to iexpress
'''

out_file = sys.argv[1]
app_name = sys.argv[2]
source_dir = sys.argv[3]
post_install_script = sys.argv[4]
files_to_add = sys.argv[5:]

with open(out_file, 'w') as fid:
    #Version Section
    print(f'[Version]\nClass=IEXPRESS\nSEDVersion=3', file=fid)
    #Options Section
    print(f'[Options]\nPackagePurpose=InstallApp\nShowInstallProgramWindow=0\nHideExtractAnimation=0\nUseLongFileName=1\n' + \
        f'InsideCompressed=0\nCAB_FixedSize=0\nCAB_ResvCodeSigning=0\nRebootMode=N\nInstallPrompt=%InstallPrompt%\n' + \
        f'DisplayLicense=%DisplayLicense%\nFinishMessage=%FinishMessage%\nTargetName=%TargetName%\n' + \
        f'FriendlyName=%FriendlyName%\nAppLaunched=%AppLaunched%\nPostInstallCmd=%PostInstallCmd%\n' + \
        f'AdminQuietInstCmd=%AdminQuietInstCmd%\nUserQuietInstCmd=%UserQuietInstCmd%\nSourceFiles=SourceFiles', file=fid)
    #Strings Section
    print(f'[Strings]\nInstallPrompt=\nDisplayLicense=\n' + \
        f'FinishMessage=Installation complete! Find your new program under Start/{app_name}\n' + \
        f'TargetName={app_name}_self_extracting_installer.EXE\n' + \
        f'FriendlyName={app_name}_self_extracting_installer\n' + \
        f'AppLaunched={post_install_script}\n' + \
        f'PostInstallCmd=cmd /c echo.\n' + \
        f'AdminQuietInstCmd=\nUserQuietInstCmd=', file=fid)
    #Files (part of strings section)
    print(f'FILE0="{post_install_script}"', file=fid)
    for idx, file in enumerate(files_to_add):
        print(f'FILE{idx+1}="{file}"', file=fid)

    #Source Files section
    print(f'[SourceFiles]', file=fid)
    print(f'SourceFiles0={source_dir}\\', file=fid)

    #Source Files 0 section
    print(f'[SourceFiles0]', file=fid)
    print(f'%FILE0%=', file=fid)
    for idx, _ in enumerate(files_to_add):
        print(f'%FILE{idx+1}%=', file=fid)


