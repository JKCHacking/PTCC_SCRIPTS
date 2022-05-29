ECHO ON
echo "Setting python path..."
setx path "%path%;C:\Python37;C:\Python37\Scripts;"
echo "Installing Dependencies..."
python -m pip install pywin32 Pillow comtypes pywinauto
echo "Installation Done..."
PAUSE