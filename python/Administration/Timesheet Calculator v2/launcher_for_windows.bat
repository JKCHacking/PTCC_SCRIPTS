ECHO ON
echo "Starting Timesheet Calculator..."
python "%~dp0\Timesheet Calculator v2\main.py"
if %ERRORLEVEL% neq 0 (do python3.6 "%~dp0\Timesheet Calculator v2\main.py")
PAUSE