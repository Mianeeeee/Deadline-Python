import pandas as pd # Build a players pricing model
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

input_file1 = 'SourceCode/problem-1/results.csv'
input_file2 = 'SourceCode/problem-4/results.csv'
output_file = 'SourceCode/problem-4/predicted_vs_actual.csv'

df1 = pd.read_csv(input_file1)
df2 = pd.read_csv(input_file2)[['Player', 'Skill / Pot', 'ETV']]
df = pd.merge(df1, df2, on='Player')

# Data cleaning
df['ETV'] = df['ETV'].str.extract(r'([\d.]+)').astype(float)
df['Age'] = df['Age'].str.extract(r'(\d+)-(\d+)').astype(int).apply(lambda x: x[0] + x[1]/365, axis=1)
df[['Skill', 'Pot']] = df['Skill / Pot'].str.extract(r'([\d.]+)\s*/\s*([\d.]+)').astype(float)
df = pd.concat([df, df['Pos'].str.get_dummies(sep=',')], axis=1)

# Select numeric features
x = df[['Age', 'Min', 'Skill', 'Pot'] + list(df['Pos'].str.get_dummies(sep=',').columns)]
y = np.log1p(df['ETV'])

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model = LinearRegression().fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\nRMSE: {rmse:.4f}")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}\n")

# Predicted vs Actual Results Table
results_df = pd.DataFrame({
    "Actual ETV (€)": np.expm1(y_test),
    "Predicted ETV (€)": np.expm1(y_pred)
})
results_df.to_csv(output_file, index=False)
print('Successful save to csv!')