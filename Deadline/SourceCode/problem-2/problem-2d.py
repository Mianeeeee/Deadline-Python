import pandas as pd # Determine the team with the highest score for each statistic, analyze which team has the best record during the season 

input_file = 'SourceCode/problem-2/results.csv'
output_file = 'SourceCode/problem-2/Team_stat_leaders_and_record.txt'

def save_file(df):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(df[['Team', 'Atk', 'Def', 'Pos', 'Total']].round(2).to_string(index=False, col_space=12))

df = pd.read_csv(input_file)

metrics = {
    'Atk': ['Mean of Gls_st', 'Mean of Ast_st', 'Mean of xG_st'],
    'Def': ['Mean of Tkl_def', 'Mean of Int_def', 'Mean of Blocks_def'],
    'Pos': ['Mean of Cmp_pas', 'Mean of PrgP_pas', 'Mean of Touches_pos']
}

def normalize(res):
    return (res - res.min()) / (res.max() - res.min())

scores = {}
for category, cols in metrics.items():
    normalized_data = df[cols].apply(normalize)
    scores[category] = normalized_data.mean(axis=1) * 100

score_df = pd.DataFrame(scores)
score_df['Team'] = df['Team']
score_df['Total'] = (score_df['Atk'] * 0.4 + score_df['Def'] * 0.3 + score_df['Pos'] * 0.3)
score_df = score_df.sort_values(by='Total', ascending=False)
save_file(score_df)
print("Team rankings based on aggregate points:")
print(score_df[['Team', 'Atk', 'Def', 'Pos', 'Total']].round(2).to_string(index=False, col_space=12))

top_team = score_df.iloc[0]['Team']
top_score = score_df.iloc[0]['Total']
print(f"\nTeam with the best record: **{top_team}** (with {top_score:.2f} aggregate points)")