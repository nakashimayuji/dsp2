import sqlite3
import requests
import flet as ft

# データベースの初期化
def init_db():
    con = sqlite3.connect('天気.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Areas (
            id INTEGER PRIMARY KEY,
            name TEXT,
            en_name TEXT,
            office_name TEXT
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Forecasts (
            id INTEGER PRIMARY KEY,
            area_id INTEGER,
            forecast_date TEXT,
            weather TEXT,
            FOREIGN KEY(area_id) REFERENCES Areas(id)
        );
    ''')
    con.close()

# 地域情報をデータベースに保存
def save_area_data(area_data):
    con = sqlite3.connect('天気.db')
    cur = con.cursor()
    sql_insert_area = '''
    INSERT OR REPLACE INTO Areas (id, name, en_name, office_name)
    VALUES (?, ?, ?, ?);
    '''
    for center_code, center_info in area_data['centers'].items():
        cur.execute(sql_insert_area, (center_code, center_info['name'], center_info['enName'], center_info['officeName']))
    con.commit()
    con.close()

# 天気予報情報をデータベースに保存
def save_forecast_data(forecast_data, area_id):
    con = sqlite3.connect('天気.db')
    cur = con.cursor()
    sql_insert_forecast = '''
    INSERT INTO Forecasts (area_id, forecast_date, weather)
    VALUES (?, ?, ?);
    '''
    for forecast in forecast_data[0]['timeSeries'][0]['areas']:
        forecast_date = forecast_data[0]['timeSeries'][0].get('timeDefines', ["不明な日付"])[0]
        cur.execute(sql_insert_forecast, (area_id, forecast_date, forecast['weathers'][0]))
    con.commit()
    con.close()

# 天気予報を表示
def show_forecast(page, code, children):
    forecast_text = ""
    forecast_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
    response = requests.get(forecast_url)
    if response.status_code == 200:
        forecast_data = response.json()
        save_forecast_data(forecast_data, code)
        for forecast in forecast_data[0]['timeSeries'][0]['areas']:
            forecast_text += f"{forecast['area']['name']}: {forecast['weathers'][0]}\n"
    else:
        forecast_text += f"天気予報データを取得できませんでした。 (地域コード: {code})\n"

    for child_code in children:
        child_forecast_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{child_code}.json"
        child_response = requests.get(child_forecast_url)
        if child_response.status_code == 200:
            child_forecast_data = child_response.json()
            save_forecast_data(child_forecast_data, child_code)
            for forecast in child_forecast_data[0]['timeSeries'][0]['areas']:
                forecast_text += f"{forecast['area']['name']}: {forecast['weathers'][0]}\n"
        else:
            forecast_text += f"天気予報データを取得できませんでした。 (childrenコード: {child_code})\n"

    forecast_display = ft.Container(
        width=500,
        content=ft.Text(forecast_text)
    )
    page.controls[0].controls[1] = forecast_display
    page.update()

# 初期化
init_db()

# メイン関数
def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0
    page.title = "天気予報アプリ"

    def handle_expansion_tile_change(e):
        page.open(
            ft.SnackBar(
                ft.Text(f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"),
                duration=1000,
            )
        )
        if e.control.trailing:
            e.control.trailing.name = (
                ft.icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.icons.ARROW_DROP_DOWN_CIRCLE
                else ft.icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    # 地域リストの取得と保存
    area_url = "http://www.jma.go.jp/bosai/common/const/area.json"
    area_data = requests.get(area_url).json()
    save_area_data(area_data)

    # 地域リストを表示するためのExpansionTileを作成
    area_tiles = []
    for center_code, center_info in area_data['centers'].items():
        area_name = center_info['name']
        en_name = center_info['enName']
        office_name = center_info['officeName']
        children_codes = center_info.get('children', [])

        tile = ft.ExpansionTile(
            title=ft.Text(f"{area_name} ({en_name})"),
            subtitle=ft.Text(f"Office: {office_name}"),
            trailing=ft.Icon(ft.icons.ARROW_DROP_DOWN),
            on_change=handle_expansion_tile_change,
            controls=[
                ft.ListTile(
                    title=ft.Text(f"天気予報を表示➡︎"),
                    on_click=lambda e, code=center_code, children=children_codes: show_forecast(page, code, children)
                )
            ]
        )
        area_tiles.append(tile)

    left_panel = ft.Container(
        width=300,
        content=ft.ListView(
            controls=area_tiles
        )
    )

    forecast_display = ft.Container(
        width=500,
        content=ft.Text("天気予報がここに表示されます")
    )

    layout = ft.Row(
        controls=[left_panel, forecast_display],
        expand=True
    )

    page.add(layout)

ft.app(target=main)