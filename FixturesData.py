from constants import *


class FixturesData:
    def __init__(self, json_fixtures_data):
        self.upcoming_fixtures = json_fixtures_data['fixtures']  # A list containing data about the next fixtures.
        self.history_fixtures = json_fixtures_data['history']  # A list containing data about previous fixtures.
        self.number_of_games = len(self.history_fixtures)  # Number of fixtures the player has played (or didn't play)
        self.next_fixture = json_fixtures_data['fixtures'][0]  # A data about next fixture.
        self.next_fixture_opponent_strength = json_fixtures_data['fixtures'][0]['difficulty']
        self.next_fixture_home = json_fixtures_data['fixtures'][0]['is_home']  # True if the next fixture is at home.
        self.next_fixture_opponent_id = json_fixtures_data['fixtures'][0]['id']
        self.active = False  # If the player is considered active, then this field will be True.
        self.next_fixture_bonus = 0  # The next fixture bonus grade.
        self.set_next_fixture_bonus()
        self.set_activity()

    # Sets the activity field.
    # If the player played at least a half of the game in each of the team's last 3 games, then his considered active.
    def set_activity(self):
        activity_counter = 0
        for i in range(1, MIN_NUM_OF_GAMES_ACTIVE + 1):
            if self.history_fixtures[self.number_of_games - i]['minutes'] >= MIN_MINUTES_NEEDED_TO_PASS:
                activity_counter += 1
        if activity_counter == MIN_NUM_OF_GAMES_ACTIVE:
            self.active = True

    # Returns True if the player is active, False otherwise.
    def is_active(self):
        return self.active

    # Calculates next fixture bonus, according to: home/away game and opponent strength.
    def set_next_fixture_bonus(self):
        if self.next_fixture_home:  # Checks if the team plays at home or away.
            self.next_fixture_bonus += HOME_GAME_BONUS
        else:
            self.next_fixture_bonus -= AWAY_GAME_DEDUCTION

        if self.next_fixture_opponent_id in TOP_5_TEAMS_ID:  # Currently top strength teams.
            self.next_fixture_bonus -= TOP_STRENGTH_TEAM_BONUS
        elif self.next_fixture_opponent_strength == 5:
            self.next_fixture_bonus -= TOP_STRENGTH_TEAM_BONUS  # Pay attention to the minus!
        elif self.next_fixture_opponent_strength == 4:
            self.next_fixture_bonus -= GOOD_STRENGTH_TEAM_BONUS  # Pay attention to the minus!
        elif self.next_fixture_opponent_strength == 3:
            self.next_fixture_bonus -= AVERAGE_STRENGTH_TEAM_BONUS  # Pay attention to the minus!
        else:
            self.next_fixture_bonus -= BAD_STRENGTH_TEAM_DEDUCTION  # Pay attention to the minus!

    # Returns the next fixture bonus.
    def get_next_fixture_bonus(self):
        return self.next_fixture_bonus
