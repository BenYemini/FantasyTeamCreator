class Team:
    def __init__(self, team_info):
        self.id = team_info['id']  # Team's id in the premier league api
        self.name = team_info['name']  # Team's full name.
        self.short_name = team_info['short_name']  # Team's shortened name.
        self.strength = 0
        self.strength_attack_home = team_info['strength_attack_home']  # Team's attack strength at home.
        self.strength_attack_away = team_info['strength_attack_away']  # Team's attack strength at away.
        self.strength_defence_home = team_info['strength_defence_home']  # Team's defense strength at home.
        self.strength_defence_away = team_info['strength_defence_away']  # Team's defense strength at away.
        self.picked = 0  # Counter for number of players picked to UserFantasyTeam, from this team.
        self.set_strength(int(team_info['strength']))  # In scale of 1-5 (1 - Worst, 5 - Best).

    # Returns team name.
    def get_name(self):
        return self.name

    # Returns team name shortened.
    def get_short_name(self):
        return self.short_name

    # Sets the team's strength.
    def set_strength(self, strength):
        if self.get_name() in ["Chelsea", "Arsenal", "Spurs", "Newcastle"]:
            self.strength = 5
        else:
            self.strength = strength

    # Returns the team strength.
    def get_strength(self):
        return self.strength

    # Returns the teams attack strength at home games.
    def get_strength_attack_home(self):
        return self.strength_attack_home

    # Returns the teams attack strength at away games.
    def get_strength_attack_away(self):
        return self.strength_attack_away

    # Returns the teams defense strength at home games.
    def get_strength_defence_home(self):
        return self.strength_defence_home

    # Returns the teams defense strength at away games.
    def get_strength_defence_away(self):
        return self.strength_defence_away

    # Returns the number of picked players to the user's team from this team object.
    def get_picked_players(self):
        return self.picked

    # If a player is chosen to UserTeam, then the "Picked_players" counter is added by 1.
    def set_picked_player(self):
        self.picked += 1

    # Print the teams name.
    def print_team(self):
        print(self.get_name())
