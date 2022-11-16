from matplotlib import pyplot as plt
import random
from Player import *
from constants import *
from UserFantasyTeam import *


class FantasyTeamRenderer(object):
    def __init__(self, user_team):
        self.first_squad = user_team.get_first_squad()
        self.sub_players = user_team.get_sub_players()
        self.team_captain = user_team.get_first_captain()
        self.second_team_captain = user_team.get_second_captain()
        self.remaining_budget = user_team.get_budget()

    def render_first_squad(self):
        print("\n" + "First squad:" + "\n")
        print("GKP:")
        self.first_squad['GKP'][FIRST_KEEPER].print()
        print("\n" + "DEF:")
        for defender in self.first_squad['DEF']:
            defender.print()
        print("\n" + "MID:")
        for midfielder in self.first_squad['MID']:
            midfielder.print()
        print("\n" + "FWD:")
        for forward in self.first_squad['FWD']:
            forward.print()

    def render_subs(self):
        print("\n" + "Sub players:" + "\n")
        sub_counter = 1
        for sub_player in self.sub_players:
            print(str(sub_counter))
            sub_player.print()
            sub_counter += 1

    def render_captains(self):
        print()
        print("Team Captain:")
        self.team_captain.print()
        print()
        print("Second Team Captain:")
        self.second_team_captain.print()

    def render_remaining_budget(self):
        print("\n" + "The remaining budget is: " + "{:.1f}".format(self.remaining_budget))

    def render_graph_representation_first_squad(self):
        total_grade_side = []
        position_side = []

        for player in self.first_squad['GKP']:
            total_grade_side.append(player.get_total_grade())
            position_side.append(random.random() + 1)
        for player in self.first_squad['DEF']:
            total_grade_side.append(player.get_total_grade())
            position_side.append(random.random() + 2)
        for player in self.first_squad['MID']:
            total_grade_side.append(player.get_total_grade())
            position_side.append(random.random() + 3)
        for player in self.first_squad['FWD']:
            total_grade_side.append(player.get_total_grade())
            position_side.append(random.random() + 4)

        plt.scatter(position_side, total_grade_side, label="total_grades", color="green",
                    marker=".", s=40)

        plt.xlabel('Total Grade side')
        # frequency label
        plt.ylabel('Position Side')
        # plot title
        plt.title('User Team - Total Grades divided to positions ')

        # showing legend
        plt.legend()
        # function to show the plot
        plt.show()



