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
from collections import Counter
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

        self.home_squad_gk = []
        self.home_squad_def = []
        self.home_squad_mid = []
        self.home_squad_fwd = []

        self.away_squad_gk = []
        self.away_squad_def = []
        self.away_squad_mid = []
        self.away_squad_fwd = []

    def home_squad(self, formation, club):
        choice = input("Starting goalkeeper: ")
        squad_size = len(club.squad)
        print(squad_size)
        fail_flag = False
        for i in range(squad_size):   # todo: optimize range to the relevant positions instead of whole squad
            if choice.capitalize() in club.squad[i][0] and club.squad[i][4].lower() == 'goalkeeper':
                self.home_squad_gk.append(club.squad[i])
                print("You added",club.squad[i])
                break
            else:
                print("Player not found. Try again.")
                choice = input("Starting goalkeeper: ")
        j = 0
        while j < int(formation[0]):
            print("Add defender", j+1, "of", formation[0])
            choice = input()
            for i in range(squad_size):
                if choice.capitalize() in club.squad[i][0] and club.squad[i][4].lower() == 'defender':
                    self.home_squad_def.append(club.squad[i])
                    print("You added",club.squad[i])
                    fail_flag = False
                    break
                elif i == squad_size-1:
                    fail_flag = True
            if fail_flag:
                print("Player not found. Try again.")
            else:
                j += 1
        j = 0
        while j < int(formation[1]):
            print("Add midfielder", j+1, "of", formation[0])
            choice = input()
            for i in range(squad_size):
                if choice.capitalize() in club.squad[i][0] and club.squad[i][4].lower() == 'midfielder':
                    self.home_squad_mid.append(club.squad[i])
                    print("You added",club.squad[i])
                    fail_flag = False
                    break
                elif i == squad_size-1:
                    fail_flag = True
            if fail_flag:
                print("Player not found. Try again.")
            else:
                j += 1
        j = 0
        while j < int(formation[2]):
            print("Add forward", j+1, "of", formation[0])
            choice = input()
            for i in range(squad_size):
                if choice.capitalize() in club.squad[i][0] and club.squad[i][4].lower() == 'forward':
                    self.home_squad_fwd.append(club.squad[i])
                    print("You added",club.squad[i])
                    fail_flag = False
                    break
                elif i == squad_size-1:
                    fail_flag = True
            if fail_flag:
                print("Player not found. Try again.")
            else:
                j += 1

    def away_squad(self, formation, club):
        choice = input("Starting goalkeeper: ")
        squad_size = len(club.squad)
        print(squad_size)
        exit_flag = False
        fail_flag = False
        for i in range(squad_size):   # todo: optimize range to the relevant positions instead of whole squad
            if choice.capitalize() in club.squad[i][0] and club.squad[i][4].lower() == 'goalkeeper':
                self.away_squad_gk.append(club.squad[i])
                print("You added",club.squad[i])
                break
            else:
                print("Player not found. Try again.")
                choice = input("Starting goalkeeper: ")
        j = 0
        while j < int(formation[0]):
            print("Add defender", j+1, "of", formation[0])
            choice = input()
            exit_flag = False
            for i in range(squad_size):
                if exit_flag:
                    break
                if choice.capitalize() in club.squad[i][0] and club.squad[i][4].lower() == 'defender':
                    self.away_squad_def.append(club.squad[i])
                    print("You added",club.squad[i])
                    exit_flag = True
                elif i == squad_size-1:
                    fail_flag = True
            if fail_flag:
                print("Player not found. Try again.")
            else:
                j += 1
        i = 0
        while j < int(formation[1]):
            print("Add midfielder", j+1, "of", formation[0])
            choice = input()
            exit_flag = False
            for i in range(squad_size):
                if exit_flag:
                    break
                if choice.capitalize() in club.squad[i][0] and club.squad[i][4].lower() == 'midfielder':
                    self.away_squad_mid.append(club.squad[i])
                    print("You added",club.squad[i])
                    exit_flag = True
                elif i == squad_size-1:
                    fail_flag = True
            if fail_flag:
                print("Player not found. Try again.")
            else:
                j += 1
        i = 0
        while j < int(formation[2]):
            print("Add forward", j+1, "of", formation[0])
            choice = input()
            exit_flag = False
            for i in range(squad_size):
                if exit_flag:
                    break
                if choice.capitalize() in club.squad[i][0] and club.squad[i][4].lower() == 'forward':
                    self.away_squad_fwd.append(club.squad[i])
                    print("You added",club.squad[i])
                    exit_flag = True
                elif i == squad_size-1:
                    fail_flag = True
            if fail_flag:
                print("Player not found. Try again.")
            else:
                j += 1

    def result(self):
        self.result = result

    def play_match(self):
        pass

#------------- function definitions -------------

def pick_match_squad(club,match):
    # going with a 4-4-2 formation, option of changing formation will come later
    formation = "442"
    if match.home_team == club.name:
        match.home_squad(formation,club)
    elif match.away_team == club.name:
        match.home_squad(formation,club)
    else:
        print("Something bad happened.")

def initiate_match(away_team, home_team, date):
    pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to Football Simulator version", CONST_VERSION)
    print("Type help to see available commands.\n")

def san_txt(field):
    return ''.join(c for c in unicodedata.normalize('NFD', field)
        if unicodedata.category(c) != 'Mn') # remove accents from search results for easier searching

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
                        name = san_txt(row[0])
                        clubs[i].squad.append((name,row[1],row[2],row[3],row[4],row[5])) # add player to the club
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
match_120816 = Match('CHELSEA','ARSENAL','12.08.2016')
pick_match_squad(clubs[3], match_120816)
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
