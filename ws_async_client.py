import websockets
from loguru import logger
from pydantic import ValidationError

from config import ws_subscribe_command, beter_ws_url


async def ws_loop(on_msg):
    while True:
        try:
            async with websockets.connect(beter_ws_url) as ws:
                logger.info(f"Connected to {beter_ws_url}")
                await ws.send(ws_subscribe_command)
                # ignore snapshot msg
                _ = await ws.recv()

                while True:
                    try:
                        msg = await ws.recv()
                        await on_msg(msg)
                    except ValidationError as e:
                        logger.error(e.json())

        except Exception as e:
            logger.exception(e)
