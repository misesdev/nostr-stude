import json
from websockets.sync.client import connect

class RelayPool:

    def __init__(self, subscription = "5830625b2fff8d359295"):
        self.subscription = subscription

    def fetchEvents(self, author: str, kind: int, limit: int):
        
        filter = { 
            "authors": [author],
            "kinds": [kind], 
            "limit": limit
        }

        with connect("wss://relay.damus.io") as websocket:
            websocket.send(f"[\"REQ\",\"{self.subscription}\", {json.dumps(filter)}]")
            
            event = websocket.recv()

            print(f"event: {event}")

