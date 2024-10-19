## 概要
OBS Studioで配信を開始したときにDiscordに自動的に通知を送る機能

## 必要なもの
- OBS Studio：配信に使うOBS環境です
- Python：OBS Studioのスクリプト機能を使うためにPythonが必要です。OBSにPythonスクリプトが有効になっているか確認してください
- Discord Webhook：通知を送信するためのDiscordのWebhookを作成します

## 手順
#### 1. Discord Webhookを設定する
まずは，Discordで通知を送るためのWebhookを作成します。

1. 自分がホストしているDiscordサーバーに入り，通知を送りたいチャンネルを選択します。
![無題.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3680988/6c59c2e8-f5b4-2c74-4d0a-d5d42f9faa96.png)

1. チャンネルの「設定」メニューを開き，「連携サービス」タブから「ウェブフックを作成」を選択します。
![スクリーンショット 2024-10-19 140438.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3680988/0c69da1e-b37f-3924-5b47-0b19823c780e.png)

1. 「新しいウェブフック」が作成されますので，名前やアイコンを設定した後，「ウェブフック URL」をコピーします。このWebhook URLは後ほどスクリプトで使用するので，メモしておいてください。
![スクリーンショット 2024-10-19 140552.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3680988/10999174-ecb5-1121-c5ab-39c2438864a9.png)


#### 2. Pythonスクリプトの作成
次に，OBS Studio用のPythonスクリプトを作成します。以下のコードをコピーし.py 拡張子で保存してください（例：discord_notification.py）。

```py:discord_notification.py
import obspython as obs
import requests

webhook_url = ""
message_content = ""
notify_discord = False

# スクリプトが最初にロードされたときの設定
def script_description():
    return (
        "OBSで配信を開始したときにDiscordに通知を送るスクリプトです。\n"
        "設定画面からWebhook URLと通知のオン/オフを設定できます。"
    )

# スクリプトがロードされたときに呼ばれる関数
def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)

# 配信開始時に呼ばれる関数
def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        # チェックボックスがオンの場合にのみ通知を送信
        if notify_discord and webhook_url and message_content:
            send_discord_notification()
            # Discordに通知を送る関数

# Discordに通知を送る関数
def send_discord_notification():
    payload = {"content": message_content}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Discordに通知を送信しました")
        else:
            print(f"エラーが発生しました: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"リクエスト中にエラーが発生しました: {e}")

# スクリプトの設定が変更されたときに呼ばれる関数
def script_update(settings):
    global notify_discord, webhook_url, message_content
    notify_discord = obs.obs_data_get_bool(settings, "notify_discord")
    webhook_url = obs.obs_data_get_string(settings, "webhook_url")
    message_content = obs.obs_data_get_string(settings, "message_content")

# スクリプトの設定UIを定義する関数
def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_bool( # Discordに通知を送るチェックボックス
        props, "notify_discord", "Discordに通知を送る"
    )
    obs.obs_properties_add_text( # Webhook URLの入力欄を追加
        props, "webhook_url", "Webhook URL", obs.OBS_TEXT_DEFAULT
    )
    obs.obs_properties_add_text( # メッセージ内容の入力欄
        props, "message_content", "送信するメッセージ", obs.OBS_TEXT_MULTILINE
    )

    return props

```


#### 3. OBS Studioにスクリプトを追加する

1. OBS Studioを起動し，「ツール」メニューから「スクリプト」を選択します。<br>
![OBS](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3680988%2F06826eea-4b9f-9aaf-ac93-5b9373000b2e.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=acd880d19e898737210c91714b406d6e)

2. 「スクリプトマネージャー」が表示されるので，「+」ボタンをクリックして，先ほど保存したPythonスクリプトを選択します。<br>
![スクリプト](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3680988%2F2b2cbfc2-590c-3acb-85ad-765c0fd8c04a.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=421bd6482d8a46851a325c872cd1137f)<br>
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3680988/fd223e79-4316-be1d-8e78-089daf6ea88d.png)<br>

3. スクリプトを選択すると，設定画面に以下のオプションが表示されます：
    - 「Discordに通知を送る」: 通知を有効にするチェックボックス
    - 「Webhook URL」: 先ほどコピーしたDiscordのWebhook URLを入力する
    - 「送信するメッセージ」: 配信開始時に送信したいメッセージを入力します（例：「配信が開始されました！」など）。<br>
![スクリーンショット 2024-10-19 140658.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3680988/7af7a0ab-ac79-b5a8-da23-7a0fe7a2b6fa.png)


#### 4. 動作確認
設定が完了したら，OBSでテスト的に配信を開始してみてください。正しく設定されていれば，指定したDiscordチャンネルに通知が自動的に送信されるはずです。

## 参考

https://qiita.com/yhotta240/items/6c19adecb725b2205f5b

▼ Python/Lua スクリプト

https://docs.obsproject.com/scripting

▼ イベントが発生したときに呼び出されるコールバック関数

https://docs.obsproject.com/reference-frontend-api#c.obs_frontend_add_event_callback

▼ イベント一覧

https://docs.obsproject.com/reference-frontend-api#c.obs_frontend_event
