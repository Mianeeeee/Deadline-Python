import pandas as pd # Histogram plots for 3 offensive indicators and 3 defensive indicators
import matplotlib.pyplot as plt

input_file = 'SourceCode/problem-1/results.csv'
output_file = 'SourceCode/problem-2/histogram_premier_league.png'

df = pd.read_csv(input_file)

cols = ['Gls_st', 'Ast_st', 'xG_st', 'Tkl_def', 'Int_def', 'Blocks_def']
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

fig, axes = plt.subplots(2, 3, figsize=(15, 7))
fig.suptitle('Histograms of Atk and Def metrics in Premier League', fontsize=20)
axes = axes.flatten()

colors = ['lightblue', 'lightpink', 'lightgreen', 'lavender', 'peachpuff', 'wheat']
column_names = {
    'Gls_st': 'Goals',
    'Ast_st': 'Assists',
    'xG_st': 'Expected Goals',
    'Tkl_def': 'Tackles',
    'Int_def': 'Interceptions',
    'Blocks_def': 'Blocks'
}

for i, col in enumerate(cols):
    max_value = int(df[col].max())
    axes[i].hist(df[col], bins=max_value, color=colors[i], edgecolor='black')

    axes[i].set_title(column_names[col])
    axes[i].set_xlabel('Index')
    axes[i].set_ylabel('Number of Players')
    axes[i].set_facecolor('whitesmoke')
    axes[i].grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.subplots_adjust(wspace=0.3, hspace=0.4, top=0.85)
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()