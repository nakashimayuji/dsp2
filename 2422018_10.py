import pandas as pd
# items.cav読み込み
items = pd.read_csv('items.csv')
# ordera.csv読み込み
orders = pd.read_csv('orders.csv')
merged = pd.merge(orders, items, on='item_id')
# 各注文の購入金額を計算
merged['amount'] = merged['order_num'] * merged['item_price']
# 最も高い購入金額を
max_order = merged.loc[merged['amount'].idxmax()]
# 結果を出力
print([max_order['order_id'], max_order['amount']])