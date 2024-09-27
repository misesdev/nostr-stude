from websockets.sync.client import connect
import json

from keyPair import KeyPair
from event import Event
from relayPool import RelayPool

relayPool = RelayPool([
       "wss://relay.damus.io"
    ])

keyPair = KeyPair("b2776165d40acc349ad1f7f11105b037a3403971ee1be87787b47b407b6eb77f")

user_data = json.dumps({ "name": "Dev Test", "displayName": "Hangle" })

event = Event(kind=0, author=keyPair.getPubkey(), content=user_data)

event.sign(keyPair)

msg = f'["EVENT", {event.serialise()}]'

def hello():
	with connect("wss://relay.damus.io") as websocket:
		websocket.send(msg)
		message = websocket.recv()
		print(f"Received: {message}")


hello()

relayPool.fetchEvents(keyPair.getPubkey(), 0, 1)

