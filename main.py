import asyncio
from signalr_async.netcore import Hub, Client
from signalr_async.netcore.protocols import MessagePackProtocol


class MyHub(Hub):
    async def on_connect(self, connection_id: str) -> None:
        """Will be awaited after connection established"""

    async def on_disconnect(self) -> None:
        """Will be awaited after client disconnection"""

    def on_event_one(self, x: bool, y: str) -> None:
        """Invoked by server synchronously on (event_one)"""

    async def on_event_two(self, x: bool, y: str) -> None:
        """Invoked by server asynchronously on (event_two)"""

    async def get_something(self) -> bool:
        """Invoke (method) on server"""
        return await self.invoke("method", "arg1", 2)


hub = MyHub("my-hub")


@hub.on("event_three")
async def three(z: int) -> None:
    pass


@hub.on
async def event_four(z: int) -> None:
    pass


async def multi_event(z: int) -> None:
    pass


for i in range(10):
    hub.on(f"event_{i}", multi_event)



API_KEY = "374cbc97-3126-441c-9bfa-6df8426380ff"
BASE_URL = "http://feed.beter.co"
FEED_NAME = "incident"

url = f"{BASE_URL}/{FEED_NAME}?ApiKey={API_KEY}"

async def main():

    async with Client(
        url,
        hub,
        connection_options={
            "protocol": MessagePackProtocol(),
        },
    ) as client:
        return await hub.get_something()


asyncio.run(main())