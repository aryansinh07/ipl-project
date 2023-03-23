import pandas as pd

def preprocess_matches(matches,deli):
    delin = deli[deli['innings'] == 1]
    first_inning_score = delin.groupby('ID')['total_run'].sum().reset_index().rename(
        columns={'total_run': 'first_inning_score'})
    matches = pd.merge(matches, first_inning_score, on='ID', how='left')
    delin = deli[deli['innings'] == 2]
    second_inning_score = delin.groupby('ID')['total_run'].sum().reset_index().rename(
        columns={'total_run': 'second_inning_score'})
    matches = pd.merge(matches, second_inning_score, on='ID', how='left')
    matches['Season'].replace(to_replace='2007/08', value='2008', inplace=True)
    matches['Season'].replace(to_replace='2009/10', value='2010', inplace=True)
    matches['Season'].replace(to_replace='2020/21', value='2020', inplace=True)
    matches['Season'] = matches['Season'].astype(dtype='int32')
    matches['Team1'] = matches['Team1'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    matches['Team2'] = matches['Team2'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    matches['WinningTeam'] = matches['WinningTeam'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    matches['TossWinner'] = matches['TossWinner'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    matches['Team1'] = matches['Team1'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    matches['Team2'] = matches['Team2'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    matches['WinningTeam'] = matches['WinningTeam'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    matches['TossWinner'] = matches['TossWinner'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    matches['Team1'] = matches['Team1'].replace(to_replace='Rising Pune Supergiants', value='Rising Pune Supergiant')
    matches['Team2'] = matches['Team2'].replace(to_replace='Rising Pune Supergiants', value='Rising Pune Supergiant')
    matches['WinningTeam'] = matches['WinningTeam'].replace(to_replace='Rising Pune Supergiants',
                                                            value='Rising Pune Supergiant')
    matches['TossWinner'] = matches['TossWinner'].replace(to_replace='Rising Pune Supergiants',
                                                          value='Rising Pune Supergiant')
    matches['Team1'] = matches['Team1'].replace(to_replace='Kings XI Punjab', value='Punjab Kings')
    matches['Team2'] = matches['Team2'].replace(to_replace='Kings XI Punjab', value='Punjab Kings')
    matches['WinningTeam'] = matches['WinningTeam'].replace(to_replace='Kings XI Punjab', value='Punjab Kings')
    matches['TossWinner'] = matches['TossWinner'].replace(to_replace='Kings XI Punjab', value='Punjab Kings')
    return matches

def preprocess_delivery(matches, deli):
    deli = deli.merge(matches, on='ID', how='left')
    def bowlingTeam(deli, BowlingTeam):
        for i in range(len(deli)):
            if deli['BattingTeam'][i] == deli['Team1'][i]:
                BowlingTeam.append(deli['Team2'][i])
            else:
                BowlingTeam.append(deli['Team1'][i])

    BowlingTeam = []
    bowlingTeam(deli, BowlingTeam)
    deli['BowlingTeam'] = BowlingTeam
    deli['BattingTeam'] = deli['BattingTeam'].replace(to_replace='Delhi Daredevils', value='Delhi Capitals')
    deli['BattingTeam'] = deli['BattingTeam'].replace(to_replace='Deccan Chargers', value='Sunrisers Hyderabad')
    deli['BattingTeam'] = deli['BattingTeam'].replace(to_replace='Rising Pune Supergiants',
                                                      value='Rising Pune Supergiant')
    deli['BattingTeam'] = deli['BattingTeam'].replace(to_replace='Kings XI Punjab', value='Punjab Kings')
    deli.drop(columns=['Team1Players', 'Team2Players', 'Umpire1', 'Umpire2'], inplace=True)
    return deli
