#Lo scopo di questo script è ottenere i vari formati possibili per le chiavi private e pubbliche su Bitcoin
import hashlib
import typing
import Weierstrass
from hashlib import sha256
from binascii import unhexlify
from base58 import b58encode

Point = typing.Tuple[int, int]

#These functions convert integers to bytes
def bytes_from_int(a : int) -> bytes:
    return a.to_bytes(32, "big")

def bytes_x_from_point(P : Point) -> bytes:
    x_coord = Weierstrass.x(P)
    return bytes_from_int(x_coord)

def bytes_y_from_point(P : Point) -> bytes:
    y_coord = Weierstrass.y(P)
    return bytes_from_int(y_coord)

#This function encodes a private key into a private key in WIF-compressed format
def generate_wif_privkey(private_key : str) -> bytes:
    private_key = '80' + private_key
    private_key_bytes = unhexlify(private_key)
   # sha256 = hashlib.sha256()
    #utilizzare il metodo/funzione update e poi visualizzare con il metodo digest
    sha256().update(private_key_bytes)
    hash = sha256().digest()

    sha256().update(hash)
    hash2 = sha256().hexdigest()

    checksum = hash2[:8]
    private_key = private_key + checksum

    #codifichiamo utilizzando la funzione b58encode. L'input va espresso il bytes
    return b58encode(unhexlify(private_key))

#Questa funzione genera la chiave privata in formato WIF a partire da una chiave privata
def generate_wif_compressed_privkey(private_key : str) -> bytes:
    private_key = '80' + private_key + '01'
    private_key_bytes = unhexlify(private_key)
    sha256 = hashlib.sha256()
    #utilizzare il metodo/funzione update e poi visualizzare con il metodo digest
    sha256.update(private_key_bytes)
    hash = sha256.digest()

    sha256.update(hash)
    hash2 = sha256.hexdigest()

    checksum = hash2[:8]

    private_key = private_key + checksum

    #codifichiamo utilizzando la funzione b58encode. L'input va espresso il bytes
    return b58encode(unhexlify(private_key))

#Questa funzione restituisce la chiave pubblica in formato non-compresso (prefisso 0x04)
def uncompressed_pubkey(P : Point) -> str:
    x_coord = bytes_x_from_point(P).hex()
    y_coord = bytes_y_from_point(P).hex()
    public_key = '04' + x_coord + y_coord
    return public_key

#Questa funzione restituisce la chiave pubblica in formato compresso (prefisso 0x02 oppure 0x03)
def compressed_pubkey(P : Point) -> str:
    y_coord = Weierstrass.y(P)

    if y_coord % 2 == 1:
        public_key = '03' + bytes_x_from_point(P).hex()
    else:
        public_key = '02' + bytes_x_from_point(P).hex()

    return public_key