# the start of a football simulator game
# todo: stats per player will be done later
#       for now the team reputation will basically determine the result
#       live commentary with scoreboard and stats will be added
#       strictly CLI for the time beeing
#       split files

import csv
import os
from datetime import date
from datetime import datetime

CONST_VERSION = "0.1"
CONST_PLAYERS_PER_TEAM = 11
CONST_MINS_PER_GAME = 90
CONST_PLAYER_DB = 'player_db.csv'
CONST_TEAM_DB = 'team_db.csv'

#-------------  class definitions

class Player(object):

    def __init__(self, name, pos, dob, country, club, number):
        self.number = number
        self.name = name
        self.pos = pos
        self.dob = dob
        self.country = country
        self.club = club

    def description(self):
        print(self.name, self.pos, self.age, self.country, self.club)

class Club(object):

    def __init__(self, name, country, reputation, players):
        self.name = name
        self.country = country
        self.reputation = reputation
        self.players = players

class League(object):

    def __init__(self, name, country, reputation, teams):
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
        self.home = home
        self.away = away
        self.date = date

    def result(self):
        self.result = result

    def play_match(self):
        pass

#------------- function definitions

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
            "team search\t\tSearch for a team using name")

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

def calculate_age(born):
    born = datetime.strptime(born, '%d/%m/%Y')
    today = date.today()
    years_difference = today.year - born.year
    is_before_birthday = (today.month, today.day) < (born.month, born.day)
    elapsed_years = years_difference - int(is_before_birthday)
    return elapsed_years

def populate_team(team):
    pass

# search csv file for players
def search_player(search_string):
    if search_string == "":
        print(" Please enter a search string.")
        return
    with open(CONST_PLAYER_DB, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        print("\n   Search Results:")
        for row in reader:
            #print(row[1])
            for field in row:
                if search_string.capitalize() in field:
                    player_output(row[0],row[1],row[2],row[3],row[4],row[5])

def search_team():
    pass


#------------- main program
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
            search_string = input("\n Enter search query: ")
            search_player(search_string)
        clear_screen()
    elif inp.lower() == "team search":
        search_team()
    else:
        print("Could not find", inp, "\nType help to see available commands.")
