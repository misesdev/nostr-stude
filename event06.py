from secp256k1 import PrivateKey, PublicKey 
from websockets.sync.client import connect
import time
import json
import hashlib

#chave privada
chave_privada_obj = PrivateKey(bytes.fromhex("a4fef14e375d7d7726851120afbed7755a668011aa136190944ba31d9abfcd68"))
hash_chave_privada = chave_privada_obj.serialize()
chave_privada_bytes = chave_privada_obj.deserialize(hash_chave_privada)
private_key_hex = chave_privada_bytes.hex()
print(f"private key: ...: {private_key_hex}")

#chave publica
chave_publica_obj = chave_privada_obj.pubkey

# A chave pública deve ser descmprimida. Em criptografia de curva eliptca a chave pública é 
# a posição x + y do "plano cartesiano", e a chave privada a quantidade de intercessões que geram aquela posição.
# Atravéz de um cálculo é possível deduzir a posição y dado uma posição x, o inverso também é verdade, e por isso
# geralmente lidamos com chaves pública comprimidas [prefixo + x] ou [prefixo + y], então, para comprimir passamos
# o parametro compressed = True

# com compressed True, é retornada o valor do exio Y da chave pública, o evento exepra o valor de x da chave pública
# então pegamos o calor descompactado [prefix+x+y], ignoramos o prefixo e pegamos os próximos 64 caracteres: [2:66]
chave_publica_bytes = chave_publica_obj.serialize(compressed = False)
hash_chave_publica = hashlib.sha256(chave_publica_bytes).hexdigest()

# A chave pública comprimida é apenas o prefixo de um byte e o número de 32 bytes x ou y, queremos apenas o número 
# de 32 bytes como descrito na documentação. no caso da chave comprimida em x fica o prefixo 0x02 + x e no caso de y
# fica o prefixo 0x03 + y, então pegamos a partir do terceiro caractere hexadecimal até o fim, e temos a pubkey:
public_key_hex = chave_publica_bytes.hex()[2:66]
print(f"public key ...: {public_key_hex}")

#created_at
timestamp = int(time.time())

#evento
# the kind 0 for the first event of user -> metadata 
evento01 = {
	"id" : 0,
	"pubkey" : public_key_hex, # aqui passamos a chave publica em hexadecimal
	"created_at" : timestamp,
	"kind" : 0, 
    "tags" : [],
    "content" : json.dumps({ "name": "malboro", "displayName": "Mal Boro" }),
}

#gerando id
conteudo_evento = [
    evento01["id"], 
    evento01["pubkey"], 
    evento01["created_at"], 
    evento01["kind"], 
    evento01["tags"], 
    evento01["content"]
]

# Em dumps, basta indicar os separators do json, isso garante que não haverão espaços extras. 
# A função replace apenas substitui os baytes que você passa para ela.
conteudo_evento = json.dumps(conteudo_evento, separators=(",", ":"))

id_evento_obj = hashlib.sha256(conteudo_evento.encode())

id_evento = id_evento_obj.hexdigest()

evento01["id"] = id_evento
print(f"event id ...: {id_evento}")

#assinatura
assinatura_obj = chave_privada_obj.ecdsa_sign(bytes.fromhex(id_evento))

#assinatura_bytes = chave_privada_obj.ecdsa_serialize(assinatura_obj)

# Na assinatura o relay espera um hexadecimal de 64 bytes, porém a assinatura ecdsa padrão e formada
# com dois números inteiros de 32 bytes s e r no formato (DER) que considera o cabeçalho, que é como se fosse 
# o prefixo no caso da chave pública então ficam 71 bytes, então tem que usar a função ecdsa_serialize_compact:

assinatura_bytes = chave_privada_obj.ecdsa_serialize_compact(assinatura_obj)

#hash_assinatura = hashlib.blake2b(assinatura_bytes).hexdigest() #cuspir com 64bytes
# Essa função também está incorreta, dado que já temos a assinatura compactada sem prefixos, apenas r+s
# basta converter para hexadecimal:

assinatura_hex = assinatura_bytes.hex()
print(f"assinatura ...: {assinatura_hex}")

evento01["sig"] = assinatura_hex

verificacao = chave_publica_obj.ecdsa_verify(bytes.fromhex(id_evento), assinatura_obj)
print(f"Assinatura verificada: {verificacao}")

#transmitindo evento
obj_json = json.dumps(evento01)

msg = f'["EVENT", {obj_json}]'

def hello():
	with connect("wss://relay.damus.io") as websocket:
		websocket.send(msg)
		message = websocket.recv()
		print(f"Received: {message}")
     


hello()
