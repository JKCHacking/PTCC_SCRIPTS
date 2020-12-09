import zipfile
import shutil
import os
import sys

macro_name = sys.argv[1]
spreadsheet_name = sys.argv[2]

print("Delete and create directory with_macro")
shutil.rmtree("with_macro", True)
os.mkdir("with_macro")

file_name = "with_macro/" + spreadsheet_name
print("Open File " + spreadsheet_name)
shutil.copyfile(spreadsheet_name, file_name)

doc = zipfile.ZipFile(file_name, 'a')
doc.write(macro_name, "Scripts/python/" + macro_name)

manifest = []
for line in doc.open('META-INF/manifest.xml'):
    if '</manifest:manifest>' in line.decode('utf-8'):
        for path in ['Scripts/', 'Scripts/python', 'Scripts/python/' + macro_name]:
            manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="%s"/>' 
                            % path)
    manifest.append(line.decode('utf-8'))

doc.writestr('META-INF/manifest.xml', ''.join(manifest))
doc.close()
print("File created: %s".format(file_name))
