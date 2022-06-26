import json
import os

coach_url = os.getenv("COACH_BASE_URL", "https://deep.osai.ai/osai-table-tennis-coach/")

system_kit_id = os.getenv("SYSTEM_KIT_ID", 1)
coach_auth_token = os.getenv(
    "COACH_AUTH_TOKEN",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjIiLCJzdGFydCI6MTY1NTQ2MzI5OC40MjQ5MjZ9.VHfg0p6JLlxBMAjm7KxJE5BMMnqc1aIMNjjPmkKdoPU",
)

beter_ws_url = os.getenv("BETER_WS_URL", "wss://ws.setka-cup.com/")
beter_ws_auth_client = os.getenv("BETER_WS_AUTH_CLIENT", "OSAI")
beter_ws_auth_token = os.getenv(
    "BETER_WS_AUTH_TOKEN", "2BjyYCXE5PGDBAoENjPb3ttotf3wbTfX"
)
beter_ws_channel = os.getenv("BETER_WS_CHANNEL", "incident-feed")

ws_subscribe_command = json.dumps(
    {
        "command": "subscribe",
        "channel": beter_ws_channel,
        "auth": {
            "client": beter_ws_auth_client,
            "token": beter_ws_auth_token,
        },
    }
)
