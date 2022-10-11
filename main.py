import requests
from FantasyTeamRenderer import *
from FantasyTeamCreator import *

bootstrap_endpoint = "https://fantasy.premierleague.com/api/bootstrap-static/"
response_bootstrap = requests.get(bootstrap_endpoint)
if response_bootstrap:
    data = response_bootstrap.json()
else:
    raise Exception("The HTTP request to bootstrap failed!")

budget = float(input("What is your budget?" + "\n"))
fantasy_team_creator = FantasyTeamCreator(data['teams'], data['elements'])
user_team = fantasy_team_creator.create_team(budget)
user_team.set_first_squad()
user_team.set_sub_players()
fantasy_team_renderer = FantasyTeamRenderer(user_team)
fantasy_team_renderer.render_first_squad()
fantasy_team_renderer.render_subs()
fantasy_team_renderer.render_captains()
