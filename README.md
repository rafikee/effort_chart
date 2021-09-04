### How to setup the Effort Chart locally
1. Navigate to the parent folder of where you want to run the program
2. Clone the repo into that folder by running 
`git clone https://github.com/rafikee/effort_chart.git`
3. Navigate into the newly cloned folder and create the python environment
`python3 -m venv ./venv`
4. Navigate back to the root of the repo and activate the new environment
`. venv/bin/activate`
5. Install the requirements
`pip3 install -r requirements.txt`

6. Add these lines to your bash_profile (adjust the path as needed):

`export FLASK_APP=$HOME/effort_chart/main.py`

`export FLASK_ENV=development`

`export FLASK_APP=$HOME/effort_chart/main.py`

7. Exit the terminal and re-enter to apply the updated bash_profile.

8. Add to these two files to the repo folder:

`key.json`

`fbconfig.json`

9. Start up the flask server locally `flask run`

10. Access the application here: http://127.0.0.1:5000/

