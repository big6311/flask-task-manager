@echo off
cd /d "C:\Users\Bryan\OneDrive\Desktop\First API project"
start "" http://127.0.0.1:5000/tasks
python task_api.py
pause
