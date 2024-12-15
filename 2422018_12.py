import pandas as pd
items_df = pd.read_csv('items.csv')
target_item = items_df[items_df['item_id'] == 101].iloc[0]
filtered_items = items_df[items_df['item_id'] != 101]
sorted_items = filtered_items.sort_values(
    by=['small_category', 'big_category', 'item_price', 'pages']  # 'page_num'を'pages'に変更
)
recommended_items = sorted_items.head(3)
recommended_item_ids = recommended_items['item_id'].tolist()
print(recommended_item_ids)