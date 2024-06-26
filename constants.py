FIRST_KEEPER = 0  # First keeper index in the 'GKP' key list.
SECOND_KEEPER = 1  # Second keeper index in the 'GKP' key list.
NUMBER_OF_DEFENDERS = 5  # The amount of defenders in the team.
NUMBER_OF_MIDFIELDERS = 5  # The amount of midfielders in the team.
NUMBER_OF_FORWARDS = 3  # The amount of forwards in the team.
MIN_DEFENDERS_IN_SQUAD = 3  # Min number of defenders in team squad.
MIN_MIDFIELDERS_IN_SQUAD = 2  # Min number of midfielders in team squad.
MIN_FORWARDS_IN_SQUAD = 1  # Min number of forwards in team squad.
NUM_OF_SUB_PLAYERS = 4  # Number of sub players in the team.
MAX_NUM_OF_PLAYERS_FROM_TEAM = 3  # The maximum number of players which can ben selected from each team.
TOTAL_NUM_OF_PLAYERS_IN_FINAL_TEAM = 15  # The final amount of players in the team.
NUM_OF_FIRST_SQUAD_PLAYERS = 11  # Number of first-squad players in soccer team.
MIN_AMOUNT_OF_BUDGET_FOR_EACH_FIRST_SQUAD_PLAYER = 4  # Guarantees each first-squad player price will be above 4.5.
MIN_AMOUNT_OF_BUDGET_FOR_EACH_SUB_PLAYER = 3  # Guarantees each sub player's price will be above 3.5.
MIN_BUDGET_FOR_SUB_PLAYERS_SELECTION = 12  # Min amount of budget needed to buy 4 sub players.
HOME_GAME_BONUS = 0.2  # If the team plays at home the probability to win is bigger.
AWAY_GAME_DEDUCTION = -0.2  # If the team plays at away field the probability to win is smaller.
TOP_STRENGTH_TEAM_BONUS = 2  # Top strength team are the best teams in the premier league (rating - 5).
GOOD_STRENGTH_TEAM_BONUS = 1  # Good strength teams are teams that has a rating of 4 (in 1-5 scale).
AVERAGE_STRENGTH_TEAM_BONUS = 0.5  # Average strength teams are teams that has a rating of 3 (in 1-5 scale).
BAD_STRENGTH_TEAM_DEDUCTION = -2  # Bad strength teams are teams that has a rating of 1-2 (in 1-5 scale).
MIN_TOTAL_GRADE_NEEDED_TO_PASS = 7  # Min grade for activity and next fixture check.
MIN_TOTAL_GRADE_NEEDED_TO_PASS_FOR_FWD = 6  # Min grade for activity and next fixture check for forwards only.
MIN_NUM_OF_GAMES_ACTIVE = 2  # Min num of games played by player this season in order to be considered as active.
ONE_HALF_TIME = 45  # The length of one half in football.
DEF_PENALTIES_BONUS = 2.5  # If a defender is the penalty taker in his team then he receives this bonus.
MID_PENALTIES_BONUS = 2  # If a midfielder is the penalty taker in his team then he receives this bonus.
FWD_PENALTIES_BONUS = 2  # If a forward is the penalty taker in his team then he receives this bonus.
CORNERS_OR_FREEKICK_BONUS = 0.75  # If a player is the set piece taker he receives this bonus.
SELECTED_BY_MAJORITY_BONUS = 2  # If the majority of fantasy players selected this player, he receives a bonus.
MAX_NUM_OF_GOALKEEPERS_IN_TEAM = 2  # The maximum number of goalkeepers in the UserTeam.
MAX_NUM_OF_DEFENDERS_IN_TEAM = 5  # The maximum number of defenders in the UserTeam.
MAX_NUM_OF_MIDFIELDERS_IN_TEAM = 5  # The maximum number of midfielders in the UserTeam.
MAX_NUM_OF_FORWARDS_IN_TEAM = 3  # The maximum number of forwards in the UserTeam.
TOP_5_TEAMS_ID = [1, 13, 18, 15, 14]  # Premier league TOP 5 teams (id number in API)
TOP_5_TEAMS_NAMES = ["Arsenal", "Man City", "Spurs", "Newcastle", "Man Utd"]  # Top 5 premier league teams.
MAX_NUM_OF_SUPERSTARS_IN_USER_TEAM = 2  # Number of superstar players, most points per game in premier league players.
MIN_MINUTES_NEEDED_TO_PASS = 40  # Min amount of minutes needed to pass the activity check.
