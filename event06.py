from secp256k1 import PrivateKey, PublicKey
import time
import json
import hashlib
import asyncio
from websockets.sync.client import connect

chave_privada_obj = PrivateKey()
hash_chave_privada = chave_privada_obj.serialize()
chave_privada_bytes = chave_privada_obj.deserialize(hash_chave_privada)

chave_publica_obj = chave_privada_obj.pubkey
chave_publica_bytes = chave_publica_obj.serialize()
hash_chave_publica = hashlib.sha256(chave_publica_bytes).hexdigest()

timestamp = int(time.time())

evento01 = {
	"id" : "",
	"pubkey" : "",
	"created_at" : "",
	"kind" : "",
	"tags" : "",
	"content" : "",
	"sig" : ""
}

evento01["id"] = 0
evento01["pubkey"] = hash_chave_publica
evento01["created_at"] = timestamp
evento01["kind"] = 1
evento01["tags"] = []
evento01["content"] = "Hello World!"

conteudo_evento = [evento01["id"], evento01["pubkey"], evento01["created_at"], evento01["kind"], evento01["tags"], evento01["content"]]
conteudo_evento = json.dumps(conteudo_evento).replace(" ","")

id_evento_obj = hashlib.sha256(conteudo_evento.encode("utf-8"))
id_evento = id_evento_obj.hexdigest()

evento01["id"] = id_evento

assinatura_obj = chave_privada_obj.ecdsa_sign(id_evento.encode("utf-8"))
assinatura_bytes = chave_privada_obj.ecdsa_serialize(assinatura_obj)
hash_assinatura = hashlib.blake2b(assinatura_bytes).hexdigest() #cuspir com 64bytes
evento01["sig"] = hash_assinatura
verificacao = chave_publica_obj.ecdsa_verify(evento01["id"].encode(), assinatura_obj)


obj_json = json.dumps(evento01)

msg = f'["EVENT", {obj_json}]'

#local-client-side
def hello():
	with connect("wss://relay.primal.net") as websocket:
		websocket.send(msg)
		message = websocket.recv()
		print(f"Received: {message}")

hello()
