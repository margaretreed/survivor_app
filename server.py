"""Server for survivor app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""
    all_seasons = crud.return_all_seasons()
    return render_template('homepage.html', seasons=all_seasons)

@app.route('/season/<season_num>')
def season_page(season_num):
    """View Season Page."""
    all_seasons = crud.return_all_seasons()
    season = crud.return_season_details(season_num)
    # episodes = crud.return_episodes_in_season(season_num)

    #query for season name, location, tribe set up, winner
    #query for all episodes in that season
    return render_template('season.html', seasons=all_seasons, season_num=season_num, season=season)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)