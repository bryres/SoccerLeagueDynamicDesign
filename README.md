# Summerville Soccer 
A teaching project for introduction to webdev and Flask.

## VSCode Setup
1) Install a recent Python 3.x version.

2) Clone the project from GitHub
    'git clone https://github.com/bryres/SoccerLeagueDynamicDesign'

3) Create a Python 3.x virtual environment. 
    Open a command prompt in the repo directory.
    'pip install virtualenv'
    'virtualenv venv'        

4) Activate the virtualenv:
    Windows: 'venv\Scripts\activate.bat'         
    Mac: 'source venv/bin/activate'

5) Install the required packages using pip.
    'pip install -r requirements.txt'

## Add the following environment variables to your system
    SOCCER_DEBUG=True
    SOCCER_SHOW_QUERIES=True
    SOCCER_SECRET_KEY=Anything -- really, anything

    # You will need to supply the values for these
    SOCCER_DB_HOST
    SOCCER_DB_SCHEMA
    SOCCER_DB_USER
    SOCCER_DB_PASSWORD
    SOCCER_DB_PORT

## Running the application
1) Open a terminal in your project directory.
2) Activate the virtual environment (Step 4 above)
3) Run 'python application.py'
