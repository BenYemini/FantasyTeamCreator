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
        self.second_captain = Player
        self.first_squad_candidates = []
        self.first_squad = {
            "GKP": [],
            "DEF": [],
            "MID": [],
            "FWD": []
        }
        self.num_of_players_in_first_squad = 0
        self.sub_players = []

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

    def set_captains(self, player):
        self.set_first_captain(player)
        if self.first_captain != player:
            self.set_second_captain(player)

    # Returns the team's captain.
    def get_first_captain(self):
        return self.first_captain

    # If the given player's points per game average is greater than the current first captain,
    # it sets him to be the first captain If not, it checks with the second captain.
    def set_first_captain(self, player):
        if self.num_of_players_in_first_squad == 0:
            self.first_captain = player
        else:
            if self.first_captain.get_points_per_game() < player.get_points_per_game():
                self.second_captain = self.first_captain
                self.first_captain = player
            else:
                self.set_second_captain(player)

    # Returns the team's second captain.
    def get_second_captain(self):
        return self.second_captain

    # If the given player's points per game average is greater than the current second captain,
    # it sets him to be the second captain.
    def set_second_captain(self, player):
        if self.num_of_players_in_first_squad == 1:
            self.second_captain = player
        else:
            if self.second_captain.get_points_per_game() < player.get_points_per_game():
                self.second_captain = player

    # This method appends the given player to the relevant list, according to his position.
    def append(self, player, winners_position):
        if winners_position == "GKP":
            self.goalkeepers.append(player)
            self.num_of_players += 1
        elif winners_position == "DEF":
            self.defenders.append(player)
            self.num_of_players += 1
        elif winners_position == "MID":
            self.midfielders.append(player)
            self.num_of_players += 1
        else:
            self.forwards.append(player)
            self.num_of_players += 1

    # Returns a List[Player] containing 11 first squad players.
    def get_first_squad(self):
        return self.first_squad

    # Sets the team's first squad, according to total grades, and FPL limitations.
    # Notice that the limitations refers only to goalkeepers, defenders and forwards but simple math will tell us that
    # the number of midfielders in the first squad is also a limitation (2 midfielders).
    def set_first_squad(self):
        self.set_player_to_squad(self.goalkeepers[FIRST_KEEPER], "GKP")  # Picking the goalkeeper.
        for d in range(NUMBER_OF_DEFENDERS):  # Picking the 3 defensive players that were added first.
            if d < MIN_DEFENDERS_IN_SQUAD:
                self.set_player_to_squad(self.defenders[d], "DEF")
            else:
                self.first_squad_candidates.append(self.defenders[d])
        for m in range(NUMBER_OF_MIDFIELDERS):  # Picking the 2 midfield players that were added first.
            if m < MIN_MIDFIELDERS_IN_SQUAD:
                self.set_player_to_squad(self.midfielders[m], "MID")
            else:
                self.first_squad_candidates.append(self.midfielders[m])
        for f in range(NUMBER_OF_FORWARDS):
            if f < MIN_FORWARDS_IN_SQUAD:  # Picking the forward that was added first.
                self.set_player_to_squad(self.forwards[f], "FWD")
            else:
                self.first_squad_candidates.append(self.forwards[f])
        self.first_squad_candidates.sort(key=total_grade_key_func,
                                         reverse=True)  # Sort the list in order to extract the TOP
        # 4 to be in the first squad. The others will be set as sub.
        for p in range(PLAYERS_LEFT_TO_FILL_SQUAD):  # Select the 4 top graded player from the first squad candidates
            # list, and set them to be in the first squad.
            position = self.first_squad_candidates[p].get_position()
            self.set_player_to_squad(self.first_squad_candidates[p], position)

    # Returns a List[Player] containing 4 sub players
    def get_sub_players(self):
        return self.sub_players

    # Sets the left players from the first_squad_candidates to be in subs, according to their place in the list.
    # Sets the second goalkeeper to be the last sub - fantasy logic.
    def set_sub_players(self):
        for s in range(PLAYERS_LEFT_TO_FILL_SQUAD, len(self.first_squad_candidates)):  # Set the others to be subs.
            self.set_player_to_subs(self.first_squad_candidates[s])
        self.set_player_to_subs(self.goalkeepers[SECOND_KEEPER])  # Set the second goalkeeper to be last sub.

    # Sets the given player to be in first squad, according to his position.
    def set_player_to_squad(self, player, position):
        self.set_captains(player)
        self.first_squad[position].append(player)
        self.num_of_players_in_first_squad += 1

    # Sets the given player to be in sub players list.
    def set_player_to_subs(self, player):
        self.sub_players.append(player)


# Key function for the first_squad_candidates sort at the set_first_squad method. Sort by total grade.
def total_grade_key_func(element):
    return element.get_total_grade()
