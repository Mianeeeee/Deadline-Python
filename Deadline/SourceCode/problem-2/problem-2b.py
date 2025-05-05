import pandas as pd # Find the median, mean, and standard deviation for each team

input_file = 'SourceCode/problem-1/results.csv'
output_file = 'SourceCode/problem-2/results.csv'

df = pd.read_csv(input_file, encoding='utf-8')
df.drop(columns=['Player', 'Nation', 'Age', 'Pos'], inplace= True)
df = df.replace('N/a', 0.0)
for col in df.columns:
    if col != 'Team':
        df[col] = pd.to_numeric(df[col], errors='coerce')
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
table_cols = ['Team']

for h in numeric_columns:
    c = str(h)
    table_cols.append('Mean of ' + c)
    table_cols.append('Median of ' + c)
    table_cols.append('Std of ' + c)

teams = sorted(list(set(df['Team'])))

table_data = []

for team in teams:
    team_data = df[df['Team'] == team]
    row = [team]
    for col in numeric_columns:
        row.append(team_data[col].mean())
        row.append(team_data[col].median())
        row.append(team_data[col].std())
    table_data.append(row)

df = pd.DataFrame(table_data, columns=table_cols)
df.to_csv(output_file, index=False)
print('Successful save to csv!')