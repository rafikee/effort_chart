from flask import Flask
from flask import render_template
import pandas as pd

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# test deploy
@app.route('/', methods=['GET'])
def hello():
    df = pd.read_csv('chart_input.csv', dtype=object)
    stats = list(df['stats'].dropna())
    cols = stats.copy()
    cols.insert(0, ' ')
    players = ['#' + player for player in list(df['players'].dropna())]
    return render_template('chart.html', plyrs=players, cols=cols, stats=stats)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
