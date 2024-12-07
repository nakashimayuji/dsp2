import pandas as pd
df = pd.read_csv('winequality-red.csv')
gentei = df.iloc[4:10]
print(gentei)