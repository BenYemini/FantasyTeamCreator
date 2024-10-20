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
fantasy_team_creator = FantasyTeamCreator(data['teams'], data['elements'], budget)
user_team = fantasy_team_creator.create_team()

user_team.set_first_squad()
user_team.set_sub_players()

fantasy_team_renderer = FantasyTeamRenderer(user_team)
fantasy_team_renderer.render_first_squad()
fantasy_team_renderer.render_subs()
fantasy_team_renderer.render_captains()
fantasy_team_renderer.render_remaining_budget()

while True:
    user_decision = input("Would you like to render your First Squad total grades in a graph?" + "\n").lower()
    if user_decision == "yes":
        fantasy_team_renderer.render_graph_representation_first_squad()
        break
    elif user_decision == "no":
        break

    else:
        print("\n" + "Yes or No answer please." + "\n")