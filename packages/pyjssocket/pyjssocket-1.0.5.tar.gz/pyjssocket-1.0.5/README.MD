# PyJSSocket
This is a Python library that lets you communicate through JavaScript WebSocket client.

## Installation
To install this library run `pip install pyjssocket` in your terminal.

## Example
Here is an example of a server that can handle multiple calls from a different JS clients
```
import json
import jsserver
import socketserver

import threading
import time

class MyJsRequestHandler(jsserver.JSBaseRequestHandler):

    def on_handshake(self, host: str, url: str, seqKey: str):
        def target():
            while True:
                self.send_response(json.dumps({'success': True, 'time': time.time()}))
                time.sleep(1)

        super().on_handshake(host, url, seqKey)

        thread = threading.Thread(target=target, daemon=True)
        thread.start()

    def on_message(self, data: bytes):
        self.send_response(json.dumps({'success': True, 'time': time.time()}))

    def on_error(self, value: str):
        self.send_response(json.dumps({'success': False, 'message': value}))

if __name__ == '__main__':
    with socketserver.ThreadingTCPServer(('0.0.0.0', 451), MyJsRequestHandler) as tcpServer:
        tcpServer.serve_forever()
```