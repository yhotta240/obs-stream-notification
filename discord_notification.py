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