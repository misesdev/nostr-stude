from secp256k1 import PrivateKey

class KeyPair:

    def __init__(self, privatekey: str):
        self.privatekey = PrivateKey(bytes.fromhex(privatekey))

    def sign(self, message: str):
        message_bytes = bytes.fromhex(message)

        return self.privatekey.schnorr_sign(message_bytes, None, raw=True).hex()

    def verify(self, message: str, signature: str):
        message_bytes = bytes.fromhex(message)
        signature_bytes = bytes.fromhex(signature)

        return self.privatekey.pubkey.schnorr_verify(message_bytes, signature_bytes, None, raw=True)

    def getPubkey(self):
        return self.privatekey.pubkey.serialize(compressed=False).hex()[2:66]




