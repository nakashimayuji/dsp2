import pandas as pd
# CSV読み込み
users = pd.read_csv('users.csv')
orders = pd.read_csv('orders.csv')
items = pd.read_csv('items.csv')
# 商品価格を取得
merged = pd.merge(orders, items, on='item_id')
# 各注文の購入金額を計算
merged['amount'] = merged['order_num'] * merged['item_price']
# 各ユーザの平均購入金額を計算
avg_amount = merged.groupby('user_id')['amount'].mean()
# 最も高い平均購入金額を持つユーザを見つける
max_user = avg_amount.idxmax()
max_avg = avg_amount.max()
# 結果を出力
print([max_user, max_avg])