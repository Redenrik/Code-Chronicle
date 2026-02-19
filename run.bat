@echo off
setlocal

if not exist .venv (
    echo Creating virtual environment in the project folder...
    py -3 -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies from requirements.txt...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Running Code Chronicle...
python src\gui.py
