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
import time
import random
import re
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
CONST_FIXTURES_EPL = 'fixtures_epl.csv'

#-------------  class definitions -------------

class Reprinter:
    def __init__(self):
        self.text = ''

    def moveup(self, lines):
        for _ in range(lines):
            sys.stdout.write("\x1b[A")

    def reprint(self, text):
        # Clear previous text by overwritig non-spaces with spaces
        self.moveup(self.text.count("\n"))
        sys.stdout.write(re.sub(r"[^\s]", " ", self.text))

        # Print new text
        lines = min(self.text.count("\n"), text.count("\n"))
        self.moveup(lines)
        sys.stdout.write(text)
        self.text = text

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
        self.training = {
                'defending' : 0,
                'passing' : 0,
                'attacking' : 0
                }
        self.squad = []
        self.points = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def win(self):
        self.points += 3
        self.wins += 1

    def draw(self):
        self.points += 1
        self.draws += 1

    def loss(self):
        self.losses += 1

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

    def __init__(self, home, away, date, league):
        self.home_team = home
        self.away_team = away
        self.date = date
        self.league = league
        self.home_score = 0
        self.away_score = 0
        self.match_stats = { 'possession' : [50,50],
                             'shots' : [0,0],
                             'fouls' : [0,0] }

        # these should be made into one home_squad dict instead of several lists
        self.home_squad_gk = []
        self.home_squad_def = []
        self.home_squad_mid = []
        self.home_squad_fwd = []

        self.away_squad_gk = []
        self.away_squad_def = []
        self.away_squad_mid = []
        self.away_squad_fwd = []

    def pick_squad(self, formation, club, side):
        print("\n  Select match squad for the game",self.home_team.capitalize(),
                "vs", self.away_team.capitalize(), "on", self.date, "\n")
        squad_size = len(club.squad)
        if self.pick_player(squad_size, club, 'goalkeeper', side, formation):
            print("\n  Squad selection has been cancelled.")
            return
        if self.pick_player(squad_size, club, 'defender', side, formation):
            print("\n  Squad selection has been cancelled.")
            return
        if self.pick_player(squad_size, club, 'midfielder', side, formation):
            print("\n  Squad selection has been cancelled.")
            return
        if self.pick_player(squad_size, club, 'forward', side, formation):
            print("\n  Squad selection has been cancelled.")
            return

    def pick_player(self, squad_size, club, pos, side, formation):
        i = j = f = 0
        fail_flag = False
        picked = []
        prev_pos = 0
        num_pos = count_pos(club,pos) # number of players in the position
        player_by_position(pos, club)
        if pos == 'defender':
            f = formation[0] # f = number of positions available
            prev_pos = count_pos(club,'goalkeeper') # get start of search index
        elif pos == 'midfielder':
            f = formation[1]
            prev_pos = count_pos(club,'defender')+count_pos(club,'goalkeeper')
        elif pos == 'forward':
            f = formation[2]
            prev_pos = count_pos(club,'midfielder')+count_pos(club,'defender')+count_pos(club,'goalkeeper')
        elif pos == 'goalkeeper':
            f = 1
        while j < int(f):
            print("\n  Add", pos.lower(), j+1, "of", f, "-- (", pos_names(pos,formation, j), ")")
            choice = input("  >")
            if choice == "cancel":
                if side == 'home': # discard choices made if user cancels selection process
                    self.home_squad_gk = self.home_squad_def = self.home_squad_mid = self.home_squad_fwd = []
                elif side == 'away':
                    self.away_squad_gk = self.away_squad_def = self.away_squad_mid = self.away_squad_fwd = []
                return True
            elif choice == "":
                print("  You didn't enter a player name. Try again. Type cancel to return to menu.")
            else:
                if i != 0:
                    i = prev_pos - 1     # get the start index   | this makes sure that we search
                tot = prev_pos-1+num_pos # end index             | only for player in the right position
                while i <= tot:
                    player_name = club.squad[i][0].split() # split the name so the user can search either first or last name
                    full_name = player_name[0]+" "+player_name[-1]
                    if choice.capitalize() == player_name[0] or choice.capitalize() == player_name[-1] or choice.title() == full_name and club.squad[i][4].lower() == pos:
                        if any(club.squad[i][0] in s for s in picked):
                            print("\n", club.squad[i][0], "is already picked.") # don't let user add player twice
                            fail_flag = True
                        elif side.lower() == 'home': # check if home or away side
                            if pos.lower() == 'defender':
                                self.home_squad_def.append(club.squad[i]) # append picked player to the match squad
                                picked.append(club.squad[i][0]) # register that the player is picked
                                print("\n    Added", club.squad[i][0], "as", pos_names(pos,formation,j))
                                fail_flag = False
                                break
                            elif pos.lower() == 'midfielder':
                                self.home_squad_mid.append(club.squad[i])
                                picked.append(club.squad[i][0])
                                print("\n    Added", club.squad[i][0], "as", pos_names(pos,formation,j))
                                fail_flag = False
                                break
                            elif pos.lower() == 'forward':
                                self.home_squad_fwd.append(club.squad[i])
                                picked.append(club.squad[i][0])
                                print("\n    Added", club.squad[i][0], "as", pos_names(pos,formation,j))
                                fail_flag = False
                                break
                            elif pos.lower() == 'goalkeeper':
                                self.home_squad_gk.append(club.squad[i])
                                picked.append(club.squad[i][0])
                                print("\n    Added", club.squad[i][0], "as", pos_names(pos,formation,j))
                                fail_flag = False
                                break
                            else:
                                print("Something has gone wrong.")
                        elif side.lower() == 'away':
                            if pos.lower() == 'defender':
                                self.away_squad_def.append(club.squad[i])
                                picked.append(club.squad[i][0])
                                print("\n    Added", club.squad[i][0], "as", pos_names(pos,formation,j))
                                fail_flag = False
                                break
                            elif pos.lower() == 'midfielder':
                                self.away_squad_mid.append(club.squad[i])
                                picked.append(club.squad[i][0])
                                print("\n    Added", club.squad[i][0], "as", pos_names(pos,formation,j))
                                fail_flag = False
                                break
                            elif pos.lower() == 'forward':
                                self.away_squad_fwd.append(club.squad[i])
                                picked.append(club.squad[i][0])
                                print("\n    Added", club.squad[i][0], "as", pos_names(pos,formation,j))
                                fail_flag = False
                                break
                            elif pos.lower() == 'goalkeeper':
                                self.away_squad_gk.append(club.squad[i])
                                picked.append(club.squad[i][0])
                                print("\n    Added", club.squad[i][0], "as", pos_names(pos,formation,j))
                                fail_flag = False
                                break
                            else:
                                print("Something has gone wrong.")
                    i += 1
                    if i == tot:
                        fail_flag = True
                if fail_flag:
                    print(" Try again.")
                else:
                    j+=1

    def result(self):
        self.result = ""

    def play_match(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n Welcome to today's match on", self.date)
        print(" Today it is",self.home_team.capitalize(), "v", self.away_team.capitalize())
        print("")
        sec = min = 0 # start match at 0:00
        end = CONST_MINS_PER_GAME
        template = "{0:35}{1:35}"
        reprinter = Reprinter()
        while min <= end: # run match until 90 mins
            time.sleep(0.001)
            event_check(self, min, sec, reprinter)
            print(template.format(str(min)+":"+str(sec).zfill(2), str(self.home_score)+"-"+str(self.away_score)), end="\r ")
            if sec == 59: # 60 sec == 1 min
                min += 1
                sec = 0
            else:
                sec += 1
            if min == 45 and sec == 0:
                print(" --- Half time. The score is", str(self.home_score)+"-"+str(self.away_score), "--- ")
                input(" -- Press enter to start 2nd half. -- ")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n Welcome to today's match on", self.date)
                print(" Today it is",self.home_team.capitalize(), "v", self.away_team.capitalize())
                print("")
        print("\n\n\n\n\n FULL TIME!")
        print(" Final result:", self.home_team.capitalize(), self.home_score, "-", self.away_score, self.away_team.capitalize())


#------------- function definitions -------------

# match engine in its infancy
def event_check(match, min, sec, reprinter):
    num_lines = 0
    if random.randrange(0,1000) > 995: # home team has the ball
        time.sleep(1)
        sys.stdout.write("\n "+match.home_team.capitalize()+" controls the ball.")
        sys.stdout.flush()
        num_lines += 1
        if random.randrange(0,1000) > 997: # home team scores
            sys.stdout.write("\n "+match.home_team.capitalize()+" goal!")
            sys.stdout.flush()
            match.home_score += 1
            num_lines += 1
            moveup(num_lines)
            return
    if random.randrange(0,1000) > 997: # away team has the ball
        time.sleep(1)
        sys.stdout.write("\n "+match.away_team.capitalize()+" controls the ball.")
        sys.stdout.flush()
        num_lines += 1
        if random.randrange(0,1000) > 999: # away team scores
            sys.stdout.write("\n "+match.away_team.capitalize()+" goal!")
            sys.stdout.flush()
            match.away_score += 1
            num_lines += 1
            moveup(num_lines)
            return
    reprinter.moveup(num_lines)

def posession():
    pass

def attack():
    pass

def chance():
    pass

def shot():
    pass

def goal():
    pass

def miss():
    pass

def corner():
    pass

def tackle():
    pass

def foul():
    pass

def freekick():
    pass

def penalty():
    pass

def yellow_card():
    pass

def red_card():
    pass

def counter_attack():
    pass

def pos_names(pos, formation, j):
    if pos == 'defender' and formation == '442':
        if j == 0:
            return("Right back")
        elif j == 1:
            return("Right central defender")
        elif j == 2:
            return("Left central defender")
        elif j == 3:
            return("Left back")
    elif pos == 'midfielder' and formation == '442':
        if j == 0:
            return("Right midfielder")
        elif j == 1:
            return("Right central midfielder")
        elif j == 2:
            return("Left central midfielder")
        elif j == 3:
            return("Left midfielder")
    elif pos == 'forward' and formation == '442':
        if j == 0:
            return("Right centre forward")
        elif j == 1:
            return("Left centre forward")

def count_pos(club, pos):
    squad_size = len(club.squad)
    counter = 0
    for i in range(squad_size):
        if club.squad[i][4].lower() == pos:
            counter += 1
    return counter


def show_match_squad(club, match, formation):
    if club.name.lower() == match.home_team.lower() and formation == '442':
        print_442(match,'home')
    elif club.name.lower() == match.away_team.lower() and formation == '442':
        print_442(match,'away')

def print_442(match, side):
    template_gk = "{0:15}{1:20}{2:5}{3:20}{4:15}"
    template = "{0:25}{1:25}{2:25}{3:25}"
    if side == 'home':
        if len(match.home_squad_gk) == 1 and len(match.home_squad_def) == 4 and \
                len(match.home_squad_mid) == 4 and len(match.home_squad_fwd) == 2:
            print("\n\n")
            print(template_gk.format("","",match.home_squad_gk[0][0],"",""))
            print("\n\n\n\n")
            print(template.format(match.home_squad_def[0][0],
                                  match.home_squad_def[1][0],
                                  match.home_squad_def[2][0],
                                  match.home_squad_def[3][0]))
            print("\n\n\n\n")
            print(template.format(match.home_squad_mid[0][0],
                                  match.home_squad_mid[1][0],
                                  match.home_squad_mid[2][0],
                                  match.home_squad_mid[3][0]))
            print("\n\n\n\n")
            print(template.format("",
                                  match.home_squad_fwd[0][0],
                                  match.home_squad_fwd[1][0],
                                  ""))
            print("\n\n")
        else:
            print("  You haven't picked your line-up yet. Type <pick match squad> to start.")
    elif side == 'away':
        if len(match.away_squad_gk) == 1 and len(match.away_squad_def) == 4 and \
                len(match.away_squad_mid) == 4 and len(match.away_squad_fwd) == 2:
            print("\n\n")
            print(template_gk.format("","",match.away_squad_gk[0][0],"",""))
            print("\n\n")
            print(template.format(match.away_squad_def[0][0],
                                  match.away_squad_def[1][0],
                                  match.away_squad_def[2][0],
                                  match.away_squad_def[3][0]))
            print("\n\n")
            print(template.format(match.away_squad_mid[0][0],
                                  match.away_squad_mid[1][0],
                                  match.away_squad_mid[2][0],
                                  match.away_squad_mid[3][0]))
            print("\n\n")
            print(template.format("",
                                  match.away_squad_fwd[0][0],
                                  match.away_squad_fwd[1][0],
                                  ""))
            print("\n\n")
        else:
            print("  You haven't picked your line-up yet. Type <pick match squad> to start.")


def player_by_position(pos, club):
    template = "{0:>8}{1:1}{2:30}{3:15}{4:4}{5:>20}"
    print("\n ", pos.upper())
    print("")
    print(template.format("NUMBER", "", "NAME", "POSITION", " AGE", "COUNTRY"))
    for i in range(len(club.squad)):
        if club.squad[i][4].lower() == pos:
            print(template.format(
                club.squad[i][5]," ",
                club.squad[i][0],
                club.squad[i][4],
                calculate_age(club.squad[i][2]),
                club.squad[i][1]))

def pick_match_squad(club,match):
    # going with a 4-4-2 formation, option of changing formation will come later
    formation = "442"
    if match.home_team == club.name:
        match.pick_squad(formation,club, 'home')
    elif match.away_team == club.name:
        match.pick_squad(formation,club, 'away')
    else:
        print("Wrong team name entered. Make sure to spell it correctly.")

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
            "exit\t\t\tExit the application\n",
            "\n",
            "player search\t\tSearch for a player using name, team or country\n",
            "squad list\t\tSearch for a team to display the squad list\n",
            "club fixtures\t\tShow the fixtures of a specific team\n",
            "fixture search\t\tSearch fixture by teams\n",
            "pick match squad\tPick the squad for the next game\n",
            "show match squad\tShow the line-up for the next game\n",
            "print table\t\tPrint the season's league table"
    )

def player_output(name, country, dob, club, position, number):
    age = calculate_age(dob)
    print("  ",79*"_",
            "\n  | \n  |  Player Name:\t",name,
            "\n  |  Player Number:\t",number,
            "\n  |  Player Position:\t",position,
            "\n  |\n  |  Date of Birth:\t",dob,age,"years old."
            "\n  |  Country:\t\t",country,
            "\n  |  Club:\t\t",club,
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

# add teams from DB to list of Clubs objects
def populate_league():
    with open(CONST_TEAM_DB, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            for field in row:
                clubs.append(Club(row[0],row[1],row[2])) # add club to to clubs list
                break

# add players to the clubs in the clubs[] list of objects
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
                if search_string.title() in field:
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

def add_fixtures(league):
    with open(CONST_FIXTURES_EPL, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            for field in row:
                fixtures.append(Match(row[1],row[2],row[0],league)) # add fixtures to the fixtures list
                break

def club_fixtures(club,fixtures):
    print("")
    template = "{0:>25}{1:^5}{2:25}{3:15}"
    for i in range(len(fixtures)):
        if club.lower() in fixtures[i].home_team.lower() or\
                club.lower() in fixtures[i].away_team.lower(): # if club is either home or away team, print the fixture
            if fixtures[i].result == "H" or fixtures[i].result == "T" or fixtures[i].result == "A": # if the fixture has been played
                print(template.format(fixtures[i].home_team,                                        # and has a result, print it
                      str(fixtures[i].home_score)+"-"+str(fixtures[i].away_score),
                      fixtures[i].away_team, fixtures[i].date))
            else:
                print(template.format(fixtures[i].home_team, "v", fixtures[i].away_team, fixtures[i].date))

def search_fixture(fixtures):
    team_one = input("\n  Enter the first team to search for: ")
    team_two = input("  Enter the second team to search for: ")
    print("")
    template = "{0:>25}{1:^5}{2:25}{3:15}"
    for i in range(len(fixtures)):
        if team_one.lower() in fixtures[i].home_team.lower() and team_two.lower() in fixtures[i].away_team.lower() or team_one.lower() in fixtures[i].away_team.lower() and team_two.lower() in fixtures[i].home_team.lower():
            if fixtures[i].result == "H" or fixtures[i].result == "T" or fixtures[i].result == "A":
                print(template.format(fixtures[i].home_team,
                      str(fixtures[i].home_score)+"-"+str(fixtures[i].away_score),
                      fixtures[i].away_team, fixtures[i].date))
            else:
                print(template.format(fixtures[i].home_team, "v", fixtures[i].away_team, fixtures[i].date))


#------------- main program -------------
clubs = []
fixtures = []
populate_league()
populate_teams()
add_fixtures('EPL')
clear_screen()
match_120816 = Match('CHELSEA','ARSENAL','12.08.2016', 'EPL')
match_120816.play_match()
while True:
    inp = input("\n  What would you like to do? ")
    if inp.lower() == "help":
        print_help()
    elif inp.lower() == "clear":
        clear_screen()
    elif inp.lower() == "player search":
        print("\n",82*"-")
        print("\n Search for a player using name, club or country. Type back to return to main menu.")
        search_string = " "
        while search_string.lower() != "back":
            if search_string.lower() == "clear":
                clear_screen()
            elif search_string == "":
                print(" Please enter a search string.")
            search_string = input("\n Enter player to search for: ")
            search_player(search_string)
        clear_screen()
    elif inp.lower() == "club fixtures":
        search_string = input("\n Enter team to search for: ")
        club_fixtures(search_string, fixtures)
    elif inp.lower() == "print table":
        print_league_table()
    elif inp.lower() == "squad list":
        print("\n  Search for a club's squad list using the club name. Type back to return to main menu.")
        search_string = " "
        while search_string.lower() != "back":
            if search_string.lower() == "clear":
                clear_screen()
            elif search_string.lower() == "":
                print("  Please enter a valid search string.")
            search_string = input("\n  Enter team to search for: ")
            search_club(search_string, clubs)
        clear_screen()
        search_club(search_string, clubs)
    elif inp.lower() == "pick match squad":
        pick_match_squad(clubs[3], match_120816)
    elif inp.lower() == "show match squad":
        show_match_squad(clubs[3], match_120816, '442')
    elif inp.lower() == "fixture search":
        search_fixture(fixtures)
    elif inp.lower() == "exit":
        confirm = input("\n  Are you sure you want to exit? (Y/n)  ")
        if confirm.lower() == 'y' or confirm.lower() == 'yes':
            break
    else:
        print("\n  Could not find <", inp, ">\n  Type help to see available commands.")
