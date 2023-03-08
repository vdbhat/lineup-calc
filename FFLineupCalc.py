class Player(object):
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
    def __init__(self, name, offense, defense):
        self.name = name
        self.offense = offense
        self.defense = defense


import xlrd, xlwt, openpyxl, xlsxwriter
import pandas as pd


def read_player_data():
    player_df = pd.read_csv("NFL Player Database.csv")
    names = player_df["Name"].astype(str)
    teams = player_df["Team"].astype(str)
    positions = player_df["Position"].astype(str)
    depths = player_df["Depth"].astype(int)
    injuries = player_df["Injury"].astype(str)
    matchups = player_df["Matchup"].astype(str)
    top10 = player_df["Top 10"].astype(str)

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

    lineup = []
    print("Enter your roster below, including benched players (First name and last name, "
          "entries are not case sensitive).")
    print("For D/ST, Enter as 2 or 3 Letter Team Code (For example, Kansas City is KC, and Buffalo is BUF).")
    print("Type 'done' when you are finished entering players.")
    print()
    roster = input("Player: ").upper()
    lineup.append(roster)
    while roster != "DONE":
        roster = input("Player: ").upper()
        lineup.append(roster)
    print()

    chosen_players = []
    for player in players:
        if player.name in lineup:
            chosen_players.append(player)

    return chosen_players


def read_team_data():
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
    # For QB: Only thing that matters is depth and matchup, also take into account if they are top 10
    # For RB: Depth, matchup, top 10
    # For WR: Depth (1 and 2), matchup, top 10
    # For TE: Depth, matchup, top 10
    # For D/ST: QB Rank, offense rank
    # For K: Depth, matchup, top 10
    players_roster = read_player_data()
    team_roster = read_team_data()
    qbs = []
    rbs = []
    wrs = []
    tes = []
    dsts = []
    ks = []
    flex = []
    for player in players_roster:
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

    if len(qbs) == 0 or len(rbs) == 0 or len(wrs) == 0 or len(tes) == 0 or len(dsts) == 0 or len(ks) == 0:
        recommendations = []
        return recommendations

    recommendations = [(max(qbs, key=lambda p: p.score)), (max(rbs, key=lambda p: p.score)),
                       (max(wrs, key=lambda p: p.score)), (max(tes, key=lambda p: p.score)),
                       (max(dsts, key=lambda p: p.score)), (max(ks, key=lambda p: p.score))]
    flex.remove(max(rbs, key=lambda p: p.score))
    flex.remove(max(wrs, key=lambda p: p.score))
    flex.remove(max(tes, key=lambda p: p.score))
    rbs.remove(max(rbs, key=lambda p: p.score))
    wrs.remove(max(wrs, key=lambda p: p.score))
    recommendations.append((max(rbs, key=lambda p: p.score)))
    recommendations.append((max(wrs, key=lambda p: p.score)))
    flex.remove(max(rbs, key=lambda p: p.score))
    flex.remove(max(wrs, key=lambda p: p.score))
    recommendations.append((max(flex, key=lambda p: p.score)))

    return recommendations


def recommend():
    recommendations = score_players()

    if len(recommendations) == 0:
        print("You don't have enough players to recommend a lineup!")
        return

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

    print("Recommended Lineup:")
    print("  QB:", recommendations[0])
    print("  RB1:", recommendations[1])
    print("  RB2:", recommendations[6])
    print("  WR1:", recommendations[2])
    print("  WR2:", recommendations[7])
    print("  TE:", recommendations[3])
    print("  FLEX:", recommendations[8])
    print("  D/ST:", recommendations[4])
    print("  K:", recommendations[5])


def main():
    recommend()


if __name__ == "__main__":
    main()