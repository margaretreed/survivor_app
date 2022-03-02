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
    """Return all seasons in the db"""
    return Season.query.all()

def return_season_details(season_num):
     """Return a season object by it's season number"""
     return Season.query.get(season_num)

def return_episodes_in_season(season_num):
    """Return all episodes in a season"""
    season = Season.query.get(season_num)
    return season.episodes

def return_episode(season_num, episode_num):
    """Return an episode"""
    episode = db.session.query(Episode).join(Season).filter(Season.season_num==season_num, Episode.episode_num==episode_num).first()
    return episode

def return_season_castaways_in_season(season_num):
    season = Season.query.get(season_num)
    return season.season_castaways

def get_votes_by_episode(season_num, episode_num):
    episode = return_episode(season_num, episode_num)
    vote_records = Vote_Record.query.filter(Vote_Record.episode_id==episode.episode_id).all()

    return vote_records


def get_previous_seasons_of_castaways(season_num):
    """Returns dictionary of seasons as keys, and castaways that appear in those seasons as values"""
    season = Season.query.get(season_num)
    
    # query all seasons that castaway id appears where season_num is less than season parameter
    
    previous_seasons_with_castaways = {}

    # all season_castaways in current season
    season_castaways = season.season_castaways

    for season_castaway in season_castaways:
        # get castaway object associated with that season_castaway
        castaway = season_castaway.castaway
        # get all season_castaway objects associated with that castaway
        season_castaways_by_castaway_id = castaway.season_castaways

        for season_castaway_by_castaway_id in season_castaways_by_castaway_id:
            if season_castaway_by_castaway_id.season_id < int(season_num):
                # add season as key and list of castaway objects as value to the dict
                if season_castaway_by_castaway_id.season_id not in previous_seasons_with_castaways:
                    previous_seasons_with_castaways[season_castaway_by_castaway_id.season_id] = [season_castaway_by_castaway_id.castaway]
                else:
                    previous_seasons_with_castaways[season_castaway_by_castaway_id.season_id].append(season_castaway_by_castaway_id.castaway)

    return previous_seasons_with_castaways

def convert_voted_for_data(vote_records, season_castaways):
    """Returns dictionary with nodes and links as keys.
         
         {
             "nodes": [
                 {"id": "Tony"},
                 {"id": "Sarah"}
                 {"id": "Jake"}
             ],
             "links": [
                 {"source": "Tony", "target": "Sarah"},
                 {"source": "Sarah", "target": "Tony"},
                 {"source": "Jake", "target": "Sarah"}
             ]
         }
    """
    # using season_castaways to add a node for every castaway in that season,
    # rather than vote_records since some castaways may not have recorded a vote that episode
    castaway_nodes = []
    for season_castaway in season_castaways:
        new_node = {}
        new_node["id"] = season_castaway.castaway.short_name
        castaway_nodes.append(new_node)
    
    # loop through list of vote records and append each name as a node
    # once (may have <1 vote records for revotes or special votes)
    vote_links = []
    for vote in vote_records:
        new_link = {}
        new_link["source"] = vote.season_castaway.castaway.short_name
        new_link["target"] = vote.castaway_voted_for.castaway.short_name
        vote_links.append(new_link)

    vote_records_dictionary = {
                                "nodes": castaway_nodes,
                                "links": vote_links
                              }

    return vote_records_dictionary

        






    
