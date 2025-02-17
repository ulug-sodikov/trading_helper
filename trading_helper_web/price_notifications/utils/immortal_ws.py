import time

import websocket


class ImmortalWebSocket(websocket.WebSocket):
    """
    WebSocket that will try to reestablish a connection every two seconds
    if the connection has been closed by the websocket server.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # https://peps.python.org/pep-0412/
        self._url = None

    def connect(self, url, **options):
        self._url = url

        while True:
            try:
                return super().connect(url, **options)
            except (
                    ConnectionRefusedError,
                    ConnectionResetError,
                    websocket.WebSocketConnectionClosedException
            ):
                time.sleep(2)

    def recv(self):
        try:
            return super().recv()
        except websocket.WebSocketConnectionClosedException:
            self.connect(self._url)
