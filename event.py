import json
from time import time
from secp256k1 import hashlib
from keyPair import KeyPair

class Event:
    def __init__(self, 
                 kind: int, 
                 author: str, 
                 content: str):
        self.kind = kind
        self.author = author
        self.content = content
        self.created_at = int(time())
        self.tags = []
        self.sig = None
        self.id = None

    def sign(self, pairKey: KeyPair):
        
        event_id = self.generateId()

        self.sig = pairKey.sign(event_id)

    def generateId(self): 
        content = [0, self.author, self.created_at, self.kind, self.tags, self.content ]

        str_content = json.dumps(content, separators=(",", ":")).encode()

        self.id = hashlib.sha256(str_content).hexdigest()

        return self.id

    def serialise(self):

        if(self.sig == None):
            print(f"Please sign event")
            return None
        
        event = {
                "id": self.id,
                "pubkey": self.author,
                "created_at": self.created_at,
                "kind": self.kind,
                "tags": self.tags,
                "content": self.content,
                "sig": self.sig
            }

        return json.dumps(event)

        

     

