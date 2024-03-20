import psycopg2
import pandas as pd
from sqlalchemy import create_engine

conn_string = 'postgresql://postgres:postgres@127.0.0.1:5432/Pro_Basketball'
db = create_engine(conn_string)
connection = db.connect()

conn = psycopg2.connect(
    dbname='Pro_Basketball',
    user='postgres',
    password='',
    host='127.0.0.1',
    port='5432'
)

conn.autocommit = True
cursor = conn.cursor()

# import json files into pandas dataframe
player_data = pd.read_json('player.json')
international_data = pd.read_json('international_box_player_season.json')
nba_data = pd.read_json('nba_box_player_season.json')

# data cleaning

# standardizing capitalization of player names
player_data['first_name'] = player_data['first_name'].str.capitalize()
player_data['last_name'] = player_data['last_name'].str.capitalize()
# removing any duplicated inside of the dataframe
player_data.drop_duplicates()

# clean data from international player boxscore table
international_data['first_name'] = international_data['first_name'].str.capitalize()
international_data['last_name'] = international_data['last_name'].str.capitalize()
international_data.drop_duplicates()
# all null values for team name and internal box plus minus have been left alone
international_data['true_shooting_percentage'] = international_data['true_shooting_percentage'].fillna(
    international_data['points'] / (2 * (
            (international_data['two_points_attempted'] + international_data['three_points_attempted']) + 0.44 *
            international_data['free_throws_attempted'])))
international_data['three_point_attempt_rate'] = international_data['three_point_attempt_rate'].fillna(
    international_data['three_points_attempted'] / (
            international_data['two_points_attempted'] + international_data['three_points_attempted']))
international_data['free_throw_rate'] = international_data['free_throw_rate'].fillna(
    international_data['free_throws_attempted'] / (
            international_data['two_points_attempted'] + international_data['three_points_attempted']))
international_data['turnover_percentage'] = international_data['turnover_percentage'].fillna(
    international_data['turnovers'] / (
            international_data['two_points_attempted'] + international_data['three_points_attempted'] + (
            0.44 * international_data['two_points_attempted'] + international_data['three_points_attempted'])) +
    international_data['turnovers'])
international_data = international_data.round(2)

# cleaning data from nba table
nba_data['first_name'] = nba_data['first_name'].str.capitalize()
nba_data['last_name'] = nba_data['last_name'].str.capitalize()
nba_data.drop_duplicates()
nba_data['calculated_possessions'] = nba_data['calculated_possessions'].fillna(nba_data['estimated_possessions'])
nba_data['true_shooting_percentage'] = nba_data['true_shooting_percentage'].fillna(nba_data['points'] / (2 * ((nba_data['two_points_attempted'] + nba_data['three_points_attempted']) + 0.44 * nba_data['free_throws_attempted'])))
nba_data['three_point_attempt_rate'] = nba_data['three_point_attempt_rate'].fillna(nba_data['three_points_attempted'] / (nba_data['two_points_attempted'] + nba_data['three_points_attempted']))
nba_data['free_throw_rate'] = nba_data['free_throw_rate'].fillna(nba_data['free_throws_attempted'] / (nba_data['two_points_attempted'] + nba_data['three_points_attempted']))
nba_data['turnover_percentage'] = nba_data['turnover_percentage'].fillna(nba_data['turnovers'] / (nba_data['two_points_attempted'] + nba_data['three_points_attempted'] + (0.44 * nba_data['two_points_attempted'] + nba_data['three_points_attempted'])) + nba_data['turnovers'])
nba_data['plays_used'] = (nba_data['usage_percentage'] / 100) * (nba_data['two_points_attempted'] + nba_data['three_points_attempted'] + 0.5 * nba_data['free_throws_attempted'] + nba_data['turnovers'])
nba_data = nba_data.round(2)

# create three tables: (1)player, (2)international, (3)nba
create_player_table = '''
CREATE TABLE player(
first_name CHAR(20), 
last_name CHAR(20), 
birthdate DATE);
'''
cursor.execute('DROP TABLE IF EXISTS player')
cursor.execute(create_player_table)
player_data.to_sql(name='player', con=connection, if_exists='replace', index=False)
print('done with player table')

create_nba_table = '''
CREATE TABLE nba(
first_name VARCHAR(20),
last_name VARCHAR(20),
season VARCHAR(20),
season_type VARCHAR(20),
league VARCHAR(20),
team VARCHAR(20),
games INT,
starts INT,
minutes DECIMAL,
points INT,
plus_minus INT,
two_points_made INT,
two_points_attempted INT,
three_points_made INT,
three_points_attempted INT,
free_throws_made INT,
free_throws_attempted INT,
blocked_shot_attempts INT,
offensive_rebounds INT,
defensive_rebounds INT,
assists INT,
screen_assists INT,
turnovers INT,
steals INT,
deflections INT,
loose_balls_recovered INT,
blocked_shots INT,
personal_fouls INT,
personal_fouls_drawn INT,
offensive_fouls INT,
charges_drawn INT,
technical_fouls INT,
flagrant_fouls INT,
ejections INT,
points_off_turnovers INT,
points_in_paint INT,
second_chance_points INT,
fast_break_points INT,
possessions INT,
estimated_possessions DECIMAL,
calculated_possessions INT,
plays_used INT,
team_possessions DECIMAL,
usage_percentage DECIMAL,
true_shooting_percentage DECIMAL,
three_point_attempt_rate DECIMAL,
free_throw_rate DECIMAL,
offensive_rebounding_percentage DECIMAL,
defensive_rebounding_percentage DECIMAL,
total_rebounding_percentage DECIMAL,
assist_percentage DECIMAL,
steal_percentage DECIMAL,
block_percentage DECIMAL,
turnover_percentage DECIMAL,
internal_box_plus_minus DECIMAL
);
'''
cursor.execute('DROP TABLE IF EXISTS nba')
cursor.execute(create_nba_table)
nba_data.to_sql(name='nba', con=connection, if_exists='replace', index=False)
print('done with nba table')

create_international_table = '''
CREATE TABLE international(
first_name VARCHAR(20),
last_name VARCHAR(20),
season VARCHAR(20),
season_type VARCHAR(20),
league VARCHAR(20),
team VARCHAR(20),
games INT,
starts INT,
minutes DECIMAL,
points INT,
two_points_made INT,
two_points_attempted INT,
three_points_made INT,
three_points_attempted INT,
free_throws_made INT,
free_throws_attempted INT,
blocked_shot_attempts INT,
offensive_rebounds INT,
defensive_rebounds INT,
assists INT,
screen_assists INT,
turnovers INT,
steals INT,
deflections INT,
loose_balls_recovered INT,
blocked_shots INT,
personal_fouls INT,
personal_fouls_drawn INT,
offensive_fouls INT,
charges_drawn INT,
technical_fouls INT,
flagrant_fouls INT,
ejections INT,
points_off_turnovers INT,
points_in_paint INT,
second_chance_points INT,
fast_break_points INT,
possessions DECIMAL,
estimated_possessions DECIMAL,
team_possessions DECIMAL,
usage_percentage DECIMAL,
true_shooting_percentage DECIMAL,
three_point_attempt_rate DECIMAL,
free_throw_rate DECIMAL,
offensive_rebounding_percentage DECIMAL,
defensive_rebounding_percentage DECIMAL,
total_rebounding_percentage DECIMAL,
assist_percentage DECIMAL,
steal_percentage DECIMAL,
block_percentage DECIMAL,
turnover_percentage DECIMAL,
internal_box_plus_minus DECIMAL
);
'''
cursor.execute('DROP TABLE IF EXISTS international')
cursor.execute(create_international_table)
player_data.to_sql(name='international', con=connection, if_exists='replace', index=False)
print('done with international table')

conn.close()
