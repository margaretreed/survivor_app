"""CRUD operations."""

from model import db, Castaway, Season, Episode, Season_Castaway, Vote_Record, Tribe_Map, connect_to_db

def create_castaway(full_name, short_name, date_of_birth, gender):
    """Create and return a new castaway."""

    castaway = Castaway(full_name=full_name,
                        short_name=short_name,
                        date_of_birth=date_of_birth,
                        gender=gender)

    return castaway

def create_season(season_num, season_name, location, country, tribe_setup, filming_started, filming_ended, winner_id):
    """Create and return a new season."""
    season = Season(season_num=season_num,
                    season_name=season_name,
                    location=location,
                    country=country,
                    tribe_setup=tribe_setup,
                    filming_started=filming_started,
                    filming_ended=filming_ended,
                    winner_id=winner_id)

    return season

def create_episode(season_id, episode_num, title, episode_date, num_viewers):
    """Create and return a new episode."""
    episode = Episode(season_id=season_id,
                      episode_num=episode_num,
                      title=title,
                      episode_date=episode_date,
                      num_viewers=num_viewers)

    return episode

def create_season_castaway(season_id, castaway_id, city, state, episode_voted_out, day_voted_out, order_voted_out, outcome_desc, jury_status, finalist_status, img_url):
    """Create and return a new season_castaway."""
    season_castaway = Season_Castaway(season_id=season_id,
                                      castaway_id=castaway_id,
                                      city=city,
                                      state=state,
                                      episode_voted_out=episode_voted_out,
                                      day_voted_out=day_voted_out,
                                      order_voted_out=order_voted_out,
                                      outcome_desc=outcome_desc,
                                      jury_status=jury_status,
                                      finalist_status=finalist_status,
                                      img_url=img_url)

    return season_castaway

def create_vote_record(episode, season_castaway, castaway_voted_for, immunity_status, vote_nullified, vote_desc, final_jury_vote):
    """Create and return a new vote record."""
    vote_record = Vote_Record(episode=episode,
                              season_castaway=season_castaway,
                              castaway_voted_for=castaway_voted_for,
                              immunity_status=immunity_status,
                              vote_nullified=vote_nullified,
                              vote_desc=vote_desc,
                              final_jury_vote=final_jury_vote)
    
    return vote_record

def create_tribe_map(season_castaway_id, episode_id, tribe_name, tribe_status):
    """Create and return a new tribe map."""
    tribe_map = Tribe_Map(season_castaway_id=season_castaway_id,
                          episode_id=episode_id,
                          tribe_name=tribe_name,
                          tribe_status=tribe_status)
    
    return tribe_map


def return_all_seasons():
    return Season.query.all()

def return_season_details(season_num):
    return Season.query.get(season_num)

# def return_episodes_in_season(season_num):

if __name__ == '__main__':
    from server import app
    connect_to_db(app)