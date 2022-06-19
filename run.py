import sys
from time import sleep

from coach_client import CoachClient
from config import (
    beter_base_url,
    beter_feed_channel,
    beter_api_key,
    beter_snapshot_batch_size,
    coach_url,
    system_kit_id,
    coach_auth_token,
)
from hub import init_hub_connection
from score_updater import ScoreUpdater

if __name__ == "__main__":
    beter_server_url = f"{beter_base_url}/{beter_feed_channel}?ApiKey={beter_api_key}&snapshotBatchSize={beter_snapshot_batch_size}"
    coach_cli = CoachClient(coach_url, system_kit_id, coach_auth_token)
    score_updater = ScoreUpdater(coach_cli)
    hub_connection = init_hub_connection(beter_server_url, score_updater.on_upd)

    try:
        hub_connection.start()
        while True:
            sleep(1)
    finally:
        hub_connection.stop()
        sys.exit(0)
