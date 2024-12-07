import pandas as pd
df = pd.read_csv('winequality-red.csv')
ijyou = df[df['quality'] >= 6]
narabi = ijyou.sort_values(by='quality',  ascending=False)
print(narabi)