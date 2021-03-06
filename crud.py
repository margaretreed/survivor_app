"""CRUD operations."""

from model import db, Castaway, Season, Episode, Season_Castaway, Vote_Record, Tribe_Map, connect_to_db
from collections import Counter


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

def get_tribe_status_by_episode(season_num, episode_num):
    #query for tribe statuses for all season_castaways per episode -- call this function in get data route on server, then pass variable into convert data function below
    episode = return_episode(season_num, episode_num)
    tribe_assignments = Tribe_Map.query.filter(Tribe_Map.episode_id==episode.episode_id).all()

    return tribe_assignments

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

    season_items = previous_seasons_with_castaways.items()
    sorted_seasons_with_prev_castaways = sorted(season_items)

    return sorted_seasons_with_prev_castaways

def convert_voted_for_data(vote_records, season_castaways, tribe_assignments):
    """Returns dictionary with nodes and links as keys.
         
         {
             "nodes": [
                {"name": "Tony", "n": 1, "grp": 1, "id": "Tony"},
                {"name": "Sarah", "n": 1, "grp": 1, "id": "Sarah"},
                {"name": "Jake", "n": 1, "grp": 1, "id": "Jake"},
                {"name": "TonyVT", "n": 1, "grp": 0, "id": "Tony"},
                {"name": "SarahVT", "n": 1, "grp": 0, "id": "Sarah"},
                {"name": "JakeVT", "n": 1, "grp": 0, "id": "Jake"}
             ],
             "links": [
                 {"source": "Tony", "target": "SarahVT", "value": 1},
                 {"source": "Sarah", "target": "TonyVT", "value": 1},
                 {"source": "Jake", "target": "SarahVT", "value": 1}
             ]
         }
    """
    #determining the tribe names in a given episode to be able to use the index as the group value for each node on graph
    tribes_in_episode = []
    for tribe_record in tribe_assignments:
        if tribe_record.tribe_name not in tribes_in_episode:
            tribes_in_episode.append(tribe_record.tribe_name)
    # using season_castaways to add a node for every castaway in that season,
    # rather than vote_records since some castaways may not have recorded a vote that episode
    castaway_nodes = []
    for season_castaway in season_castaways:
        new_node = {}
        new_node["name"] = season_castaway.castaway.short_name
        new_node["n"] = 1
        for tribe_record in tribe_assignments:
            if tribe_record.season_castaway == season_castaway:
                #then new_node["grp"] = the index of that tribe in the tribes_in_episode list plus 1
                new_node["grp"] = tribes_in_episode.index(tribe_record.tribe_name) + 1

        new_node["id"] = season_castaway.castaway.short_name
        castaway_nodes.append(new_node)

    for season_castaway in season_castaways:
        new_node = {}
        new_node["name"] = f'{season_castaway.castaway.short_name}VT'
        new_node["n"] = 1
        new_node["grp"] = 0
        new_node["id"] = f'{season_castaway.castaway.short_name}VT'
        castaway_nodes.append(new_node)

    # loop through list of vote records and append each name as a node
    # once (may have <1 vote records for revotes or special votes)
    vote_links = []
    for vote in vote_records:
        new_link = {}
        new_link["source"] = vote.season_castaway.castaway.short_name
        new_link["target"] = f'{vote.castaway_voted_for.castaway.short_name}VT'
        new_link["value"] = 1
        vote_links.append(new_link)

    vote_records_dictionary = {
                                "nodes": castaway_nodes,
                                "links": vote_links
                              }

    return vote_records_dictionary


def get_heat_map_data(season_num, episode_num):

    season_castaways = return_season_castaways_in_season(season_num)
    season_castaway_dict = {}
    for season_castaway in season_castaways:
        short_name = season_castaway.castaway.short_name
        season_castaway_dict[short_name] = None


    episode_counter = int(episode_num)
    alliances_dict = {}
    alliance_pair_list = []

    while episode_counter >= 1:
        vote_records = get_votes_by_episode(season_num, episode_counter)

        for vote in vote_records:
            if vote.castaway_voted_for:
                castaway = vote.season_castaway.castaway.short_name
                castaway_voted_for = vote.castaway_voted_for.castaway.short_name
            if castaway_voted_for not in alliances_dict:
                alliances_dict[castaway_voted_for] = [castaway]
            else:
                alliances_dict[castaway_voted_for].append(castaway)

        #with the dict of alliances, each key represents the person voted for, and each value
        # is a list of castaways tha voted similarly that episode. Loop through the values of that list
        # to create key value pairings of those that voted similarly and append to alliance pair list
        for castaway_voted_for, castaways in alliances_dict.items():
            if len(castaways) > 1:
                for castaway in castaways:
                    for castaway_pair in castaways:
                        alliance_pair = [castaway, castaway_pair]
                        alliance_pair_list.append(tuple(alliance_pair))
        
        alliances_dict = {}
        episode_counter = episode_counter - 1

    alliance_pair_tallies = Counter(alliance_pair_list)
    # print(alliance_pair_tallies)



    heat_map_data_list = []
    for pair_set, value in alliance_pair_tallies.items():
        pair_list = list(pair_set)
        pair_list.append(value)
        heat_map_data_list.append(pair_list)

    # heat_map_data = {
    #             "values": {
    #                 "data": heat_map_data_list
    #             }
    #         }
    heat_map_data = {
                "castaways": season_castaway_dict,
                "data": heat_map_data_list
                }
    
    
    print(heat_map_data)


    return heat_map_data
