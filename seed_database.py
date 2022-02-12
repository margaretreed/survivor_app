"""Script to seed database."""

import os
import csv
import pandas as pd
from datetime import datetime

import crud
import model
import server

os.system("dropdb survivor")
os.system('createdb survivor')

model.connect_to_db(server.app)
model.db.create_all()


castaway_details_df = pd.read_csv('data/castaway_details.csv', usecols=["full_name",
                                                                        "short_name",
                                                                        "date_of_birth",
                                                                        "gender"])
castaways_in_db = []

for index, row in castaway_details_df.iterrows():
    full_name = row['full_name']
    short_name = row['short_name']
    date_of_birth = row['date_of_birth']
    gender = row['gender']
    # print(full_name, short_name, date_of_birth, gender)

    created_castaway = crud.create_castaway(full_name,
                                            short_name,
                                            date_of_birth,
                                            gender)
    
    castaways_in_db.append(created_castaway)

#print(castaways_in_db)
model.db.session.add_all(castaways_in_db)
model.db.session.commit()

#create seasons db with winner matched to castaway object

season_summary_df = pd.read_csv('data/season_summary.csv', usecols=["season_name",
                                                                        "season",
                                                                        "location",
                                                                        "country",
                                                                        "tribe_setup",
                                                                        "winner_id",
                                                                        "filming_started",
                                                                        "filming_ended"])

seasons_in_db = []

for index, row in season_summary_df.iterrows():
    season_name = row['season_name']
    season_num = row['season']
    location = row['location']
    country = row['country']
    tribe_setup = row['tribe_setup']
    winner = row['winner_id']
    #filter for castaway object by winner_id
    winner = model.Castaway.query.get(winner)
    winner_id = winner.castaway_id
    filming_started_str = row['filming_started']
    filming_ended_str = row['filming_ended']
    str_format= "%Y-%m-%d"
    filming_started = datetime.strptime(filming_started_str, str_format)
    filming_ended = datetime.strptime(filming_ended_str, str_format)

    created_season = crud.create_season(season_num,
                                        season_name,
                                        location,
                                        country,
                                        tribe_setup,
                                        filming_started,
                                        filming_ended,
                                        winner_id)
    
    seasons_in_db.append(created_season)

model.db.session.add_all(seasons_in_db)
model.db.session.commit()

# create season_castaways db
castaways_df = pd.read_csv('data/castaways.csv', usecols=["season",
                                                        "castaway_id",
                                                        "city",
                                                        "state",
                                                        "episode",
                                                        "day",
                                                        "order",
                                                        "result",
                                                        "jury_status",
                                                        "finalist",
                                                        "immunity_idols_won",
                                                        "img_url"])

season_castaways_in_db = []

for index, row in castaways_df.iterrows():
    season = row['season']
    season = model.Season.query.get(season)
    season_id = season.season_id
    castaway = row['castaway_id']
    castaway = model.Castaway.query.get(castaway)
    castaway_id = castaway.castaway_id
    city = row['city']
    state = row['state']
    episode_voted_out = row['episode']
    day_voted_out = row['day']
    order_voted_out = row['order']
    outcome_desc = row['result']
    jury_status = row['jury_status']
    finalist_status = row['finalist']
    img_url = row['img_url']

    created_season_castaway = crud.create_season_castaway(season_id,
                                                            castaway_id,
                                                            city, state,
                                                            episode_voted_out,
                                                            day_voted_out,
                                                            order_voted_out,
                                                            outcome_desc,
                                                            jury_status,
                                                            finalist_status,
                                                            img_url)
  
    season_castaways_in_db.append(created_season_castaway)

model.db.session.add_all(season_castaways_in_db)
model.db.session.commit()

#create episodes table

viewers_df = pd.read_csv('data/viewers.csv', usecols=["season",
                                                        "episode",
                                                        "episode_title",
                                                        "episode_date",
                                                        "viewers"])

episodes_in_db = []

for index, row in viewers_df.iterrows():
    season = row['season']
    season = model.Season.query.get(season)
    season_id = season.season_id
    episode_num = row['episode']
    title = row['episode_title']
    episode_date = row['episode_date']
    num_viewers = row['viewers']
    #print(type(num_viewers))

    created_episode = crud.create_episode(season_id,
                                            episode_num,
                                            title,
                                            episode_date,
                                            num_viewers)

    episodes_in_db.append(created_episode)

model.db.session.add_all(episodes_in_db)
model.db.session.commit()

#create vote_history table
vote_history_df = pd.read_csv('data/vote_history.csv', usecols=["season",
                                                        "episode",
                                                        "castaway_id",
                                                        "vote_id",
                                                        "immunity",
                                                        "nullified",
                                                        "vote",
                                                        "jury_vote"])

vote_records_in_db = []

for index, row in vote_history_df.iterrows():
    season_num = row['season']
    season = model.Season.query.get(season_num)
    season_id = season.season_id

    episode = row['episode']
    episode_list = model.db.session.query(model.Episode).join(model.Season).filter(model.Season.season_num==season_num, model.Episode.episode_num==episode).all()
    episode = episode_list[0]

    castaway_id = row["castaway_id"]

    #querying for all season_castaway objects with matching castaway_id and season_id
    #getting results with two castaway_season records for castaways that were voted out then came back in a later episode
    season_castaway_list = model.Season_Castaway.query.filter(model.Season_Castaway.castaway_id==castaway_id, model.Season_Castaway.season_id==season_num).all()
    season_castaway = None
    # if episode of vote_record <= episode_voted_out of the season_castaway object
    # then current season_castaway object is the castaway id of that vote_record
    for season_castaway_item in season_castaway_list:
        if episode.episode_num <= season_castaway_item.episode_voted_out:
            season_castaway = season_castaway_item

    castaway_voted_for = row['vote_id']
    #results of this query produce multiple season_castaways if a castaway was voted out then came back at a later episode,
    #and produces 0 results for various reasons a season_castaway was unable to cast a vote- see vote description for more info
    castaway_voted_for_list = model.Season_Castaway.query.filter(model.Season_Castaway.castaway_id==castaway_voted_for, model.Season_Castaway.season_id==season_num).all()
    castaway_voted_for = None

    if not castaway_voted_for_list:
        castaway_voted_for = None
    
    for castaway_voted_for_item in castaway_voted_for_list:
        if episode.episode_num <= castaway_voted_for_item.episode_voted_out:
            castaway_voted_for = castaway_voted_for_item
    
    immunity_status = row['immunity']
    vote_nullified = row['nullified']
    vote_desc = row['vote']
    final_jury_vote = row['jury_vote']

    created_vote_record = crud.create_vote_record(episode,
                                                    season_castaway,
                                                    castaway_voted_for,
                                                    immunity_status,
                                                    vote_nullified,
                                                    vote_desc,
                                                    final_jury_vote)

    vote_records_in_db.append(created_vote_record)

jury_votes_df = pd.read_csv('data/jury_votes.csv', usecols=["season",
                                                        "finalist",
                                                        "castaway_id",
                                                        "finalist_id",
                                                        "jury_vote",])

for index, row in jury_votes_df.iterrows():
    season_num = row['season']
    vote_desc = row['finalist']
    castaway_id = row['castaway_id']
    #query for season castaway object with that id and season
    season_castaway_list = model.Season_Castaway.query.filter(model.Season_Castaway.castaway_id==castaway_id, model.Season_Castaway.season_id==season_num).all()
    #first item in list is the season_castaway record that cast the final vote
    season_castaway = season_castaway_list[0]

    castaway_voted_for_id = row['finalist_id']
    castaway_voted_for_list = model.Season_Castaway.query.filter(model.Season_Castaway.castaway_id==castaway_voted_for_id, model.Season_Castaway.season_id==season_num).all()
    castaway_voted_for = castaway_voted_for_list[0]
    final_jury_vote = row['jury_vote']

    episode = None
    immunity_status = None
    vote_nullified = False

    created_vote_record = crud.create_vote_record(episode,
                                                    season_castaway,
                                                    castaway_voted_for,
                                                    immunity_status,
                                                    vote_nullified,
                                                    vote_desc,
                                                    final_jury_vote)

    vote_records_in_db.append(created_vote_record)

#print(vote_records_in_db)
model.db.session.add_all(vote_records_in_db)
model.db.session.commit()

#create tribe_mapping table

tribe_mapping_df = pd.read_csv('data/tribe_mapping.csv', usecols=["season",
                                                        "episode",
                                                        "castaway_id",
                                                        "tribe",
                                                        "tribe_status"])
tribe_maps_in_db = []

for index, row in tribe_mapping_df.iterrows():
    season_num = row['season']
    episode_num = row['episode']
    castaway_id = row['castaway_id']
    tribe_name = row['tribe']
    tribe_status = row['tribe_status']

    season_castaway_list = model.Season_Castaway.query.filter(model.Season_Castaway.castaway_id==castaway_id, model.Season_Castaway.season_id==season_num).all()
    season_castaway_id = season_castaway_list[0].season_castaway_id

    episode_list = model.db.session.query(model.Episode).join(model.Season).filter(model.Season.season_num==season_num, model.Episode.episode_num==episode_num).all()
    episode_id = episode_list[0].episode_id
    # print(episode_list)

    created_tribe_map = crud.create_tribe_map(season_castaway_id,
                                                episode_id,
                                                tribe_name,
                                                tribe_status)

    tribe_maps_in_db.append(created_tribe_map)

#model.Vote_Record.query.filter(model.Vote_Record.final_jury_vote==True).all()

# print(tribe_maps_in_db)
model.db.session.add_all(tribe_maps_in_db)
model.db.session.commit()