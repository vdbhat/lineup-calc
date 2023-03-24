class Player(object):
    # Initialize the 8 main characteristics of a player: Name, Team, Position, Rank on the depth chart, injury status,
    # Weekly team matchup, Score (To be determined by program), and top 10 status within fantasy.
    def __init__(self, name='', team='', position='', depth=0, injury='', matchup='', score=0, top10=''):
        self.name = name
        self.team = team
        self.position = position
        self.depth = depth
        self.injury = injury
        self.matchup = matchup
        self.score = score
        self.top10 = top10

    def __str__(self):
        return str(self.name)


class Team(object):
    # Initialize 3 main characteristics of team: Team name, rank of offense, and rank of defense
    def __init__(self, name, offense, defense):
        self.name = name
        self.offense = offense
        self.defense = defense


import xlrd, xlwt, openpyxl, xlsxwriter
import pandas as pd
from tkinter import *


def read_player_data():
    # Read the NFL Player CSV using Pandas
    # Turn each column into a list, all turned into strings for simplicity
    player_df = pd.read_csv("NFL Player Database.csv")
    names = player_df["Name"].astype(str)
    teams = player_df["Team"].astype(str)
    positions = player_df["Position"].astype(str)
    depths = player_df["Depth"].astype(int)
    injuries = player_df["Injury"].astype(str)
    matchups = player_df["Matchup"].astype(str)
    top10 = player_df["Top 10"].astype(str)

    # Create an object for each player by looping through the list of each player.
    num_players = len(names)
    players = []
    for i in range(num_players):
        name = names[i].upper()
        player_team = teams[i].upper()
        position = positions[i].upper()
        depth = depths[i]
        injury = injuries[i].upper()
        matchup = matchups[i].upper()
        top10status = top10[i].upper()
        player = Player(name, player_team, position, depth, injury, matchup, 0, top10status)
        players.append(player)

    # Take in user input for user's list of players in their roster
    # Since number of players can vary between users, they can assert when they're done entering players
    lineup = []
    root = Tk()
    root.title("Fantasy Football Lineup Calculator")
    header1 = Label(root, text="Enter your roster below, including benched players (First name and last name, "
                               "entries are not case sensitive). Click the 'Enter' button after each "
                               "entry.").grid(row=0, column=0)
    header2 = Label(root, text="For D/ST, Enter as 2 or 3 Letter Team Code (For example, Kansas City is KC, "
                               "and Buffalo is BUF).").grid(row=1, column=0)
    header3 = Label(root, text="Click the 'Done' button when you are finished entering players.").grid(row=2, column=0)
    player_entries = Entry(root, width=50)
    player_entries.grid(row=3, column=0)
    def entry_click():
        roster_entry = player_entries.get()
        lineup.append(roster_entry.upper())
        player_entries.delete(0, len(roster_entry))
    enter_button = Button(root, text="Enter", command=entry_click).grid(row=4, column=0)
    done_button = Button(root, text="Done", command=root.destroy).grid(row=5, column=0)
    root.mainloop()

    # Only look at the player objects for each of the players the user has entered
    chosen_players = []
    for player in players:
        if player.name in lineup:
            chosen_players.append(player)

    return chosen_players


def read_team_data():
    # Same process as reading player data
    team_df = pd.read_csv("NFL Team Database.csv")
    team_codes = team_df["Team"].astype(str)
    offense_score = team_df["Offense"].astype(int)
    defense_score = team_df["Defense"].astype(int)

    team_roster = []
    for i in range(32):
        team_code = team_codes[i].upper()
        team_offense = offense_score[i]
        team_defense = defense_score[i]
        team = Team(team_code, team_offense, team_defense)
        team_roster.append(team)

    return team_roster


def score_players():
    players_roster = read_player_data()
    team_roster = read_team_data()
    # Initialize empty lists for every position to store respective players in
    qbs = []
    rbs = []
    wrs = []
    tes = []
    dsts = []
    ks = []
    flex = []
    # Loop through the list of players user has in their roster
    # For every player: Check if the player is injured, whether they have a top 10 status in fantasy, or if they have
    # a bye that week. Any of these cases force the loop forward to the next iteration.
    for player in players_roster:
        # For QBs: Check their position on the depth chart, and their opposing team matchup for the week.
        # Add to their score if they're 1st on depth, and if the opposing defense is bad or average (0 or 1 on team
        # defense respectively). If the opposing defense is good (2 on team defense), deduct a point.
        if player.position == "QB":
            if player.injury == "YES":
                player.score -= 10
                qbs.append(player)
                continue
            if player.top10 == "YES":
                player.score += 5
                qbs.append(player)
                continue
            if player.matchup == "BYE":
                player.score -= 20
                qbs.append(player)
                continue
            if player.depth == 1:
                player.score += 1
            for team in team_roster:
                if player.matchup == team.name:
                    if team.defense == 0:
                        player.score += 2
                    elif team.defense == 1:
                        player.score += 1
                    else:
                        player.score -= 1
            qbs.append(player)
        # For RBs: Check their position on the depth chart, and their opposing team matchup for the week.
        # Add to their score if they're 1st on depth, and if the opposing defense is bad or average (0 or 1 on team
        # defense respectively). If the opposing defense is good (2 on team defense), deduct a point.
        elif player.position == "RB":
            if player.injury == "YES":
                player.score -= 10
                rbs.append(player)
                flex.append(player)
                continue
            if player.top10 == "YES":
                player.score += 5
                rbs.append(player)
                flex.append(player)
                continue
            if player.matchup == "BYE":
                player.score -= 20
                rbs.append(player)
                continue
            if player.depth == 1:
                player.score += 1
            for team in team_roster:
                if player.matchup == team.name:
                    if team.defense == 0:
                        player.score += 2
                    elif team.defense == 1:
                        player.score += 1
                    else:
                        player.score -= 1
            rbs.append(player)
            flex.append(player)
        # For WRs: Check their position on the depth chart, and their opposing team matchup for the week. Give the
        # player 2 points if they're rank 1, and 1 point if they're rank 2. WRs 1 and 2 are used more than players of
        # depth 2 on other positions.
        # Add to their score if they're 1st on depth, and if the opposing defense is bad or average (0 or 1 on team
        # defense respectively). If the opposing defense is good (2 on team defense), deduct a point.
        elif player.position == "WR":
            if player.injury == "YES":
                player.score -= 10
                wrs.append(player)
                flex.append(player)
                continue
            if player.top10 == "YES":
                player.score += 5
                wrs.append(player)
                flex.append(player)
                continue
            if player.matchup == "BYE":
                player.score -= 20
                wrs.append(player)
                continue
            if player.depth == 1:
                player.score += 2
            elif player.depth == 2:
                player.score += 1
            for team in team_roster:
                if player.matchup == team.name:
                    if team.defense == 0:
                        player.score += 2
                    elif team.defense == 1:
                        player.score += 1
                    else:
                        player.score -= 1
            wrs.append(player)
            flex.append(player)
        # For TEs: Check their position on the depth chart, and their opposing team matchup for the week.
        # Add to their score if they're 1st on depth, and if the opposing defense is bad or average (0 or 1 on team
        # defense respectively). If the opposing defense is good (2 on team defense), deduct a point.
        elif player.position == "TE":
            if player.injury == "YES":
                player.score -= 10
                tes.append(player)
                flex.append(player)
                continue
            if player.top10 == "YES":
                player.score += 5
                tes.append(player)
                flex.append(player)
                continue
            if player.matchup == "BYE":
                player.score -= 20
                tes.append(player)
                continue
            if player.depth == 1:
                player.score += 1
            for team in team_roster:
                if player.matchup == team.name:
                    if team.defense == 0:
                        player.score += 2
                    elif team.defense == 1:
                        player.score += 1
                    else:
                        player.score -= 1
            tes.append(player)
            flex.append(player)
        # For D/STs: Check their position on the depth chart, and their opposing team matchup for the week.
        # Add to their score if the opposing offense is bad or average (0 or 1 on team
        # offense respectively). If the opposing offense is good (2 on team offense), deduct a point. Look at the team's
        # defense as well, and if their defense is good to average (2 or 1), add points. Otherwise, deduct points.
        elif player.position == "D/ST":
            if player.top10 == "YES":
                player.score += 5
                dsts.append(player)
                continue
            for team in team_roster:
                if player.matchup == team.name:
                    if team.offense == 0:
                        player.score += 2
                    elif team.offense == 1:
                        player.score += 1
                    else:
                        player.score -= 1
                if player.name == team.name:
                    if team.defense == 2:
                        player.score += 2
                    elif team.defense == 1:
                        player.score += 1
                    else:
                        player.score -= 1
            dsts.append(player)
        # For Ks: Check their position on the depth chart, and their opposing team matchup for the week.
        # Add to their score if they're 1st on depth, and if the opposing defense is bad or average (0 or 1 on team
        # defense respectively). If the opposing defense is good (2 on team defense), deduct a point.
        elif player.position == "K":
            if player.injury == "YES":
                player.score -= 10
                ks.append(player)
                continue
            if player.top10 == "YES":
                player.score += 5
                ks.append(player)
                continue
            if player.matchup == "BYE":
                player.score -= 20
                ks.append(player)
                continue
            if player.depth == 1:
                player.score += 1
            for team in team_roster:
                if player.matchup == team.name:
                    if team.defense == 0:
                        player.score += 2
                    elif team.defense == 1:
                        player.score += 1
                    else:
                        player.score -= 1
            ks.append(player)

    # Handles errors if user does not enter one of every player in each position
    if len(qbs) == 0 or len(rbs) == 0 or len(wrs) == 0 or len(tes) == 0 or len(dsts) == 0 or len(ks) == 0:
        recommendations = []
        return recommendations

    # Use lambda functions to get the players with the highest scores in each position. This is a list of 6, while the
    # number of players needed is 9. One more RB, WR, and FLEX player are needed.
    recommendations = [(max(qbs, key=lambda p: p.score)), (max(rbs, key=lambda p: p.score)),
                       (max(wrs, key=lambda p: p.score)), (max(tes, key=lambda p: p.score)),
                       (max(dsts, key=lambda p: p.score)), (max(ks, key=lambda p: p.score))]
    # Remove the current RBs, WRs, and TEs in the list from the flex list.
    flex.remove(max(rbs, key=lambda p: p.score))
    flex.remove(max(wrs, key=lambda p: p.score))
    flex.remove(max(tes, key=lambda p: p.score))
    # Remove the RBs and WRs chosen from their own lists
    rbs.remove(max(rbs, key=lambda p: p.score))
    wrs.remove(max(wrs, key=lambda p: p.score))
    # Take the next WR and RB with the highest scores and add to the list of recommendations
    recommendations.append((max(rbs, key=lambda p: p.score)))
    recommendations.append((max(wrs, key=lambda p: p.score)))
    # Remove these added players from flex
    flex.remove(max(rbs, key=lambda p: p.score))
    flex.remove(max(wrs, key=lambda p: p.score))
    # Add the highest scored player from the flex list to the list of recommendations
    recommendations.append((max(flex, key=lambda p: p.score)))

    return recommendations


def recommend():
    recommendations = score_players()

    # Handles error if player does not enter enough players for each position. Stops the program here
    if len(recommendations) == 0:
        root2 = Tk()
        root2.title("Fantasy Football Lineup Calculator")
        error_message = Label(root2, text="You don't have enough players to recommend a lineup!").grid(row=0, column=0)
        quit_button = Button(root2, text="Quit", command=root2.destroy).grid(row=1, column=0)
        root2.mainloop()
        return

    # Checks scores for each player in the list of recommendations. Checks if they're projected to be low scoring,
    # injured, or if they have a bye week.
    for i in range(len(recommendations)):
        if recommendations[i].score == -1:
            recommendations[i].name = recommendations[i].name + " (This player is not projected to do very well this " \
                                                                "week. Switch for a different player or look at " \
                                                                "waivers for a substitute.)"
        elif recommendations[i].score == -10:
            recommendations[i].name = recommendations[i].name + " (This player is injured! Switch for a different " \
                                                                "player or look at waivers for a substitute.)"
        elif recommendations[i].score == -20:
            recommendations[i].name = recommendations[i].name + " (This player has a bye. Switch for a different " \
                                                                "player or look at waivers for a substitute.)"

    root3 = Tk()
    root3.title("Fantasy Football Lineup Calculator")
    header = Label(root3, text="Recommended Lineup:").grid(row=0, column=0)
    qb_rec = Label(root3, text="  QB: " + str(recommendations[0])).grid(row=1, column=0)
    rb1_rec = Label(root3, text="  RB1: " + str(recommendations[1])).grid(row=2, column=0)
    rb2_rec = Label(root3, text="  RB2: " + str(recommendations[6])).grid(row=3, column=0)
    wr1_rec = Label(root3, text="  WR1: " + str(recommendations[2])).grid(row=4, column=0)
    wr2_rec = Label(root3, text="  WR2: " + str(recommendations[7])).grid(row=5, column=0)
    te_rec = Label(root3, text="  TE: " + str(recommendations[3])).grid(row=6, column=0)
    flex_rec = Label(root3, text="  FLEX: " + str(recommendations[8])).grid(row=7, column=0)
    dst_rec = Label(root3, text="  D/ST: " + str(recommendations[4])).grid(row=8, column=0)
    k_rec = Label(root3, text="  K: " + str(recommendations[5])).grid(row=9, column=0)
    quit_button = Button(root3, text="Quit", command=root3.destroy).grid(row=10, column=0)
    root3.mainloop()
    return


def main():
    recommend()


if __name__ == "__main__":
    main()