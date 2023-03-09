# This program updates the matchups for every player in the CSV, since updating every player matchup manually within
# spreadsheet is extremely inefficient. The program takes in user input to update each of the 32 team matchups.

import xlrd, xlwt, openpyxl, xlsxwriter
import pandas as pd

def update_matchups():
    player_df = pd.read_csv("NFL Player Database.csv")
    playing_teams = player_df["Team"].astype(str)
    teams = ['DAL', 'PHI', 'WAS', 'NYG', 'MIN', 'DET', 'GB', 'CHI', 'TB', 'CAR', 'NO', 'ATL', 'SF', 'SEA', 'ARI',
             'LAR', 'BUF', 'NE', 'MIA', 'NYJ', 'CIN', 'BAL', 'PIT', 'CLE', 'JAX', 'IND', 'TEN', 'HOU', 'KC', 'LAC',
             'LV', 'DEN']
    matchups = {}
    for cur_team in teams:
        matchup = input("Which team is " + cur_team + " playing this week?").upper()
        matchups[cur_team] = matchup


    num_players = len(playing_teams)
    for i in range(num_players):
        team = playing_teams[i].upper()
        if team == "DAL":
            player_df.loc[i, 'Matchup'] = matchups['DAL']
        elif team == "PHI":
            player_df.loc[i, 'Matchup'] = matchups['PHI']
        elif team == "WAS":
            player_df.loc[i, 'Matchup'] = matchups['WAS']
        elif team == "NYG":
            player_df.loc[i, 'Matchup'] = matchups['NYG']
        elif team == "MIN":
            player_df.loc[i, 'Matchup'] = matchups['MIN']
        elif team == "DET":
            player_df.loc[i, 'Matchup'] = matchups['DET']
        elif team == "GB":
            player_df.loc[i, 'Matchup'] = matchups['GB']
        elif team == "CHI":
            player_df.loc[i, 'Matchup'] = matchups['CHI']
        elif team == "TB":
            player_df.loc[i, 'Matchup'] = matchups['TB']
        elif team == "CAR":
            player_df.loc[i, 'Matchup'] = matchups['CAR']
        elif team == "NO":
            player_df.loc[i, 'Matchup'] = matchups['NO']
        elif team == "ATL":
            player_df.loc[i, 'Matchup'] = matchups['ATL']
        elif team == "SF":
            player_df.loc[i, 'Matchup'] = matchups['SF']
        elif team == "SEA":
            player_df.loc[i, 'Matchup'] = matchups['SEA']
        elif team == "LAR":
            player_df.loc[i, 'Matchup'] = matchups['LAR']
        elif team == "ARI":
            player_df.loc[i, 'Matchup'] = matchups['ARI']
        elif team == "BUF":
            player_df.loc[i, 'Matchup'] = matchups['BUF']
        elif team == "MIA":
            player_df.loc[i, 'Matchup'] = matchups['MIA']
        elif team == "NE":
            player_df.loc[i, 'Matchup'] = matchups['NE']
        elif team == "NYJ":
            player_df.loc[i, 'Matchup'] = matchups['NYJ']
        elif team == "CIN":
            player_df.loc[i, 'Matchup'] = matchups['CIN']
        elif team == "BAL":
            player_df.loc[i, 'Matchup'] = matchups['BAL']
        elif team == "PIT":
            player_df.loc[i, 'Matchup'] = matchups['PIT']
        elif team == "CLE":
            player_df.loc[i, 'Matchup'] = matchups['CLE']
        elif team == "JAX":
            player_df.loc[i, 'Matchup'] = matchups['JAX']
        elif team == "TEN":
            player_df.loc[i, 'Matchup'] = matchups['TEN']
        elif team == "IND":
            player_df.loc[i, 'Matchup'] = matchups['IND']
        elif team == "HOU":
            player_df.loc[i, 'Matchup'] = matchups['HOU']
        elif team == "KC":
            player_df.loc[i, 'Matchup'] = matchups['KC']
        elif team == "LAC":
            player_df.loc[i, 'Matchup'] = matchups['LAC']
        elif team == "LV":
            player_df.loc[i, 'Matchup'] = matchups['LV']
        elif team == "DEN":
            player_df.loc[i, 'Matchup'] = matchups['DEN']

    player_df.to_csv("NFL Player Database.csv", index=False)

def main():
    update_matchups()

if __name__ == "__main__":
    main()