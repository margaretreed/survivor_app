"""Data model for survivor app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Castaway(db.Model):
    """A castaway."""

    __tablename__ = "castaways"

    castaway_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    full_name = db.Column(db.String(40), nullable=False)
    short_name = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.String(15))

    # Castaway.won_seasons returns a list of season objects won by that castaway
    won_seasons = db.relationship("Season", back_populates="winner")
    # season_castaways = a list of season_castaway objects associated with that castaway

    def __repr__(self):
        return f'<Castaway castaway_id={self.castaway_id} full_name={self.full_name}>'

class Season(db.Model):
    """A season."""

    __tablename__ = "seasons"

    season_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    season_num = db.Column(db.Integer)
    season_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    tribe_setup = db.Column(db.String(200))
    filming_started = db.Column(db.DateTime)
    filming_ended = db.Column(db.DateTime)
    winner_id = db.Column(db.Integer, db.ForeignKey("castaways.castaway_id"))

    # episodes = a list of episode objects from that season
    # season_castaways = a list of season_castaway objects from that season


    # Access winner via Season object to return object of castaway associated with that primary key
    # season = Season.query.get(1) --> gets a season with the primary key 1
    # season.winner --> returns the castaway object of the winner
    winner = db.relationship("Castaway", back_populates="won_seasons")
 
    def __repr__(self):
        return f'<Season season_id={self.season_id} season_name={self.season_name}>'

class Season_Castaway(db.Model):
    """An association table for each season's castaways."""

    __tablename__ = "season_castaways"

    season_castaway_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    season_id = db.Column(db.Integer, db.ForeignKey("seasons.season_id"))
    castaway_id = db.Column(db.Integer, db.ForeignKey("castaways.castaway_id"))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    episode_voted_out = db.Column(db.Integer)
    day_voted_out = db.Column(db.Integer)
    order_voted_out = db.Column(db.Integer)
    outcome_desc = db.Column(db.String(30))
    jury_status = db.Column(db.String(20))
    finalist_status = db.Column(db.Boolean)
    img_url = db.Column(db.String(200))

    # vote_history_voter = list of Vote_Record objects associated with that season_castaway
    # vote_for_history = list of Vote_Record objects 
    # tribe_map = list of Tribe_Map objects associated with that Season_Castaway


    # Access season object from the season_castaway object
    # season_castaway = Season_Castaway.query.get(1) --> queries the season_castaway object with primary key as 1
    # season_castaway.season --> returns the season object associated with that season_castaway
    season = db.relationship("Season", backref="season_castaways")

    # Access castaway object from the season_castaway object
    # season_castaway = Season_Castaway.query.get(1) --> queries the season_castaway object with primary key as 1
    # season_castaway.castaway --> returns the castaway object associated with that season_castaway
    castaway = db.relationship("Castaway", backref="season_castaways")

    def __repr__(self):
        return f'<Season_Castaway season_castaway_id={self.season_castaway_id} order_voted_out={self.order_voted_out}>'

class Episode(db.Model):
    """An Episode."""

    __tablename__ = "episodes"

    episode_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    season_id = db.Column(db.Integer, db.ForeignKey("seasons.season_id"))
    episode_num = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100))
    episode_date = db.Column(db.DateTime)
    num_viewers = db.Column(db.Float, nullable=True)

    # vote_history = list of Vote_Record objects from that episode
    # tribe_map = list of Tribe_Map objects associated with that episode

    # Access season object from the episode object
    # episode = Episode.query.get(1) --> queries the episode object with primary key as 1
    # episode.season --> returns the season object associated with that episode
    season = db.relationship("Season", backref="episodes")


    def __repr__(self):
        return f'<Episode episode_id={self.episode_id} title={self.title}>'

class Vote_Record(db.Model):
    """A record of how a castaway votes each episode."""

    __tablename__ = "vote_history"

    vote_record_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.episode_id"))
    season_castaway_id = db.Column(db.Integer, db.ForeignKey("season_castaways.season_castaway_id"))
    castaway_voted_for_id = db.Column(db.Integer, db.ForeignKey("season_castaways.season_castaway_id"))
    immunity_status = db.Column(db.String(20))
    vote_nullified = db.Column(db.Boolean)
    vote_desc = db.Column(db.String(20))
    final_jury_vote = db.Column(db.Boolean)

    # Access episode object from the Vote_Record object
    # vote_record = Vote_Record.query.get(1) --> queries the vote_record object with primary key as 1
    # vote_record.episode--> returns the episode object associated with that vote_record
    episode = db.relationship("Episode", backref="vote_history")


    # Access season_castaway object from the Vote_Record object
    # vote_record = Vote_Record.query.get(1) --> queries the vote_record object with primary key as 1
    # vote_record.season_castaway--> returns the season_castaway object associated with that vote_record
    season_castaway = db.relationship("Season_Castaway", foreign_keys="Vote_Record.season_castaway_id", backref="vote_history_voter")

    # DO I EVEN NEED THIS RELATIONSHIP?
    # Access season_castaway object of the person voted for from the Vote_Record object
    # vote_record = Vote_Record.query.get(1) --> queries the vote_record object with primary key as 1
    # vote_record.season_castaway_voted_for--> returns the season_castaway object associated with who was voted for in that vote_record
    castaway_voted_for = db.relationship("Season_Castaway", foreign_keys="Vote_Record.castaway_voted_for_id", backref="vote_history_votee")

    def __repr__(self):
        return f'<Vote_Record vote_record_id={self.vote_record_id} castaway_voted_for_id={self.castaway_voted_for_id}>'

class Tribe_Map(db.Model):
    """A record of how a castaway votes each episode."""

    __tablename__ = "tribe_mapping"

    tribe_map_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,)
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.episode_id"))
    season_castaway_id = db.Column(db.Integer, db.ForeignKey("season_castaways.season_castaway_id"))
    tribe_name = db.Column(db.String(20))
    tribe_status = db.Column(db.String(20))


    # Access Episode object from the Tribe_Map object
    # tribe_map = Trib_Map.query.get(1) --> queries the Tribe_Map object with primary key as 1
    # tribe_map.episode--> returns the episode object associated with that tribe_map
    episode = db.relationship("Episode", backref="tribe_map")

    # Access Season_Castaway object from the Tribe_Map object
    # tribe_map = Trib_Map.query.get(1) --> queries the Tribe_Map object with primary key as 1
    # tribe_map.season_castaway--> returns the season_castaway object associated with that tribe_map
    season_castaway = db.relationship("Season_Castaway", backref="tribe_map")


    def __repr__(self):
        return f'<Tribe_Map tribe_map_id={self.tribe_map_id} tribe_name={self.tribe_name}>'


def connect_to_db(flask_app, db_uri="postgresql:///survivor", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)