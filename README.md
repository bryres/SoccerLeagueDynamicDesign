# Summerville Soccer 
A teaching project for introduction to webdev and Flask.
`*Please use a Python 3.x virtual environment to avoid version issues`

## PyCharm Setup
1) Install a recent Python 3.x version.
2) Clone the project from GitHub
3) Create a Python 3.x virtual environment (do not add to Git!)
4) From the terminal inside PyCharm run "pip install requirements.txt".  Alternatively, open requirements.txt and PyCharm will likely prompt you to install the requirements.
5) Copy config.py to bca_web directory but do not add to GitHub.  (Ideally we will move this file up a directory soon.)

## Running in Pycharm

## Windows Instructions
set FLASK_APP=soccer.py
set FLASK_DEBUG=True
flask run

## Mac Instructions
export FLASK_APP=bca_web.py
export FLASK_DEBUG=True
flask run

## Alternative Command Line Setup / Running
1. `cd bca_web` - Navigate to the folder
2. MAC OSX - `brew install mysql` \
   Windows - `https://dev.mysql.com/downloads/windows/installer/8.0.html`
             `https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python`
3. `python setup.py install` OR `pip install requirements.txt` OR `CLICK install dependencies if using PyCharm`
4. MAC OSX - `export FLASK_APP=soccer.py` \
   Windows - `set FLASK_APP=soccer.py`
5. `flask run`

### Debug Mode
Debug mode makes testing a lot easier and displays errors.\
**Always make sure to keep debug mode ON during Development and OFF during Production** \
`export FLASK_DEBUG=True`

