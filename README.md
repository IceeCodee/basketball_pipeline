# Basketball Pipeline
The purpose of this repository is to use the json files provided and load the data into clean, well-organized tables in a postgre database.

# Data Sources
international_box_player_season.json -> json file with mock data of player stats from one of the four internatinal leagues (EuroLeague, EuroCup, Spain-ACB and Itali- Liga A)
nba_box_player_season.json -> json file with mock data of player stats from NBA seasons 2010 - 2021
player.json -> json file with mock data of basic player info (name, date of birth)

# Methodology
## Tools
pandas used for data cleaning <br>  postgreSQL used for data storage
## Data Cleaning
* For each file capitalization for player first and last name were standardized
* Duplicate entries were removed
* Missing data were handled accordingly:
  * Team name left blank
  * Internal box plus minue left blank due to
  * True shooting filled in with formula
      * $ 2 * (2PTA + 3PTA + 0.44 * FTA) $


# Queries
.....coming soon........
# Reporting
.....coming soon........
# Conclusion
.....coming soon........
