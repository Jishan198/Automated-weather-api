@echo off
REM 1. Activate the virtual environment
call "C:\Users\zayhe\OneDrive\Documents\backend_project_01\venv\Scripts\activate.bat"

REM 2. Navigate to the Django project folder containing manage.py
cd "C:\Users\zayhe\OneDrive\Documents\backend_project_01\data_dashboard"

REM 3. Run the custom management command
python manage.py fetch_weather

REM 4. Deactivate the environment
deactivate