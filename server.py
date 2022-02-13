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
    episodes = crud.return_episodes_in_season(season_num)
    previous_seasons_of_castaways= crud.get_previous_seasons_of_castaways(season_num)

    return render_template('season.html', seasons=all_seasons, season_num=season_num, season=season, episodes=episodes, previous_seasons_of_castaways=previous_seasons_of_castaways)

@app.route('/episode/<season_num>/<episode_num>')
def episode_page(season_num, episode_num):
    """View Episode Page."""
    all_seasons = crud.return_all_seasons()
    season = crud.return_season_details(season_num)
    episodes = crud.return_episodes_in_season(season_num)
    episode = crud.return_episode(season_num, episode_num)
    season_castaways = crud.return_season_castaways_in_season(season_num)
    vote_records = crud.get_votes_by_episode(season_num, episode_num)

    return render_template('episode.html', seasons=all_seasons, season_num=season_num, episodes=episodes, season=season, episode=episode, season_castaways=season_castaways, vote_records=vote_records)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)