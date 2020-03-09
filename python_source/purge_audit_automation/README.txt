Requirements:
1. Python 3.7.2 must be installed.
2. Python 3.7.2 is added to PATH environment variable as "python"
3. Install Python Packages:
    Note: make sure pip is installed and "C:\Python37\Scripts" is added to the PATH environment variable.
	* comtypes-<current-version>
	    ** to install:
	        1. open command prompt
	        2. type pip install --proxy proxy.ptcc.design:8080 comtypes
4. Operating System must be Windows.
5. BricsCAD or AutoCAD must be installed.

How to use PURGE and AUDIT Automation Script:
1. Put the desired Drawing Folder to automate inside "input" folder.
2. Double-click "run.bat" Batch file.
3. A terminal will come out to display the logs.
	* You can also check in the logs if there are error files found.
	(it will be displayed at the end of the log if there are any.)
4. The final result will be placed inside "output" folder.

How to use Automated Fixing (Fixinator) of Layout Names:
1. Make sure output->error folder has contents (especially output->error->wrong_tab_name)
2. Double-click "run_fixinator.bat"
3. Wait for the script to check for issues. It will prompt if you want to fix errors if found.
4. Press Yes
5. It will display a prompt that the script has finished fixing issues.
6. Output will display in output->fix folder.
	
NOTE:   
	* Automated Fixer (Fixinator) only supports fixing of layout names to conventions.
	* Please empty "output" folder first before running the batch file.
	* If you want to use BricsCAD, just open a new instance application of BricsCAD.
	* You must do this exercise HOURS BEFORE submission.