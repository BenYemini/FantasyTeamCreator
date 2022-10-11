import requests
from constants import *
from FixturesData import *


class Player:
    def __init__(self, player_info):
        self.id = player_info['id']  # Player's id in the premier league api
        self.first_name = player_info['first_name']  # Player's first name
        self.last_name = player_info['second_name']  # Player's last name
        self.team = player_info['team']  # Player's team id in the premier league api
        self.price = float(player_info['now_cost']) / 10  # Player's price, pay attention: 122 == 12.2
        self.position = player_info['element_type']  # Player's position in int (GKP = 1, DEF = 2, MID = 3, FWD = 4)
        self.set_position()  # Changing position field from number to the corresponding position name
        self.status = player_info['status']  # Player's status: 'a' = Available, else: unavailable
        self.points_per_game = float(player_info['points_per_game'])  # Player's points per game played
        self.selected_by_percent = float(player_info['selected_by_percent'])  # The percentage that picked this player
        self.corners_freekicks_order = player_info['corners_and_indirect_freekicks_order']  # if 1 = True, else: False
        self.penalties_order = player_info['penalties_order']  # if 1 = True, else: False
        self.penalties_corners_grade = 0
        self.total_grade = 0
        self.active = False

    # Returns the players name.
    def get_name(self):
        return self.first_name + " " + self.last_name

    # Returns the players short name.
    def get_short_name(self):
        return self.first_name[0] + "." + self.last_name

    # Returns players position.
    def get_position(self):
        return self.position

    def get_points_per_game(self):
        return self.points_per_game

    # Sets the players position according to the following: 1 = GKP, 2 = DEF, 3 = MID, 4 = FWD
    def set_position(self):
        if self.position == 1:
            self.position = "GKP"
        elif self.position == 2:
            self.position = "DEF"
        elif self.position == 3:
            self.position = "MID"
        else:
            self.position = "FWD"
        return

    # Returns the player's price
    def get_price(self):
        return self.price

    # Returns the player's team id.
    def get_team(self):
        return self.team

    # Returns the player's total grade.
    def get_total_grade(self):
        return self.total_grade

    # Calculating and Returning the Players grade.
    # For players who reached a MIN_TOTAL_GRADE_NEEDED_TO_PASS an activity check and next fixture check will be made.
    # The idea behind filtering those who receive this check is to minimize the numer of get requests to the api, notice
    # that the forwards tend to have a lower grading then others, so they will be treated differently.
    # You can read more about it at the README.
    def get_player_grade(self, team_info):
        if not self.is_available:
            return 0

        total_grade = 0
        total_grade += self.points_per_game / (self.price / 10)
        if self.selected_by_percent / 100 > 0.5:
            total_grade += SELECTED_BY_MAJORITY_BONUS
        total_grade += self.penalties_corners_bonus()
        total_grade += team_strength_grade(team_info.get_strength())

        if total_grade > MIN_TOTAL_GRADE_NEEDED_TO_PASS or (self.get_position() == "FWD" and
                                                            total_grade > MIN_TOTAL_GRADE_NEEDED_TO_PASS_FOR_FWD):
            player_fixtures_data = self.get_player_fixtures_data()
            if not player_fixtures_data.is_active():  # Player is not active, and hence choosing him is a risk.
                return 0
            else:
                total_grade += player_fixtures_data.get_next_fixture_bonus()
        return total_grade

    # Set the players total grade according to the calculation at the relevant get method.
    def set_total_grade(self, grade):
        self.total_grade = grade

    # Fetching an info from a different endpoint, referring to player's upcoming and previous fixtures performance.
    # Returns a FixturesData object.
    def get_player_fixtures_data(self):
        element_summary_endpoint = "https://fantasy.premierleague.com/api/element-summary/{element_id}/"
        response = requests.get(element_summary_endpoint.format(element_id=self.id))
        if response:
            player_fixtures_data = FixturesData(response.json())  # Creating FixturesData object from json file.
            return player_fixtures_data
        else:
            raise Exception("The HTTP request to element summary endpoint failed!")

    def set_penalties_corners_grade(self, grade):
        self.penalties_corners_grade = grade
        return

    # Returns players grade according to his role at penalties, corner kicks and free kicks.
    # Notice that the bonus is different between players who play at different positions - fantasy logic
    # (defenders and midfielders gets more points for goals)
    def penalties_corners_bonus(self):
        grade = 0
        if self.penalties_order == 1:
            if self.position == "DEF":  # Defense
                grade += DEF_PENALTIES_BONUS
            elif self.position == "MID":  # Midfield
                grade += MID_PENALTIES_BONUS
            else:  # Forward
                grade += FWD_PENALTIES_BONUS
        if self.corners_freekicks_order == 1:
            grade += CORNERS_OR_FREEKICK_BONUS
            self.set_penalties_corners_grade(grade)
        return grade

    # Returns True if the player is available, False otherwise.
    def is_available(self):
        if self.status != 'a':
            return False

    # Print's the players name and total grade.
    def print(self):
        print(self.get_short_name() + " , total grade is: " + "{:.2f}".format(self.total_grade))


# The strength stands for the team level, in scale of 1-5.
# If the quality of the team is 4-5, then the probability for points is greater, therefore the player receives bonus
# If the quality of the team is 1-2, then the probability for points is smaller.
def team_strength_grade(strength):
    if strength == 5:
        return TOP_STRENGTH_TEAM_BONUS
    elif strength == 4:
        return GOOD_STRENGTH_TEAM_BONUS
    elif strength == 3:
        return AVERAGE_STRENGTH_TEAM_BONUS
    else:
        return BAD_STRENGTH_TEAM_DEDUCTION
