from Player import *
from constants import *


class UserFantasyTeam:

    def __init__(self):
        self.goalkeepers = []
        self.defenders = []
        self.midfielders = []
        self.forwards = []
        self.num_of_players = 0
        self.first_captain = Player
        self.first_captain_position = ""
        self.second_captain = Player
        self.second_captain_position = ""
        self.first_squad_candidates = []
        self.first_squad = {
            "GKP": [],
            "DEF": [],
            "MID": [],
            "FWD": []
        }
        self.num_of_players_in_first_squad = 0
        self.sub_players = []
        self.budget = float

    # Set the team's budget to the primary budget given by the user.
    def set_budget(self, budget):
        self.budget = budget

    # Returns the current budget.
    def get_budget(self):
        return self.budget

    # Sets the budget after purchasing a player to the team.
    def set_budget_after_player_purchase(self, player_price):
        self.budget -= player_price

    # Returns the current number of players in the team.
    def get_num_of_players(self):
        return self.num_of_players

    # Returns the current number of goalkeepers in the team.
    def get_num_of_goalkeepers(self):
        return len(self.goalkeepers)

    # Returns the current number of defenders in the team.
    def get_num_of_defenders(self):
        return len(self.defenders)

    # Returns the current number of midfielders in the team.
    def get_num_of_midfielders(self):
        return len(self.midfielders)

    # Returns the current number of forwards in the team.
    def get_num_of_forwards(self):
        return len(self.forwards)

    # If the player is the first or second player chosen to the team, then he is the team's first or second captain.
    def set_captains(self, player):
        if self.num_of_players == 1:    # First player picked, therefore the team's first captain.
            self.set_first_captain(player)
        elif self.num_of_players == 2:  # Second player picked, therefore the team's second captain.
            self.set_second_captain(player)

    # Sets the given player to be the team's first captain.
    def set_first_captain(self, player):
        self.first_captain = player
        self.first_captain_position = player.get_position()

    # Returns the team's first captain.
    def get_first_captain(self):
        return self.first_captain

    # Sets the given player to be the team's second captain.
    def set_second_captain(self, player):
        self.second_captain = player
        self.second_captain_position = player.get_position()

    # Returns the team's second captain.
    def get_second_captain(self):
        return self.second_captain

    # This method appends the given player to the relevant list, according to his position.
    def append(self, player, winners_position):
        if winners_position == "GKP":
            self.goalkeepers.append(player)
        elif winners_position == "DEF":
            self.defenders.append(player)
        elif winners_position == "MID":
            self.midfielders.append(player)
        else:
            self.forwards.append(player)
        self.num_of_players += 1
        self.set_captains(player)

    # Returns a List[Player] containing 11 first squad players.
    def get_first_squad(self):
        return self.first_squad

    # Sets the team's first squad according to total grades and FPL limitations.
    # Notice that the limitations refers only to goalkeepers, defenders and forwards but simple math will tell us that
    # the number of midfielders in the first squad is also a limitation.
    def set_first_squad(self):
        self.set_goalkeepers_to_first_squad()
        self.set_defenders_to_first_squad()
        self.set_midfielders_to_first_squad()
        self.set_forwards_to_first_squad()
        self.validate_first_captain_in_first_squad()  # Making sure that the first captain is in the first squad.
        self.validate_second_captain_in_first_squad()  # Making sure that the second captain is in the first squad.
        self.first_squad_candidates.sort(key=total_grade_key_func)  # Sort the list in order to extract
        # the TOP players left to fill the squad. The others will be set as sub.
        self.set_first_squad_candidates_to_first_squad()

    # Sets the goalkeepers to be either in the first squad or either in the subs list.
    # according to FPL Limitations (for minimum number of goalkeepers in the team).
    def set_goalkeepers_to_first_squad(self):
        self.set_player_to_squad(self.goalkeepers[FIRST_KEEPER], "GKP")  # Picking the goalkeeper.
        self.set_player_to_subs(self.goalkeepers[SECOND_KEEPER])  # Set the second goalkeeper to be in subs.

    # Sets the forwards to be either in the first squad or either in the subs list.
    # according to FPL Limitations (for minimum number of defenders in the team).
    def set_defenders_to_first_squad(self):
        for counter in range(NUMBER_OF_DEFENDERS):  # Picking the 3 defensive players that were added first.
            if counter < MIN_DEFENDERS_IN_SQUAD:
                self.set_player_to_squad(self.defenders[counter], "DEF")
            else:
                self.first_squad_candidates.append(self.defenders[counter])

    # Sets the midfielders to be either in the first squad or either in the subs list.
    # according to FPL Limitations (for minimum number of midfielders in the team).
    def set_midfielders_to_first_squad(self):
        for counter in range(NUMBER_OF_MIDFIELDERS):  # Picking the 2 midfield players that were added first.
            if counter < MIN_MIDFIELDERS_IN_SQUAD:
                self.set_player_to_squad(self.midfielders[counter], "MID")
            else:
                self.first_squad_candidates.append(self.midfielders[counter])

    # Sets the forwards to be either in the first squad or either in the subs list.
    # according to FPL Limitations (for minimum number of forwards in the team).
    def set_forwards_to_first_squad(self):
        for counter in range(NUMBER_OF_FORWARDS):
            if counter < MIN_FORWARDS_IN_SQUAD:  # Picking the forward that was added first.
                self.set_player_to_squad(self.forwards[counter], "FWD")
            else:
                self.first_squad_candidates.append(self.forwards[counter])

    # Sets the left players to be either in the first squad or either in the subs list.
    def set_first_squad_candidates_to_first_squad(self):
        while self.num_of_players_in_first_squad != NUM_OF_FIRST_SQUAD_PLAYERS:
            first_squad_player = self.first_squad_candidates.pop()
            first_squad_player_position = first_squad_player.get_position()
            self.set_player_to_squad(first_squad_player, first_squad_player_position)

    # Ensurers that the team's first captain will be in the first squad.
    # Checks if his in the first squad, and if not - appends him to the first squad and removes from candidates.
    def validate_first_captain_in_first_squad(self):
        if self.first_captain in self.first_squad_candidates:  # First captain isn't in the first squad.
            self.set_player_to_squad(self.first_captain, self.first_captain_position)  # Add captain to squad.
            self.first_squad_candidates.remove(self.first_captain)  # Delete the captain from candidates list.

    # Ensurers that the team's second captain will be in the first squad.
    # Checks if his in the first squad, and if not - appends him to the first squad and removes from candidates.
    def validate_second_captain_in_first_squad(self):
        if self.second_captain in self.first_squad_candidates:  # Second captain isn't in the first squad.
            self.set_player_to_squad(self.second_captain, self.second_captain_position)  # Add captain to squad.
            self.first_squad_candidates.remove(self.second_captain)  # Delete the captain from candidates list.

    # Sets the left players to be in the subs list.
    # Notice that each sub player will be added to a place in the sub list according to his total grade.
    def set_sub_players(self):
        while len(self.first_squad_candidates) != 0:
            self.set_player_to_subs(self.first_squad_candidates.pop())

    # Returns a List[Player] containing 4 sub players.
    def get_sub_players(self):
        return self.sub_players

    # Sets the given player to be in first squad, according to his position.
    def set_player_to_squad(self, player, position):
        self.first_squad[position].append(player)
        self.num_of_players_in_first_squad += 1

    # Sets the given player to be in sub players list.
    def set_player_to_subs(self, player):
        self.sub_players.append(player)


# Key function for the first_squad_candidates sort at the set_first_squad method. Sort by total grade.
def total_grade_key_func(element):
    return element.get_total_grade()
