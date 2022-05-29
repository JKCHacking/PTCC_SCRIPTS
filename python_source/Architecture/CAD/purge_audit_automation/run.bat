ECHO ON
SET PATH=%PATH%;C:\Python37
python %~dp0\src\purge_audit_script.py
python %~dp0\src\drawing_fixinator.py
PAUSE