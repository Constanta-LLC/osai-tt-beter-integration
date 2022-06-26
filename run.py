import asyncio

from loguru import logger

from coach_client import CoachClientAsync
from config import (
    coach_url,
    system_kit_id,
    coach_auth_token,
)
from score_updater import ScoreUpdater
from ws_async_client import ws_loop


async def main():
    coach_cli = CoachClientAsync(coach_url, system_kit_id, coach_auth_token)
    try:
        await coach_cli.startup()
        score_updater = ScoreUpdater(coach_cli)
        await ws_loop(score_updater.on_upd)
    finally:
        await coach_cli.shutdown()


if __name__ == "__main__":
    logger.add("logs/service.log", rotation="1 day")
    asyncio.run(main())
