# Fantasy Team Creator - Premier league

## Introduction

**"Fantasy Team Creator" is a python Object-Oriented project that enables users to create a soccer fantasy team.**

The players are chosen to the team according to the grades they receive from the grading system that
I have developed (from my experience in fantasy and soccer).

I decided to build the Fantasy Team Creator based on the Premier League fantasy, because it's the biggest
and most relevant of them all.

**I encourage you to use the logic that was used by me during this project, and the actual code,
in order to build a team creator in other fantasy leagues!**

**If you aren't familiar with the idea of binary trees and Max-Heaps**, I recommend
reading about it before diving into the code - [Read More Here](https://www.geeksforgeeks.org/max-heap-in-python/).

**If you aren't familiar with the idea of Object-Oriented Programming**, I recommend reading about it before diving
into the code - [Read more here](https://www.educative.io/blog/object-oriented-programming)

**If you aren't familiar with the "Fantasy Premier League" (FPL)** - 
[Read More Here](https://www.fourfourtwo.com/features/fpl-what-is-fantasy-football-and-how-does-it-work).

## Project's Structure
The project is built from 3 main classes:
* **FantasyTeamCreator** - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/3bae827df09aac0e6994ed399c181a722a9add8d/README.md?plain=1#L149) 
* **UserFantasyTeam** - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/3bae827df09aac0e6994ed399c181a722a9add8d/README.md?plain=1#L168)
* **FantasyTeamRenderer** - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/3bae827df09aac0e6994ed399c181a722a9add8d/README.md?plain=1#L189![image](https://user-images.githubusercontent.com/112508491/195093227-77e50f58-47c5-44ba-9da4-c13c4f0ab1c9.png))

And 4 more classes:
* **Player** - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/3bae827df09aac0e6994ed399c181a722a9add8d/README.md?plain=1#L210)
* **Team** - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/3bae827df09aac0e6994ed399c181a722a9add8d/README.md?plain=1#L240)
* **MaxHeap** - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/3bae827df09aac0e6994ed399c181a722a9add8d/README.md?plain=1#L251)
* **FixturesData** - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/3bae827df09aac0e6994ed399c181a722a9add8d/README.md?plain=1#L264)

**I highly recommend reading about the classes before you run the program - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/3bae827df09aac0e6994ed399c181a722a9add8d/README.md?plain=1#L148).**


## Install
Before you run the program, please install requirements by:
```bash
pip install -r requirements.txt
```

## Running the application
Run the application by running ``main.py`` file.
```bash
python main.py
```

## Getting Started

1. Fetch the data, using requests library, from the bootstrap endpoint of the FPL api - [Read more here](https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19).  
```
bootstrap_endpoint = "https://fantasy.premierleague.com/api/bootstrap-static/"
response_bootstrap = requests.get(bootstrap_endpoint)
if response_bootstrap:
    data = response_bootstrap.json()
else:
    raise Exception("The HTTP request to bootstrap failed!")

```
2. Receive budget from client (the FPL allowed budget is 100).
```
budget = float(input("What is your budget?" + "\n"))
```
3. Create FantasyTeamCreator object using data from the api about teams and players ('elements').
```
fantasy_team_creator = FantasyTeamCreator(data['teams'], data['elements'])
```
4. Use the "create_team" method in order to assemble a team, according to the budget given.  
This method will return UserFantasyTeam object containing the players chosen for the team.
```
user_team = fantasy_team_creator.create_team(budget)
```
5. Use the "set_first_squad" method to decide who will be at the first squad.
```
user_team.set_first_squad()
```
6. Use the "set_sub_players" method to decide the number of each sub player.
```
user_team.set_sub_players()
```
7. Create a FantasyTeamRenderer object, that will receive the UserFantasyTeam object.
```
fantasy_team_renderer = FantasyTeamRenderer(user_team)
```
8. Use the "render_squad" method in order to print the first squad players.
```
fantasy_team_renderer.render_first_squad()
```
9. Use the "render_subs" method in order to print the sub players.
```
fantasy_team_renderer.render_subs()
```
10. Use the "render_captains" method in order to print the team's first and second captain.
```
fantasy_team_renderer.render_captains()
```


## Using the application
````
What is your budget?
100

The left budget is: 0.9

First squad:

GKP:
J.Malheiro de Sá , total grade is: 11.90

DEF:
W.Saliba , total grade is: 13.40
A.Young , total grade is: 12.02
E.Dier , total grade is: 11.63
K.Trippier , total grade is: 11.09

MID:
G.Martinelli Silva , total grade is: 13.19
G.Xhaka , total grade is: 12.42
W.Zaha , total grade is: 11.50
A.Mac Allister , total grade is: 11.17
E.Eze , total grade is: 11.09

FWD:
E.Haaland , total grade is: 11.96

Sub players:

1
H.Kane , total grade is: 10.84
2
J.Cancelo , total grade is: 10.52
3
I.Toney , total grade is: 9.78
4
H.Lloris , total grade is: 11.20

Team Captain:
E.Haaland , total grade is: 11.96

Second Team Captain:
G.Martinelli Silva , total grade is: 13.19
````
## Main Classes
### FantasyTeamCreator

when initiated creates:
* List[**Team**] - for teams
* List[**Player**] - for players
* Dictionary containing 4 **MaxHeap** - one for each position
* **UserFantasyTeam**

#### "Create_team"
This is the main method of this class, in which:  
1. Each player receives a grade according to the grading system - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/1c2fd682d6496ced4da5358e02693c009ceb1372/FantasyTeamCreator.py#L28).
2. Each player is inserted to a MaxHeap, according to his position - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/fe978bd5ac28dbdd8c683b3b5561d8e61de57385/MaxHeap.py#L12).
3. The roots of the MaxHeaps are being compared (Player objects) - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/1c2fd682d6496ced4da5358e02693c009ceb1372/FantasyTeamCreator.py#L83![image](https://user-images.githubusercontent.com/112508491/195096807-593bee21-4f71-4718-8e9b-5559f56c9128.png)).
4. Players are being picked to the UserTeam - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/fe978bd5ac28dbdd8c683b3b5561d8e61de57385/FantasyTeamCreator.py#L37). 
5. Players are being appended to the relevant list in the UserTeam - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/412e8e807e4242bf28c9ec1b7f3c8f60c10aa464/UserFantasyTeam.py#L80).
6. Prints the left budget

**Return** - UserFantasyTeam

*Pay attention - While picking each player we check if the move is legal* - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/1c2fd682d6496ced4da5358e02693c009ceb1372/FantasyTeamCreator.py#L115).

### UserFantasyTeam
This class when initiated creates:
* List[**Player**] - for Goalkeepers
* List[**Player**] - for Defenders
* List[**Player**] - for Midfielders
* List[**Player**] - for Forwards
* Dictionary containing 4 List[**Player**] (one for each position) - for first squad
* List[Player] - for sub players
* **Player** - for Team Captain selection
* **Player** - for Team Second Captain selection


#### "set_first_squad"

Pick's the 11 top graded players from the lists to be in the first squad -*under FPL limitations* - [Read more here](https://fantasy.premierleague.com/help/rules).  
Call's the "set_captains" method, to set the team's first and second captain.

#### "set_sub_players"

places the sub players in the right sub number, according to their total grades.

### FantasyTeamRenderer
This class when initiated creates:
* List[**Player**] - for first squad
* List[**Player**] - for sub players
* **Player** - for Team Captain
* **Player** - for Second Team Captain

#### "render_first_squad"

Prints the first squad players, according to positions.

#### "render_subs"
Prints the sub players, according to the number of the sub.

#### "render_captains"
Prints the team captain and second captain.

*At this point, **there is no front code** to present this project (still 
haven't learned it yet - just finished my first year :)*

## More Classes
### Player

This class when initiated receives many parameters about a player and creates fields accordingly - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/412e8e807e4242bf28c9ec1b7f3c8f60c10aa464/Player.py#L7![image](https://user-images.githubusercontent.com/112508491/195097129-34620144-771a-4a60-bc4d-e9d672beab4e.png)).

#### "get_player_grade"
The main method of this class, in which players are being graded according to several parameters:

* **Status** - if the player is unavailable for selection, grade is automatically set to 0.  

* **Points vs Price** - the ratio between players points per game to his price.  

* **The Wisdom of Crowds** - if the player is selected to the next game-week by majority of fantasy players, he receives a bonus.  

* **Penalties or Freekick taker**- if the player is the first penalty/ freekick/ corners taker he receives a bonus.  

* **Team Strength** - player receives a bonus for the team he plays for.  

* **Activity Check** - if the player had average of 45 minutes played in the last 3 games, then his considered to be active

* **Next Fixture** - player receives a bonus for the next fixture according to: home/ away, opponent team strength.  

*The points received for each of the parameters have been calculated for a long time, and relay on statistics and
logic.*

*Of course, you can play with the numbers at the constants file as you'll like and get different outcomes!*

*during the* Activity Check *and the Next Fixture methods a* **FixturesData**
*object is created - [Read more here]*

### Team
This class when initiated receives many parameters about a team and creates fields accordingly - [Read more here](https://github.com/BenYemini/FantasyTeamCreator/blob/412e8e807e4242bf28c9ec1b7f3c8f60c10aa464/Team.py#L2![image](https://user-images.githubusercontent.com/112508491/195097293-861646e1-3ce9-4c56-ba8b-477f44c89a3f.png)).

#### "set_picked_player"
This method is initiated when a player is added to **UserFantasyTeam**,
it adds 1 to the "picked" field.

*At this moment, the use of the "Team" object is limited, there are
fields that yet to be used.* 

### MaxHeap
I chose this data structure for holding the players objects, before preforming
the comparison between them, because it allows:
* FindMax - O(1)
* DeleteMax - O(log(n)).

This class when initiated creates two fields:
* List[Player] - holds Player objects in a heap structure.
* int - holds the size of the heap.

I made several modifications from the class that was 
built by GeekForGeeks, you can read about it at their website! - [Read more here](https://www.geeksforgeeks.org/max-heap-in-python/).

### FixtureData
This class when initiated creates many fields that holds data about: 
* Player's performance in previous fixtures.
* Player's team upcoming fixtures.

#### "set_next_fixture_bonus"
This method is initiated when a FixturesData object is created.
it calculates a bonus for the player's total grade, according to home/away game and 
opponent strength.

#### "set_activity"
This method is initiated when a FixturesData object is created.  
It sets the activity field, according to the definition of "active player" that was decided by me.  
Of course, there can be several definitions to what is an "active player".

