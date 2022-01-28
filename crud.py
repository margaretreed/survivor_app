"""CRUD operations."""

from model import db, Castaway, Season, Episode, Season_Castaway, Vote_Record, Tribe_Map, connect_to_db

def create_castaway(full_name, first_name, date_of_birth, city, state):
    """Create and return a new castaway."""

    castaway = Castaway(full_name=full_name,
                        first_name=first_name,
                        date_of_birth=date_of_birth,
                        city=city,
                        state=state)

    return castaway

def create_season(season_num, season_name, location_city, location_country, tribe_setup, filming_started, filming_ended, winner_id):
    """Create and return a new season."""
    season = Season(season_num=season_num,
                    season_name=season_name,
                    location_city=location_city,
                    location_country=location_country,
                    tribe_setup=tribe_setup,
                    filming_started=filming_started,
                    filming_ended=filming_ended,
                    winner_id=winner_id)
    
    return season

def create_episode(season_id, episode_num, day_num, episode_date, num_viewers, vote_outcome):
    """Create and return a new episode."""
    episode = Episode(season_id=season_id, 
                      episode_num=episode_num,
                      day_num=day_num,
                      episode_date=episode_date,
                      num_viewers=num_viewers,
                      vote_outcome=vote_outcome)
    
    return episode

def create_season_castaway(season_id, castaway_id, episode_voted_out, day_voted_out, order_voted_out, jury_status, finalist_status):
    """Create and return a new season_castaway."""
    season_castaway = Season_Castaway(season_id=season_id,
                                      castaway_id=castaway_id,
                                      episode_voted_out=episode_voted_out,
                                      day_voted_out=day_voted_out,
                                      order_voted_out=order_voted_out,
                                      jury_status=jury_status,
                                      finalist_status=finalist_status)
    
    return season_castaway

def create_vote_record(episode_id,season_castaway_id, castaway_voted_for_id, immunity_status, vote_nullified, final_jury_vote):
    """Create and return a new vote record."""
    vote_record = Vote_Record(episode_id=episode_id,
                              season_castaway_id=season_castaway_id,
                              castaway_voted_for_id=castaway_voted_for_id,
                              immunity_status=immunity_status,
                              vote_nullified=vote_nullified,
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



if __name__ == '__main__':
    from server import app
    connect_to_db(app)