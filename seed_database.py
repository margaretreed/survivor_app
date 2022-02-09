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

    created_castaway = crud.create_castaway(full_name, short_name, date_of_birth, gender)
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

    created_season = crud.create_season(season_num, season_name, location, country, tribe_setup, filming_started, filming_ended, winner_id)
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

    created_season_castaway = crud.create_season_castaway(season_id, castaway_id, city, state, episode_voted_out, day_voted_out, order_voted_out, outcome_desc, jury_status, finalist_status, img_url)
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

    created_episode = crud.create_episode(season_id, episode_num, title, episode_date, num_viewers)

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
    episode_id = model.db.session.query(model.Episode).join(model.Season).filter(model.Season.season_num==season_num, model.Episode.episode_num==episode).all()
    # print(episode_id[0].episode_num)
    castaway_id = row["castaway_id"]

    #querying for all season_castaway objects with matching castaway_id and season_id
    #getting results with two castaway_season records for castaways that were voted out then came back in a later episode
    season_castaway_list = model.Season_Castaway.query.filter(model.Season_Castaway.castaway_id==castaway_id, model.Season_Castaway.season_id==season_num).all()
    
    # if episode of vote_record <= episode_voted_out of the season_castaway object 
    # then current season_castaway object is the castaway id of that vote_record
    for season_castaway in season_castaway_list:
        if episode_id[0].episode_num <= season_castaway.episode_voted_out:
            season_castaway_id = season_castaway

    castaway_voted_for = row['vote_id']
    #results of this query produce multiple season_castaways if a castaway was voted out then came back at a later episode, 
    #and produces 0 results for various reasons a season_castaway was unable to cast a vote- see vote description for more info
    castaway_voted_for_list = model.Season_Castaway.query.filter(model.Season_Castaway.castaway_id==castaway_voted_for, model.Season_Castaway.season_id==season_num).all()
    for castaway_voted_for_item in castaway_voted_for_list:
        if not castaway_voted_for_item:
            castaway_voted_for_id = None
            print(castaway_voted_for_id)
        if episode_id[0].episode_num <= castaway_voted_for_item.episode_voted_out:
            castaway_voted_for_id = castaway_voted_for_item
    
    # print(castaway_voted_for_id)
    immunity_status = row['immunity']
    vote_nullified = row['nullified']
    vote_desc = row['vote']
    final_jury_vote = ['jury_vote']

    created_vote_record = crud.create_vote_record(episode_id,
                                                    season_castaway_id,
                                                    castaway_voted_for_id,
                                                    immunity_status,
                                                    vote_nullified,
                                                    vote_desc,
                                                    final_jury_vote)

    vote_records_in_db.append(created_vote_record)

# print(vote_records_in_db)
model.db.session.add_all(vote_records_in_db)
model.db.session.commit()

#create tribe_mapping table
