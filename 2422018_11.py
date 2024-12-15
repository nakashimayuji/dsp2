import pandas as pd
users_df = pd.read_csv('users.csv')
orders_df = pd.read_csv('orders.csv')
items_df = pd.read_csv('items.csv')
merged_df = pd.merge(orders_df, items_df, on='item_id')
merged_df['purchase_amount'] = merged_df['order_num'] * merged_df['item_price']
user_avg_purchase = merged_df.groupby('user_id')['purchase_amount'].mean()
max_avg_purchase_user = user_avg_purchase.idxmax()
max_avg_purchase_amount = user_avg_purchase.max()
print([max_avg_purchase_user, max_avg_purchase_amount])