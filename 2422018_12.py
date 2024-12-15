import pandas as pd
# item.csv読み込み
items = pd.read_csv('items.csv')
# item_idが101の商品情報を取得
target = items[items['item_id'] == 101].iloc[0]
filtered = items[items['item_id'] != 101]
sorted_items = filtered.sort_values(
    by=['small_category', 'big_category', 'item_price', 'pages']
)
# 上位3件を取得
top3 = sorted_items.head(3)
# 推薦候補のitem_id
recommendations = top3['item_id'].tolist()
# 推薦候補のitem_idを出力
print(recommendations)