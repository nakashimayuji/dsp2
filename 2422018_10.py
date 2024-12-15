import pandas as pd
items_df = pd.read_csv('items.csv')
orders_df = pd.read_csv('orders.csv')
merged_df = pd.merge(orders_df, items_df, on='item_id')
merged_df['purchase_amount'] = merged_df['order_num'] * merged_df['item_price']
max_purchase = merged_df.loc[merged_df['purchase_amount'].idxmax()]
print([max_purchase['order_id'], max_purchase['purchase_amount']])