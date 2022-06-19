import os

coach_url = os.getenv("COACH_BASE_URL", "https://deep.osai.ai/osai-table-tennis-coach/")


system_kit_id = os.getenv("SYSTEM_KIT_ID", 921)
coach_auth_token = os.getenv(
    "COACH_AUTH_TOKEN",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjIiLCJzdGFydCI6MTY1NTQ2MzI5OC40MjQ5MjZ9.VHfg0p6JLlxBMAjm7KxJE5BMMnqc1aIMNjjPmkKdoPU",
)

beter_base_url = os.getenv("BETER_BASE_URL", "wss://feed.beter.co")
beter_feed_channel = os.getenv("BETER_FEED_CHANNEL", "incident")
beter_api_key = os.getenv("BETER_API_KEY", "374cbc97-3126-441c-9bfa-6df8426380ff")
beter_snapshot_batch_size = os.getenv("BETER_SNAPSHOT_BATCH_SIZE", "1")
