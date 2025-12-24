# Windows Compile Commands


##  Compile Commands

1. Move to project directory

2. Activate virtual environment
```
.\.venv\Scripts\activate
```
2. Move to Windows release directory
```
cd windows_release
```
3. Remove previous install 
```
rmdir /s /q build
rmdir /s /q dist
```
4. Use PyInstaller to generate file
```
python -m PyInstaller --onefile ../src/SleepScienceViewerApp.py
```