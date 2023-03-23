import pandas as pd
import preprocessor

def runs(deli):
    runsbyeachteam = deli.groupby('BattingTeam')['total_run'].sum().reset_index()
    return runsbyeachteam

def winner(matches):
      winnerofeachseason = matches.drop_duplicates('Season',keep='first')[['Season','WinningTeam']].sort_values('Season').reset_index(drop=True)
      return winnerofeachseason

def orange(deli):
      orangecap = deli.groupby(['Season', 'batter'])['batsman_run'].sum().reset_index().sort_values('batsman_run').drop_duplicates(
          'Season', keep='last').sort_values(by='Season').reset_index(drop=True)
      return orangecap

def purple(deli):
      wickets = deli[deli['player_out'].isna() == False]
      wickets = wickets[(wickets['kind'] != "run out") & (wickets['kind'] != "hit wicket") & (
                  wickets['kind'] != "obstructing the field") & (wickets['kind'] != "retired out") & (
                                    wickets['kind'] != "retired hurt")]
      purplecap = wickets.groupby(['Season', 'bowler'])['player_out'].count().sort_values().reset_index().drop_duplicates('Season',
                                                                                                              keep='last').sort_values(
          'Season').reset_index(drop=True)
      return purplecap

def sixes(deli):
      highestsixes = deli[deli['batsman_run'] == 6].groupby(['Season', 'batter'])['batsman_run'].count().reset_index().sort_values(
          by=['Season', 'batsman_run'], ascending=[True, False]).drop_duplicates('Season', keep='first').reset_index(
          drop=True)
      highestsixes.rename(columns={'batsman_run':'No of Sixes'},inplace=True)
      return highestsixes

def fours(deli):
      highestfours = deli[deli['batsman_run'] == 4].groupby(['Season', 'batter'])['batsman_run'].count().reset_index().sort_values(
          by=['Season', 'batsman_run'], ascending=[True, False]).drop_duplicates('Season', keep='first').reset_index(
          drop=True)
      highestfours.rename(columns={'batsman_run':'No of Fours'},inplace=True)
      return highestfours

def catches(deli):
    highestcatches = deli[deli['kind'] == 'caught'].groupby('fielders_involved')['kind'].count().reset_index().sort_values(by='kind',
                                                                                                          ascending=False).reset_index(
        drop=True).head(10)
    highestcatches.rename(columns={'fielders_involved':'Name','kind':'Catches'})
    return highestcatches


def runout(deli):
    highestrunout = deli[deli['kind'] == 'run out'].groupby('fielders_involved')['kind'].count().reset_index().sort_values(by='kind',
                                                                                                          ascending=False).reset_index(
        drop=True).head(10)
    highestrunout.rename(columns={'fielders_involved': 'Name', 'kind': 'Run Outs'})
    return highestrunout

def death(new_deli):
    runs = new_deli[new_deli['overs'] > 14].groupby('batter')['batsman_run'].sum().reset_index().sort_values(
        by=['batsman_run'], ascending=False).reset_index(drop=True)
    no_of_balls = new_deli[new_deli['overs'] > 14].groupby('batter')['batsman_run'].count().reset_index().rename(
        columns={'batsman_run': "Bowls faced"})
    new_df = runs.merge(no_of_balls, how='left', on='batter').head(10)
    new_df['strike rate'] = (new_df['batsman_run'] / new_df['Bowls faced'])*100
    return new_df

def deathwickets(new_deli):
    temp = new_deli[
        (new_deli['isWicketDelivery'] == 1) & (new_deli['kind'] != 'run out') & (new_deli['kind'] != 'retired hurt') & (
                    new_deli['kind'] != 'obstructing the field')]
    return temp[temp['overs']>14].groupby('bowler')['isWicketDelivery'].count().reset_index().sort_values(by='isWicketDelivery' , ascending=False).reset_index(drop=True).rename(columns={'isWicketDelivery':'No of Wickets'}).head(10)



def teams(matches):
    team = matches['Team1'].unique().tolist()
    team.sort()
    return team

def won(matches,selected_team):
    iplwinners = matches.drop_duplicates(subset='Season', keep='first').sort_values(by='Season', ascending=True)[
        'WinningTeam'].tolist()
    count = 0
    for i in iplwinners:
        if i == selected_team:
            count = count + 1
    return count

def most_runs_team(deli,selected_team):
    team = deli[(deli['BattingTeam'] == selected_team)]
    most_runs = team.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).reset_index()
    return most_runs

def most_wickets_team(deli,selected_team):
    team = deli[(deli['BowlingTeam'] == selected_team)]
    mostwickets = team[(team['kind'] != 'run out') & (team['kind'] != 'retired hurt') & (
                team['kind'] != 'obstructing the field')]
    mostwickets = mostwickets.groupby('bowler')['player_out'].count().sort_values(ascending=False).reset_index()
    return mostwickets
def most_sixes_team(deli,selected_team):
    team = deli[(deli['BattingTeam'] == selected_team)]
    sixes = team[team['batsman_run'] == 6]
    sixes = sixes.groupby('batter')['batsman_run'].count().sort_values(ascending=False).reset_index().head(10)
    sixes.rename(columns={'batsman_run': 'No of Sixes'}, inplace=True)
    return sixes
def most_fours_team(deli,selected_team):
    team = deli[(deli['BattingTeam'] == selected_team)]
    fourss = team[team['batsman_run'] == 4]
    fourss = fourss.groupby('batter')['batsman_run'].count().sort_values(ascending=False).reset_index().head(10)
    fourss.rename(columns={'batsman_run': 'No of Fours'}, inplace=True)
    return fourss

def opponentteam(matches,selected_team):
    opponentteams = matches['Team1'].unique().tolist()
    opponentteams.remove(selected_team)
    opponentteams.sort()
    return opponentteams

def oppo(matches,selected_team,opponent_team):
    matches_won = matches[((matches['Team1'] == selected_team) & (matches['Team2'] == opponent_team) & (
                matches['WinningTeam'] == selected_team)) | ((matches['Team2'] == selected_team) & (
                matches['Team1'] == opponent_team) & (matches['WinningTeam'] == selected_team))]
    matches_played = matches[((matches['Team1'] == selected_team) & (matches['Team2'] == opponent_team)) | (
                (matches['Team2'] == selected_team) & (matches['Team1'] == opponent_team))]
    matches_won = matches_won.shape[0]
    matches_played = matches_played.shape[0]
    return matches_played , matches_won

def top10batsman(deli,selected_team,opponent_team):
    top10batsman = deli[
        (deli['BattingTeam'] == selected_team) & (deli['BowlingTeam'] == opponent_team)]
    top10batsman = top10batsman.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).reset_index()
    return top10batsman

def top10bowlers(deli,selected_team,opponent_team):
    top10bowler = deli[((deli['kind'] != 'run out') & (deli['kind'] != 'retired hurt') & (
                deli['kind'] != 'obstructing the field')) & (
                                   (deli['BattingTeam'] == opponent_team) & (
                                       deli['BowlingTeam'] == selected_team))]
    top10bowler = top10bowler.groupby('bowler')['player_out'].count().sort_values(ascending=False).reset_index()
    return top10bowler

def batsman(deli):
    batsmann = deli['batter'].unique().tolist()
    batsmann.sort()
    return batsmann

def batsmanruns(deli,selected_batsman):
    batsmanrunss = deli[deli['batter']==selected_batsman]['batsman_run'].sum()
    matches_played_batsman = deli[deli['batter'] == selected_batsman]
    matches_played_batsman = matches_played_batsman.drop_duplicates(subset='ID', keep='last').shape[0]
    fours = deli[(deli['batter']==selected_batsman) & (deli['batsman_run']==4)]['batsman_run'].count()
    sixes = deli[(deli['batter']==selected_batsman) & (deli['batsman_run']==6)]['batsman_run'].count()
    ball_played = deli[deli['batter']==selected_batsman].shape[0]
    teams_played = deli[deli['batter']==selected_batsman]
    teams_played = teams_played['BattingTeam'].unique().tolist()
    return batsmanrunss , matches_played_batsman , fours , sixes , ball_played , teams_played

def bowler(deli):
    bowlerr = deli['bowler'].unique().tolist()
    bowlerr.sort()
    return bowlerr


def bowler_wickets(deli,selected_bowler):
    bowler = deli[((deli['kind'] != 'run out') & (deli['kind'] != 'retired hurt') & (
                deli['kind'] != 'obstructing the field') & (deli['bowler'] == selected_bowler))]
    no_wickets = bowler['player_out'].count()
    no_wickets_season = bowler.groupby(['Season'])['player_out'].count().reset_index().sort_values(by='Season', ascending=True)
    matches = bowler.drop_duplicates(subset=['ID'] , keep='first').shape[0]
    no_teams = deli[deli['bowler'] == selected_bowler]['BowlingTeam'].unique().tolist()
    return no_wickets,no_wickets_season,matches

def batsmanvsbowler(deli,selected_batsman , selected_bowler):
    ballsfaced = deli[(deli['bowler'] == selected_bowler) & (deli['batter'] == selected_batsman)]['batsman_run'].count()
    runsscored = deli[(deli['bowler'] == selected_bowler) & (deli['batter'] == selected_batsman)]['batsman_run'].sum()
    strike_rate = (runsscored/ballsfaced)*100
    wicket= deli[(deli['bowler'] == selected_bowler) & (deli['batter'] == selected_batsman)]['player_out'].count()
    six = deli[(deli['bowler'] == selected_bowler) & (deli['batter'] == selected_batsman) & (deli['batsman_run'] == 6)].shape[0]
    four = deli[(deli['bowler'] == selected_bowler) & (deli['batter'] == selected_batsman) & (deli['batsman_run'] == 4)].shape[0]
    return ballsfaced , runsscored , strike_rate , wicket , six , four







