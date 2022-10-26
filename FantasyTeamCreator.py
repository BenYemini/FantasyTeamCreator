from UserFantasyTeam import *
from Player import *
from MaxHeap import *
from constants import *
from Team import *


class FantasyTeamCreator:

    def __init__(self, json_teams, json_players, budget):
        self.teams = create_teams_obj(json_teams)
        self.players_pool = create_players_obj(json_players)
        self.players = {
            "GKP": MaxHeap(),
            "DEF": MaxHeap(),
            "MID": MaxHeap(),
            "FWD": MaxHeap()
        }
        self.user_team = UserFantasyTeam()
        self.user_team.set_budget(budget)

    # explanation in ReadMe!
    def create_team(self):
        self.grade_giver()
        self.pick_players_for_user_team()
        return self.user_team

    # This method takes each player from the players_pool and sets his total grade, using methods from Player class.
    # After setting his grade, the player is appended to a heap according to his position.
    def grade_giver(self):
        for player in self.players_pool:
            player_team = self.teams[player.get_team()]
            player_grade = player.get_player_grade(player_team)
            player.set_total_grade(player_grade)
            push_to_heap(self, player)

    # Recursive function, pick's the top graded player every time until the UserTeam is full.
    # This method considers a lot of FPL limitations, I highly recommend reading about those limitations in the ReadMe.
    def pick_players_for_user_team(self):
        current_num_of_players_in_user_team = self.user_team.get_num_of_players()
        if current_num_of_players_in_user_team == TOTAL_NUM_OF_PLAYERS_IN_FINAL_TEAM:  # Recursion Stopping condition.
            return
        elif current_num_of_players_in_user_team < 2:  # Picking superstars - most Points Per Game players.
            winner = select_superstars(self.players_pool, self.players, self.user_team)
        else:
            winner = compare_players(self.players, self.user_team)
        if legal_move(winner, self.user_team, self.teams) and winner.is_active():  # According to FPL limitations.
            self.purchase_player_to_team(winner)
            self.pick_players_for_user_team()
        else:  # The move is illegal... the player will not be considered in the comparison anymore.
            self.pick_players_for_user_team()

    # Purchase the given player to the UserFantasyTeam including updating
    # important fields: positions, picked teams, budget.
    def purchase_player_to_team(self, winner):
        winners_position = winner.get_position()
        winners_team = winner.get_team()
        self.user_team.append(winner, winners_position)  # Add the player to the team.
        self.teams[winners_team].set_picked_player()  # Set the winner's team counter, notice the indexes.
        self.user_team.set_budget_after_player_purchase(winner.get_price())


# Returns a "superstar player".
# "Superstar player" - first or second player picked to the team.
# This sort of pick is made according to the points_per_game field.
def select_superstars(players_pool, players, user_team):
    if user_team.get_num_of_players() == 0:
        players_pool.sort(key=points_per_game_key_func)  # Top points_per_game player is last.
    winner = players_pool.pop()  # The player with the best points_per_game average.
    players[winner.get_position()].delete_player(winner)
    return winner


# This function creates Player object for each player in the json file and adds him to the players field.
def create_players_obj(json_players):
    players = []
    for player in json_players:
        player_obj = Player(player)
        players.append(player_obj)
    return players


# This function creates Team object for each team in the json file and adds him to the Teams field.
# It sets the first element to 0, in order to avoid indexes issues later (teams id starts
# from 1).
def create_teams_obj(json_teams):
    teams = [0]
    for team in json_teams:
        team_obj = Team(team)
        teams.append(team_obj)
    return teams


# This function find and returns the top graded player.
# The root holds a Player object that has the highest total grade among all players in his position.
# We will compare all 4 top graded players in their position, and return the top graded of them.
def compare_players(players, user_team):
    candidates = get_candidates_for_squad(players)  # List[Player], with top graded players from each position.
    candidates.sort(key=total_grade_key_func)  # Sorts the list.
    winner = candidates.pop()  # Gets top graded player's position on the field.
    if winner.get_position() == "GKP":
        if user_team.get_num_of_players() < NUM_OF_FIRST_SQUAD_PLAYERS and user_team.get_num_of_goalkeepers() != 0:
            # If we still pick the first squad players,and there's already a goalkeeper - no reason to have another one.
            winner = candidates.pop()  # Changing the winner to be the second place
    players[winner.get_position()].delete_max()
    return winner


# This function check's if adding the player to the UserTeam is a legal move - according to FPL limitations.
def legal_move(winner, user_team, teams):
    return (budget_ratio_approval(winner, user_team) and
            positions_approval(winner, user_team) and picked_from_teams_approval(winner, teams))


# This function check's if the player's position in the squad is available.
def positions_approval(winner, user_team):
    winners_position = winner.get_position()  # Gets player's position on the field.
    if winners_position == "GKP":
        if user_team.get_num_of_goalkeepers() == MAX_NUM_OF_GOALKEEPERS_IN_TEAM:
            return False
    elif winners_position == "DEF":
        if user_team.get_num_of_defenders() == MAX_NUM_OF_DEFENDERS_IN_TEAM:
            return False
    elif winners_position == "MID":
        if user_team.get_num_of_midfielders() == MAX_NUM_OF_MIDFIELDERS_IN_TEAM:
            return False
    else:
        if user_team.get_num_of_forwards() == MAX_NUM_OF_FORWARDS_IN_TEAM:
            return False

    return True


# This function check's if the number of players picked from the player's team is legal.
def picked_from_teams_approval(winner, teams):
    if teams[winner.get_team()].get_picked_players() == MAX_NUM_OF_PLAYERS_FROM_TEAM:
        return False
    return True


# This function check's if the budget will be enough for future players, Returns True if so, and False otherwise.
# This function is a bit tricky and requires time to understand the logic and the numbers behind it.
# In my opinion, we need to save 18.0 from budget to 4 sub players.
# The rest will be for first-squad players.

def budget_ratio_approval(winner, user_team):
    after_purchase_budget = user_team.get_budget() - winner.get_price()  # The predicted budget.
    current_players_count = user_team.get_num_of_players()
    if current_players_count == TOTAL_NUM_OF_PLAYERS_IN_FINAL_TEAM - 1:  # Picking the last player to the UserTeam.
        return after_purchase_budget >= 0
    else:
        after_purchase_players_to_go = TOTAL_NUM_OF_PLAYERS_IN_FINAL_TEAM - (current_players_count + 1)
        if current_players_count >= NUM_OF_FIRST_SQUAD_PLAYERS:  # Choosing sub player.
            ratio = after_purchase_budget / after_purchase_players_to_go  # Budget for each future sub player.
            return ratio > MIN_AMOUNT_OF_BUDGET_FOR_EACH_SUB_PLAYER
        elif current_players_count == NUM_OF_FIRST_SQUAD_PLAYERS - 1:  # Choosing the last first-squad player.
            return user_team.get_budget() >= MIN_BUDGET_FOR_SUB_PLAYERS_SELECTION
        else:  # Choosing first-squad player.
            ratio = (after_purchase_budget - MIN_BUDGET_FOR_SUB_PLAYERS_SELECTION) / \
                    (after_purchase_players_to_go - NUM_OF_SUB_PLAYERS)
            return ratio > MIN_AMOUNT_OF_BUDGET_FOR_EACH_FIRST_SQUAD_PLAYER


# Returns a List[Player] containing the top graded players from each heap (position on the field).
def get_candidates_for_squad(players):
    goalkeepers_candidate = players['GKP'].peek()  # The goalkeeper with the highest grade.
    defense_candidate = players['DEF'].peek()  # the defender with the highest grade.
    midfield_candidate = players['MID'].peek()  # the midfielder with the highest grade.
    forwards_candidate = players['FWD'].peek()  # the forward with the highest grade.
    return [goalkeepers_candidate, defense_candidate, midfield_candidate, forwards_candidate]


# Adds the given player to the relevant heap according to his position.
def push_to_heap(self, player):
    if player.get_position() == "GKP":
        self.players['GKP'].push(player)

    elif player.get_position() == "DEF":
        self.players['DEF'].push(player)

    elif player.get_position() == "MID":
        self.players['MID'].push(player)

    else:
        self.players['FWD'].push(player)


# Key function for sorting Player objects according to points_per_game field.
def points_per_game_key_func(element):
    return element.get_points_per_game()


# Key function for the compare_players function. Sort by total grade.
def total_grade_key_func(element):
    return element.get_total_grade()
