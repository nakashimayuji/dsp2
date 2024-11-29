import requests  # HTTPリクエストを送信するためのライブラリ
import flet as ft  # UIを作成するためのライブラリ

def main(page: ft.Page):
    page.spacing = 0  # ページのスペーシングを設定
    page.padding = 0  # ページのパディングを設定
    page.title = "天気予報アプリ"  # ページのタイトルを設定

    def handle_expansion_tile_change(e):
        # ExpansionTileの状態が変わったときに呼び出される関数
        page.open(
            ft.SnackBar(
                ft.Text(f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"),# バーに表示するメッセージ
                duration=1000,
            )
        )
        if e.control.trailing:
            # アイコンを変更
            e.control.trailing.name = (
                ft.icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.icons.ARROW_DROP_DOWN_CIRCLE
                else ft.icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    # 地域リストの取得
    area_url = "http://www.jma.go.jp/bosai/common/const/area.json"
    area_data = requests.get(area_url).json()  # JSONデータを取得してパース

    # 地域リストを表示するためのExpansionTileを作成
    area_tiles = []
    for center_code, center_info in area_data['centers'].items():
        area_name = center_info['name']  # 地域名を取得してarea_nameに代入
        en_name = center_info['enName']  # 英語名 (ローマ字) を取得してen_nameに代入
        office_name = center_info['officeName']  # 事務所名 (ローマ字) を取得してoffice_nameに代入
        children_codes = center_info.get('children', [])  # 子地域のコードリスト
        
        # ExpansionTileを作成
        tile = ft.ExpansionTile(
            title=ft.Text(f"{area_name} ({en_name})"), # タイトルを設定
            subtitle=ft.Text(f"Office: {office_name}"),# サブタイトルを設定
            trailing=ft.Icon(ft.icons.ARROW_DROP_DOWN),# トレーリングアイコンを設定
            on_change=handle_expansion_tile_change,# 状態変更時のイベントハンドラを設定
            controls=[
                ft.ListTile(
                    title=ft.Text(f"天気予報を表示➡︎"),# タイトルを設定
                    on_click=lambda e, code=center_code, children=children_codes: show_forecast(page, code, children)# クリック時の動作を設定
                )
            ]
        )
        area_tiles.append(tile)  # リストに追加
#スライド内のお手本に近づけるために、左と右で分けるレイアウトに設定しました。
    # 左側の地域リスト
    left_panel = ft.Container(
        width=300,
        content=ft.ListView(
            controls=area_tiles  # 作成した地域リストを表示
        )
    )

    # 右側の天気予報表示エリア
    forecast_display = ft.Container(
        width=500,
        content=ft.Text("天気予報がここに表示されます")  # 初期メッセージ
    )

    # レイアウトを左右に分割
    layout = ft.Row(
        controls=[left_panel, forecast_display],
        expand=True
    )

    
    page.add(layout)

def show_forecast(page, code, children):
    forecast_text = ""

    # 地域コードを指定して天気情報を取得
    forecast_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
    response = requests.get(forecast_url)
    
    if response.status_code != 200:
        forecast_text += f"天気予報データを取得できませんでした。 (地域コード: {code})\n"
    else:
        forecast_data = response.json()
        # 天気情報の表示
        for forecast in forecast_data[0]['timeSeries'][0]['areas']:
            forecast_text += f"{forecast['area']['name']}: {forecast['weathers'][0]}\n"

    # childrenの天気情報を取得 
    for child_code in children:
        child_forecast_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{child_code}.json"
        child_response = requests.get(child_forecast_url)
        
        if child_response.status_code != 200:
            forecast_text += f"天気予報データを取得できませんでした。 (childrenコード: {child_code})\n"
        else:
            child_forecast_data = child_response.json()
            # 天気情報の表示
            for forecast in child_forecast_data[0]['timeSeries'][0]['areas']:
                forecast_text += f"{forecast['area']['name']}: {forecast['weathers'][0]}\n"

    # 右側の天気予報表示エリアを更新
    forecast_display = ft.Container(
        width=500,
        content=ft.Text(forecast_text)
    )

    # レイアウトを更新
    page.controls[0].controls[1] = forecast_display
    page.update()

def close_dialog(dialog):
    dialog.open = False
    dialog.update()

ft.app(target=main)  # アプリを起動し、main関数をターゲットとして指定
#用語解説⬇︎
#エンドポイントとは、クライアントがアクセスするためのURLのことです。APIのエンドポイントは、APIのリクエストを送信するためのURLのことです。
#エンドポイントは、APIのリクエストを送信するためのURLのことです。
#APIのエンドポイントは、APIのリクエストを送信するためのURLのことです。