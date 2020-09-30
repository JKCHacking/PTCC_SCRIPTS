Changes:
1. It outputs 1 PDF = 1 DXF File. (You need to put profiles inside dxf file)
This is better because you can easily control the output pdf files especially if you
have alot of dxf files as input.
2. removed the -files parameter. instead expect the input files
in the input folder and output files in the output folder.
3. changed the module structure to make them testable
4. added alot of test cases. located in the test folder

5. Notes to consider:
For Inconsistent number of material to the number of profile inside the dxf file.
    2.1 material = 0, profile = 2 -> no materials will be implemented on the profiles
    2.2 material = 1, profile = 2 -> material 1 will be used on the both profiles
    2.3 material = 2, profile = 2 -> material 1 to profile 1, material 2 to profile 2
    2.4 material = 2, profile = 3 -> material 1 to profile 1, material 2 to profile 2,
                                     material 2 to profile 3.
    2.5 material = 3, profile = 2 -> material 1 to profile 1, material 2 to profile 2,
                                     material 3 will be disregarded.
6. Used Pymupdf as the PDF handler package for the script. (might change to reportlab in the future to support tabbing)
to install: pip install PyMuPDF

7. Please uninstall your sectionproperties in pip as this is still not updated
based from the original source code in github. sectionproperties is already included in the
project. if the new sectionproperties version is released just delete the sectionpropeties
folder in the project and update the new version using pip install and used that instead.

Usage:
1. copy dxf file to input folder
2. run the script command
3. check the output folder for the output report pdf.
4. use --help/-h to know the arguments

Sample Script command:

1.
+----# for long report and profiles expected to have holes.
+----python path/to/DrawingSectionProperty/main.py -long -hole

2.
+----# for short report and profiles expected to have holes.
+----python path/to/DrawingSectionProperty/main.py -hole