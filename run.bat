@echo off

if not exist env (
    echo Creating virtual environment in the project folder...
    python -m venv env
)

call env\Scripts\activate.bat

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Running the Project Explorer script...
python src\gui.py

echo Done.
pause