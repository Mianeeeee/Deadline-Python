import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time
import random

output_file = 'SourceCode/problem-1/results.csv'

https = 'https://fbref.com'
url = https + '/en/'

def format_nation(nation):
    if pd.isna(nation):
        return nation
    return nation[-3:].upper()

def main() -> None:
    session = requests.Session()
    response = session.get(url, timeout=15)
    time.sleep(random.uniform(5, 10))
    response.raise_for_status()

    soup = bs(response.text, 'html.parser')
    link_premier_league = soup.find('a', href=True, string='Premier League')
    if link_premier_league: url_premier_league = https + link_premier_league.get('href')
    else:
        print('Premier League link not found')
        return

    response_premier_league = session.get(url_premier_league, timeout=15)
    time.sleep(random.uniform(5, 10))
    response_premier_league.raise_for_status()

    soup_premier_league = bs(response_premier_league.text, 'html.parser')
    res = soup_premier_league.find('table')
    if res: team_premier_league = res.find_all('td', {'data-stat': 'team'})
    else:
        print('Team table not found')
        return

    all_teams = []
    for team in team_premier_league:
        link_team = team.find('a', href=True)
        if link_team:
            club = link_team.text
            url_team = https + link_team.get('href')
        else:
            print(f'Team link not found for a team')
            continue

        response_team = session.get(url_team, timeout=15)
        print(f"Status code for {club}: {response_team.status_code}")
        time.sleep(random.uniform(5, 10))
        response_team.raise_for_status()
        print(f'Retrieving data from club {club}' , end=' | ')

        tables = pd.read_html(response_team.text)

        # # Standard Stats
        standard_stats = tables[0]
        standard_stats.columns = pd.MultiIndex.from_tuples([
            ('Unname' if 'Unnamed' in col[0] else col[0], col[1]) 
            for col in standard_stats.columns
        ])
        standard_stats = standard_stats[standard_stats[('Playing Time', 'Min')] > 90].copy()
        players = pd.DataFrame()
        players['Player'] = standard_stats[('Unname', 'Player')].copy()
        players['Nation'] = standard_stats[('Unname', 'Nation')].apply(format_nation)
        players['Team'] = club
        players = players[~players['Player'].str.contains('Total', na=False)]
        players[['Pos', 'Age']] = standard_stats[[('Unname', 'Pos'), ('Unname', 'Age')]].copy()
        if ('Unname', 'MP') in standard_stats.columns:
            players['MP'] = standard_stats[('Unname', 'MP')].copy()
        else: players['MP'] = standard_stats[('Playing Time', 'MP')].copy()
        players[['Starts', 'Min']] = standard_stats[[('Playing Time', 'Starts'), ('Playing Time', 'Min')]].copy()
        players[['Gls_st', 'Ast_st', 'CrdY_st', 'CrdR_st']] = standard_stats[[
            ('Performance', 'Gls'), ('Performance', 'Ast'), ('Performance', 'CrdY'), ('Performance', 'CrdR')
        ]].copy()
        players[['xG_st', 'xAG_st']] = standard_stats[[('Expected', 'xG'), ('Expected', 'xAG')]].copy()
        players[['PrgC_st', 'PrgP_st', 'PrgR_st']] = standard_stats[[
            ('Progression', 'PrgC'), ('Progression', 'PrgP'), ('Progression', 'PrgR')
        ]].copy()
        players[['Gls_st_per90', 'Ast_st_per90', 'xG_st_per90', 'xAG_st_per90']] = standard_stats[[
            ('Per 90 Minutes', 'Gls'), ('Per 90 Minutes', 'Ast'), ('Per 90 Minutes', 'xG'), ('Per 90 Minutes', 'xAG')
        ]].copy()

        # # Goalkeeping
        goalkeeping_stats = tables[2]
        gk = pd.DataFrame()
        gk['Player'] = goalkeeping_stats[('Unnamed: 0_level_0', 'Player')].copy()
        gk[['GA90_gk', 'Save%_gk', 'CS%_gk']] = goalkeeping_stats[[
            ('Performance', 'GA90'), ('Performance', 'Save%'), ('Performance', 'CS%')
        ]].copy()
        gk['Save%_gk_pen'] = goalkeeping_stats[('Penalty Kicks', 'Save%')].copy()
        players = pd.merge(players, gk, on='Player', how='left')

        # # Shooting
        shooting_stats = tables[4]
        sh = pd.DataFrame()
        sh['Player'] = shooting_stats[('Unnamed: 0_level_0', 'Player')].copy()
        sh[['SoT%_sh', 'SoT/90_sh', 'G/Sh_sh', 'Dist_sh']] = shooting_stats[[
            ('Standard', 'SoT%'), ('Standard', 'SoT/90'), ('Standard', 'G/Sh'), ('Standard', 'Dist')
        ]].copy()
        players = pd.merge(players, sh, on='Player', how='left')

        # # Passing
        passing_stats = tables[5]
        passing_stats.columns = pd.MultiIndex.from_tuples([
            ('Unname' if 'Unnamed' in col[0] else col[0], col[1]) 
            for col in passing_stats.columns
        ])
        pas = pd.DataFrame()
        pas['Player'] = passing_stats[('Unname', 'Player')].copy()
        pas[['Cmp_pas', 'Cmp%_pas']] = passing_stats[[('Total', 'Cmp'), ('Total', 'Cmp%')]].copy()
        pas['Cmp%_pas_S'] = passing_stats[('Short', 'Cmp%')].copy()
        pas['Cmp%_pas_M'] = passing_stats[('Medium', 'Cmp%')].copy()
        pas['Cmp%_pas_L'] = passing_stats[('Long', 'Cmp%')].copy()
        pas[['KP_pas', '1/3_pas', 'PPA_pas', 'CrsPA_pas', 'PrgP_pas']] = passing_stats[[
            ('Unname', 'KP'), ('Unname', '1/3'), ('Unname', 'PPA'), ('Unname', 'CrsPA'), ('Unname', 'PrgP')
        ]].copy()
        players = pd.merge(players, pas, on='Player', how='left')

        # Goal and Shot Creation
        goal_and_shot_creation_stats = tables[7]
        gsc = pd.DataFrame()
        gsc['Player'] = goal_and_shot_creation_stats[('Unnamed: 0_level_0', 'Player')].copy()
        gsc[['SCA_gsc', 'SCA90_gsc']] = goal_and_shot_creation_stats[[('SCA', 'SCA'), ('SCA', 'SCA90')]].copy()
        gsc[['GCA_gsc', 'GCA90_gsc']] = goal_and_shot_creation_stats[[('GCA', 'GCA'), ('GCA', 'GCA90')]].copy()
        players = pd.merge(players, gsc, on='Player', how='left')

        # Defensive Actions
        defensive_actions_stats = tables[8]
        de = pd.DataFrame()
        de['Player'] = defensive_actions_stats[('Unnamed: 0_level_0', 'Player')].copy()
        de[['Tkl_def', 'TklW_def']] = defensive_actions_stats[[('Tackles', 'Tkl'), ('Tackles', 'TklW')]].copy()
        de[['Att_def', 'Lost_def']] = defensive_actions_stats[[('Challenges', 'Att'), ('Challenges', 'Lost')]].copy()
        de[['Blocks_def', 'Sh_def', 'Pass_def']] = defensive_actions_stats[[('Blocks', 'Blocks'), ('Blocks', 'Sh'), ('Blocks', 'Pass')]].copy()
        de['Int_def'] = defensive_actions_stats[('Unnamed: 17_level_0', 'Int')].copy()
        players = pd.merge(players, de, on='Player', how='left')

        # Possession
        possession_stats = tables[9]
        pos = pd.DataFrame()
        pos['Player'] = possession_stats[('Unnamed: 0_level_0', 'Player')].copy()
        pos[['Touches_pos', 'Def Pen_pos', 'Def 3rd_pos', 'Mid 3rd_pos', 'Att 3rd_pos', 'Att Pen']] = possession_stats[[
            ('Touches', 'Touches'), ('Touches', 'Def Pen'), ('Touches', 'Def 3rd'), ('Touches', 'Mid 3rd'), ('Touches', 'Att 3rd'), ('Touches', 'Att Pen')
        ]].copy()
        pos[['Att_pos', 'Succ%_pos', 'Tkld%_pos']] = possession_stats[[('Take-Ons', 'Att'), ('Take-Ons', 'Succ%'), ('Take-Ons', 'Tkld%')]].copy()
        pos[['Carries_pos', 'PrgDist_pos', 'PrgC_pos', '1/3_pos', 'CPA_pos', 'Mis_pos', 'Dis_pos']] = possession_stats[[
            ('Carries', 'Carries'), ('Carries', 'PrgDist'), ('Carries', 'PrgC'), ('Carries', '1/3'), ('Carries', 'CPA'), ('Carries', 'Mis'), ('Carries', 'Dis')
        ]].copy()
        pos[['Rec_pos', 'PrgR_pos']] = possession_stats[[('Receiving', 'Rec'), ('Receiving', 'PrgR')]].copy()
        players = pd.merge(players, pos, on='Player', how='left')

        # Miscellaneous
        miscellaneous_stats = tables[11]
        mis = pd.DataFrame()
        mis['Player'] = miscellaneous_stats[('Unnamed: 0_level_0', 'Player')].copy()
        mis[['Fls_mis', 'Fld_mis', 'Off_mis', 'Crs_mis', 'Recov_mis']] = miscellaneous_stats[[
            ('Performance', 'Fls'), ('Performance', 'Fld'), ('Performance', 'Off'), ('Performance', 'Crs'), ('Performance', 'Recov')
        ]].copy()
        mis[['Won_mis', 'Lost_mis', 'Won%_mis']] = miscellaneous_stats[[('Aerial Duels', 'Won'), ('Aerial Duels', 'Lost'), ('Aerial Duels', 'Won%')]].copy()
        players = pd.merge(players, mis, on='Player', how='left')

        all_teams.append(players)
        print('Complete data retrieval!')

    ans = pd.concat(all_teams)
    ans.fillna('N/a', inplace=True)
    ans = ans.sort_values('Player')
    ans.to_csv(output_file, index=False)
    print('Successful save to csv!')

if __name__ == '__main__':
    main()