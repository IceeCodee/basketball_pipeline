# Basketball Pipeline
The purpose of this repository is to use the json files provided and load the data into clean, well-organized tables in a postgre database.

# Data Sources
* international_box_player_season.json -> json file with mock data of player stats from one of the four internatinal leagues (EuroLeague, EuroCup, Spain-ACB and Italy-Liga A) <br>
* nba_box_player_season.json -> json file with mock data of player stats from NBA seasons 2010 - 2021 <br>
* player.json -> json file with mock data of basic player info (name, date of birth) <br>

# Methodology
## Tools
__pandas__  -> used for data cleaning <br>  __postgreSQL__ -> used for data storage
## Data Cleaning
* For each file capitalization for player first and last name were standardized
* Duplicate entries were removed
* Missing data were handled accordingly:
  * Team name left blank
  * Internal box plus minue left blank (not able to source formula from internet)
  * Calculated possessions can be filled in with the same number as estimated posessions
  * The reamining missing entries were filled with the following formulas source from various sources on the internet. (It should be noted that some formulas are based on other stats and if the player does not have enough information to compute the formula then it was left as null)
    * True shooting: $2 * (2PTA + 3PTA + 0.44 * FTA)$
    * Three point attempt rate: $3PTA / 2PTA+ 3PTA$
    * Free throw rate: $FTA / 2PTA+ 3PTA$
    * Turnover percentage: $TO / 2PTA + 3PTA + (0.44 * 2PTA+ 3PTA+ TO)$
    * Plays used: $USG\\% / 100 * 2PTA + 3PTA + 0.5 * FTA + TO$ <br>
 Abbreveations can be found here: [https://www.nba.com/stats/help/glossary]

# Queries
.....coming soon........
# Reporting
.....coming soon........
# Conclusion
.....coming soon........
