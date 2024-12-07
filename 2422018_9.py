import pandas as pd
df = pd.read_csv('winequality-red.csv')
heikinn = df.groupby('quality').mean()
print(heikinn)