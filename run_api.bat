@echo off
cd /d "C:\Users\Bryan\Desktop\First API project"

:: Open browser to the UI
start "" http://127.0.0.1:5000/

:: Start the Task API
python task_api.py

pause
