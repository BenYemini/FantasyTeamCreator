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
            if current_num_of_players_in_user_team == 0:
                self.players_pool.sort(key=points_per_game_key_func)
            winner = self.players_pool.pop()
            self.players[winner.get_position()].delete_player(winner)
            if not winner.is_active():
                self.pick_players_for_user_team()
        else:
            winner = compare_players(self.players, self.user_team)
        if legal_move(winner, self.user_team, self.teams):  # According to FPL limitations.
            winners_position = winner.get_position()
            winners_team = winner.get_team()
            self.user_team.append(winner, winners_position)  # Add the player to the team.
            self.teams[winners_team].set_picked_player()  # Set the winner's team counter, notice the indexes.
            self.user_team.set_budget_after_player_purchase(winner.get_price())
            self.pick_players_for_user_team()
        else:  # The move is illegal... the player will not be considered in the comparison anymore.
            self.pick_players_for_user_team()


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
    goalkeepers_candidate = players['GKP'].peek()  # The goalkeeper with the highest grade.
    defense_candidate = players['DEF'].peek()  # the defender with the highest grade.
    midfield_candidate = players['MID'].peek()  # the midfielder with the highest grade.
    forwards_candidate = players['FWD'].peek()  # the forward with the highest grade.
    candidates = [goalkeepers_candidate, defense_candidate, midfield_candidate, forwards_candidate]
    candidates.sort(key=total_grade_key_func, reverse=True)  # Sorts the list (top grade first).
    winners_position = candidates[FIRST_PLACE].get_position()  # Gets top graded player's position on the field.
    # If the goalkeeper wins.
    if winners_position == "GKP":
        if user_team.get_num_of_players() < NUM_OF_FIRST_SQUAD_PLAYERS and user_team.get_num_of_goalkeepers() != 0:
            # If we still pick the first squad players,and there's already a goalkeeper - no reason to have another one.
            winners_position = candidates[SECOND_PLACE].get_position()  # Changing the winner to be the second place
        else:
            players['GKP'].delete_max()
            return goalkeepers_candidate

    # If the defender wins.
    if winners_position == "DEF":
        players['DEF'].delete_max()
        return defense_candidate
    # if the midfielder wins.
    elif winners_position == "MID":
        players['MID'].delete_max()
        return midfield_candidate
    # If the forward wins.
    else:
        players['FWD'].delete_max()
        return forwards_candidate


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


# This function check's if the budget will be enough for future players.
# This function is a bit tricky and requires time to understand the logic and the numbers behind it.
# In my opinion, we need to save 15.0 from budget to 4 sub players, that means - 3.75 M at least for each player.
# The rest will be for first-squad players, 6.5 M at least for each player.
# The calculation for first squad players is: 2 * 12.0 + 1 * 10.0 + 3 * 8.0 + 2 * 7.0 + 3 * 5.6  = 100.0 - 15.0 = 85.0 =
# 2 SuperStars, 1 Star, 3 Top players, 2 Above average, 3 Jokers.
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


def push_to_heap(self, player):
    if player.get_position() == "GKP":
        self.players['GKP'].push(player)

    elif player.get_position() == "DEF":
        self.players['DEF'].push(player)

    elif player.get_position() == "MID":
        self.players['MID'].push(player)

    else:
        self.players['FWD'].push(player)


def points_per_game_key_func(element):
    return element.get_points_per_game()


# Key function for the compare_players function. Sort by total grade.
def total_grade_key_func(element):
    return element.get_total_grade()
