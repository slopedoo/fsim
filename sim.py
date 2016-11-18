# the start of a football simulator game
# todo: stats per player will be done later
#       for now the team reputation will basically determine the result
#       live commentary with scoreboard and stats will be added
#       strictly CLI for the time beeing
#       split files

import sys
import csv
import os
import unicodedata
from datetime import date
from datetime import datetime
#from pudb import set_trace; set_trace()

CONST_VERSION = "0.1"
CONST_SEASON = "2016/2017"
CONST_PLAYERS_PER_TEAM = 11
CONST_TEAMS_PER_LEAGUE = 20
CONST_MINS_PER_GAME = 90
CONST_PLAYER_DB = 'player_db.csv'
CONST_TEAM_DB = 'team_db.csv'

#-------------  class definitions -------------

class Player(object):

    def __init__(self, name, country, dob, club, position, number):
        self.name = name
        self.country = country
        self.dob = dob
        self.club = club
        self.position = position
        self.number = number

    def description(self):
        print(self.name, self.pos, self.age, self.country, self.club)

    def create_player(self, name, country, dob, cl):
        pass


class Club(object):

    def __init__(self, name, country, reputation):
        self.name = name
        self.country = country
        self.reputation = reputation
        self.squad = []
        self.points = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def win(self):
        self.points = self.points + 3
        self.wins = self.wins + 1

    def draw(self):
        self.points = self.points + 1
        self.draws = self.draws + 1

    def loss(self):
        self.losses = self.losses + 1

class League(object):

    def __init__(self, name, country, reputation, clubs):
        self.name = name
        self.country = country
        self.reputation = reputation
        self.clubs = clubs

class Country(object):

    def __init__(self, name, reputation, leagues):
        self.name = name
        self.reputation = reputation
        self.leagues = leagues

class Match(object):

    def __init__(self, home, away, date):
        self.home_team = home
        self.away_team = away
        self.date = date

    def home_squad(self, home_gk, home_def, home_mid, home_fwd):
        self.home_gk = home_gk
        self.home_def = []
        self.home_mid = []
        self.home_fwd = []

    def away_squad(self, away_gk, away_def, away_mid, away_fwd):
        self.away_gk = away_gk
        self.away_def = []
        self.away_mid = []
        self.away_fwd = []

    def result(self):
        self.result = result

    def play_match(self):
        pass

#------------- function definitions -------------

def pick_match_squad(club,match):
    # going with a 4-4-2 formation, option of changing formation will come later
    formation = "442"
    num_gk = 1
    num_def = formation[0]
    num_mid = formation[1]
    num_fwd = formation[2]
    if match.home_team == club.name:
        for i in range(num_gk):
            match.home_squad.home_gk = input("Starting goalkeeper: ")
        for i in range(num_def):
            choice = input("Add defender no.", i, "of", num_def)
            for i in range(int(club.squad)):
                if choice.capitalize() == club.squad[i][0] and club.squad[i][4].lower() == 'defender':
                    match.home_squad.home_def.append(choice.capitalize())
        for i in range(num_mid):
            choice = input("Add midfielder no.", i, "of", num_mid)
            for i in range(int(club.squad)):
                if choice.capitalize() == club.squad[i][0] and club.squad[i][4].lower() == 'midfielder':
                    match.home_squad.home_mid.append(choice.capitalize())
        for i in range(num_fwd):
            choice = input("Add forward no.", i, "of", num_fwd)
            for i in range(int(club.squad)):
                if choice.capitalize() == club.squad[i][0] and club.squad[i][4].lower() == 'forward':
                    match.home_squad.home_fwd.append(choice.capitalize())
    elif match.away_team == club.name:
        for i in range(num_gk):
            match.away_squad.away_gk = input("Starting goalkeeper: ")
        for i in range(num_def):
            choice = input("Add defender no.", i, "of", num_def)
            for i in range(int(club.squad)):
                if choice.capitalize() == club.squad[i][0] and club.squad[i][4].lower() == 'defender':
                    match.away_squad.away_def.append(choice.capitalize())
        for i in range(num_mid):
            choice = input("Add midfielder no.", i, "of", num_mid)
            for i in range(int(club.squad)):
                if choice.capitalize() == club.squad[i][0] and club.squad[i][4].lower() == 'midfielder':
                    match.away_squad.away_mid.append(choice.capitalize())
        for i in range(num_fwd):
            choice = input("Add forward no.", i, "of", num_fwd)
            for i in range(int(club.squad)):
                if choice.capitalize() == club.squad[i][0] and club.squad[i][4].lower() == 'forward':
                    match.away_squad.away_fwd.append(choice.capitalize())
    else:
        print("Something bad happened.")

def initiate_match(away_team, home_team, date):
    pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to Football Simulator version", CONST_VERSION)
    print("Type help to see available commands.\n")

# print available commands
def print_help():
    print("\n Available commands:\n",
            "help\t\t\tShow this help dialog\n",
            "clear\t\t\tClear the screen\n",
            "player search\t\tSearch for a player using name, team or country\n",
            "team search\t\tSearch for a team using name\n",
            "squad list\t\tSearch for a team to display the squad list\n",
            "print table\t\tPrint the season's league table"
    )

def player_output(name, country, dob, club, position, number):
    age = calculate_age(dob)
    print("  ",79*"_",
            "\n  | \n  |  Player Name:\t",name,
            "\n  |  Player Number:\t",number,
            "\n  |  Player Position:\t",position,
            "\n  |\n  |  \tDate of Birth:\t",dob,age,"years old."
            "\n  |  \tCountry:\t",country,
            "\n  |  \tClub:\t\t",club,
            "\n  |_______________________________________________________________________________")

def print_league_table():
    print("")
    for i in range(CONST_TEAMS_PER_LEAGUE):
        sys.stdout.write("   {:<25}{:<5}{:<5}{:1}{:8}\n".format(
            clubs[i].name,clubs[i].wins,clubs[i].losses,clubs[i].draws,clubs[i].points))
    print("")

# get age from DOB
def calculate_age(born):
    born = datetime.strptime(born, '%d/%m/%Y')
    today = date.today()
    years_difference = today.year - born.year
    is_before_birthday = (today.month, today.day) < (born.month, born.day)
    elapsed_years = years_difference - int(is_before_birthday)
    return elapsed_years

# add teams from DB to array of Clubs objects
def populate_league():
    with open(CONST_TEAM_DB, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            for field in row:
                clubs.append(Club(row[0],row[1],row[2])) # add club to to clubs array
                break

# add players to the clubs in the clubs[] array of objects
def populate_teams():
    with open(CONST_PLAYER_DB, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            exit_flag = False
            for field in row:
                for i in range(CONST_TEAMS_PER_LEAGUE):
                    if exit_flag:
                        break
                    elif clubs[i].name == row[3].upper():   # find the correct club
                        clubs[i].squad.append((row[0],row[1],row[2],row[3],row[4],row[5])) # add player to the club
                        exit_flag = True
                break

# search csv file for players
def search_player(search_string):
    with open(CONST_PLAYER_DB, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        print("\n   Search Results:")
        for row in reader:
            for field in row:
                field = ''.join(c for c in unicodedata.normalize('NFD', field)
                        if unicodedata.category(c) != 'Mn') # remove accents from search results for easier searching
                if search_string.capitalize() in field:
                    player_output(row[0],row[1],row[2],row[3],row[4],row[5])

# search club and print the roster
def search_club(club, clubs):
    template = "{0:>8}{1:1}{2:30}{3:15}{4:4}{5:>20}"
    for i in range(CONST_TEAMS_PER_LEAGUE):
        if club.upper() in clubs[i].name:
            print("\n")
            print("        ", clubs[i].name, "FULL SQUAD ROSTER")
            print("        ", CONST_SEASON, "SEASON")
            print("")
            print(template.format("NUMBER", "", "NAME", "POSITION", " AGE", "COUNTRY"))
            for j in range(len(clubs[i].squad)):
                print(template.format(
                    clubs[i].squad[j][5]," ",
                    clubs[i].squad[j][0],
                    clubs[i].squad[j][4],
                    calculate_age(clubs[i].squad[j][2]),
                    clubs[i].squad[j][1]))

def sub(sub_out, sub_in):
    sub_out = sub_out
    sub_in = sub_in
    for i in range(CONST_PLAYERS_PER_TEAM):
        if players_on[i] == sub_out:
            del players_on[i]
            players_on.append(sub_name)
            print(sub_out, "has been substituted off.",sub_in,"replaces him.")
        else:
            print("That player is not on the field.")


#------------- main program -------------
clubs = []
populate_league()
populate_teams()
clear_screen()
while True:
    inp = input("\nWhat would you like to do? ")
    if inp.lower() == "help":
        print_help()
    elif inp.lower() == "clear":
        clear_screen()
    elif inp.lower() == "player search":
        print("\n",82*"-")
        print("\n Search for a player using name, club or country. Type back to return to main menu.")
        search_string = ""
        while search_string.lower() != "back":
            if search_string.lower() == "clear":
                clear_screen()
            elif search_string == "":
                print(" Please enter a search string.")
            search_string = input("\n Enter player to search for: ")
            search_player(search_string)
        return
        clear_screen()
    elif inp.lower() == "team search":
        search_team()
    elif inp.lower() == "print table":
        print_league_table()
    elif inp.lower() == "squad list":
        print("\n Search for a club's squad list using the club name. Type back to return to main menu.")
        search_string = ""
        while search_string.lower() != "back":
            if search_string.lower() == "clear":
                clear_screen()
            elif search_string.lower() == "":
                print("Please enter a valid search string.")
            search_string = input("\n Enter team to search for: ")
            search_club(search_string, clubs)
        clear_screen()
        search_club(search_string, clubs)
    else:
        print("Could not find", inp, "\nType help to see available commands.")
