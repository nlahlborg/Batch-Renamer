# Batch Renamer

Batch Renamer allows you to rename a large number of files at once.

## Installation

You can use Batch Renamer as a python application or as a stand-alone application.

### Install as a standalone app.
NO python installation or coding is needed to run this program as a standalone app.
1. Download Batch_Renamer_self_extracting_installer.exe
2. Run the self extracting installer
3. Verify correct installation by launching the program from the Start Menu

### Install for use with Python
1. Setup environment with conda 
    ```conda env create -f setup\environment.yml```
OR
2. Setup environment with pip 
    ```python3 -m venv batch_renamer_prod```
    ```pip install -r setup\requirements.txt```

## Usage
### Python GUI
Launch the app from the command line:
```python batch_renamer.py```

### Standalone GUI
Launch Batch Renamer from the start menu

### Using the GUI
The GUI interface is fairly simple. To change a set of characters in a batch of files, use the following steps:
1. Click the "Open" button (or use the keyboard shortcut Ctrl+O) and search for a group of files that you want to rename. The names of these files will appear in the white box below. 
2. In the "Replace This Text" field, type the characters that you want to replace
3. In the "Replace With Text" field, type the characters you want to appear in the new file names.
4. Select additional options:
    * "Use Regex?" uses regex instead of plain text
    * "Case Sensitive?" allows case-sensitive search and replace. <b><i>If you uncheck this box, you will create file names with only lower-case characters. </i></b>
    * "Change Extension?" Check this box if you want to include change the file extension in search and replace. The default setting ignores the file extension.
5. Click "Execute Rename" to search for the text from step 2 and replace all instances with the text from step 3. 

In the example below, clicking "Execute Rename" will replace the phrase "Ar_typo" in the last three files with "Ar_A". 

| ![GUI screencap](images\example.png) |
| --- | 
| Figure 1: Example Batch Renamer GUI |


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Updating the standalone installer
If you made changes to the python code, you can re-build the installer and stand-alone app by running publish_batch_renamer.bat from the command line (requires conda package manager). This will use pyinstaller to bundle the application and dependancies, and zip them into a self-extracting installer that will install them to a specified folder. 