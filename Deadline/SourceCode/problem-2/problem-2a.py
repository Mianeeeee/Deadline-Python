import pandas as pd # The 3 players with the highest score and the 3 players with the lowest score for each statistic

input_file = 'SourceCode/problem-1/results.csv'
output_file = 'SourceCode/problem-2/Top_and_Bottom_3_statistics.txt'

df = pd.read_csv(input_file, encoding='utf-8')
non_numeric_columns = ['Player', 'Nation', 'Team', 'Pos']
df = df.replace('N/a', 0.0)
for col in df.columns:
    if col not in non_numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
result = []

for col in numeric_columns:
    sorted_df = df.sort_values(by= col, ascending=True)
    
    smallest = sorted_df[[*df.columns]].head(3)
    largest = sorted_df[[*df.columns]].tail(3)
    combined = pd.concat([smallest, largest])

    result.append(f'Column: {col}')
    result.append(combined)
    result.append('')

with open(output_file, 'w', encoding='utf-8') as f:
    for x in result:
        if isinstance(x, pd.DataFrame):
            f.write(x.to_string(index=False))
            f.write('\n')
        else: f.write(str(x) + '\n')

print('Successful save to txt!')