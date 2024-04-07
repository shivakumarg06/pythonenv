@echo off

REM Create the virtual environment
python -m venv venv

REM Activate the virtual environment
call .\venv\Scripts\activate

REM Install the required packages in this virtual environment
pip install -r requirements.txt

REM Run your Python script in this virtual environment
python fetchData_Store.py
python readData.py