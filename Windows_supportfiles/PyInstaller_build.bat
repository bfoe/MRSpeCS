C:\Python27\scripts\pyinstaller PyInstaller.spec
rmdir /Q /S ..\Windows_binary\*.*
mkdir ..\Windows_binary\*.*
copy /Y dist\MRSpeCS.exe ..\Windows_binary\*.*
copy /Y README_Windows.txt ..\Windows_binary\*.*
copy /Y ..\MRSpeCS.py ..\Windows_binary\*.*
rmdir /Q /S build
rmdir /Q /S dist
pause
