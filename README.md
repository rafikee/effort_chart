### How to setup the Effort Chart locally
1. Navigate to the parent folder of where you want to run the program
2. Clone the repo into that folder by running 
`git clone xxxxxx`
Create the virtual environment in that folder
Navigate to where the repo exists and run this:
python3 -m venv ./venv # Will create a venv called venv
. venv/bin/activate # activate the environment
pip3 install -r requirements.txt  # install the requirements

**In terminal or bash_profile:**
export FLASK_APP=path/effort_chart/main.py
export FLASK_ENV=development
export FLASK_APP=$HOME/effort_chart/main.py

Add to effort_chart:
key.json
fbconfig.json

**Now ready:**
flask run
then access here:
http://127.0.0.1:5000/
