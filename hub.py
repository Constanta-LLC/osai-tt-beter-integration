import logging

from signalrcore.hub_connection_builder import HubConnectionBuilder


def init_hub_connection(server_url, on_upd_cb):
    hub_connection = (
        HubConnectionBuilder()
        .with_url(server_url, {"skip_negotiation": server_url.startswith("ws")})
        .configure_logging(logging.ERROR, socket_trace=True)
        .with_automatic_reconnect(
            {
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 1,
                "max_attempts": None,
            }
        )
        .build()
    )
    hub_connection.on_open(
        lambda: print("connection opened and handshake received ready to send messages")
    )
    hub_connection.on_close(lambda: print("connection closed"))
    hub_connection.on("OnUpdate", on_upd_cb)
    return hub_connection
