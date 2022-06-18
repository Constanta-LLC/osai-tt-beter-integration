import os
import sys
from time import sleep

from hub import init_hub_connection
from score_updater import ScoreUpdater


address = os.getenv("ADDRESS", "wss://feed.beter.co")
channel = os.getenv("CHANNEL", "incident")
apiKey = os.getenv("API_KEY", "374cbc97-3126-441c-9bfa-6df8426380ff")
snapshotBatchSize = os.getenv("BATCH_SIZE", "1")

if __name__ == "__main__":
    server_url = (
        f"{address}/{channel}?ApiKey={apiKey}&snapshotBatchSize={snapshotBatchSize}"
    )

    score_updater = ScoreUpdater()
    hub_connection = init_hub_connection(server_url, score_updater.on_upd)

    try:
        hub_connection.start()
        while True:
            sleep(1)
    finally:
        hub_connection.stop()
        sys.exit(0)
