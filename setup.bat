@echo off

echo Setting up bot...
cd bot
python -m venv .venv

echo Installing bot packages...
call .venv\Scripts\activate
echo Upgrade Pip...
python.exe -m pip install --upgrade pip > nul
pip install -r requirements.txt
call deactivate

echo Finished bot...

exit