# This script generates every possible format for Bitcoin public and private keys
import hashlib
import typing
import Weierstrass
from hashlib import sha256
from binascii import unhexlify
from base58 import b58encode

Point = typing.Tuple[int, int]


# These functions convert integers to bytes
def bytes_from_int(a: int) -> bytes:
    return a.to_bytes(32, "big")


def bytes_x_from_point(P: Point) -> bytes:
    x_coord = Weierstrass.x(P)
    return bytes_from_int(x_coord)


def bytes_y_from_point(P: Point) -> bytes:
    y_coord = Weierstrass.y(P)
    return bytes_from_int(y_coord)


# This function computes a checksum
def checksum_computation(string: str) -> hex:
    cs = hashlib.sha256(hashlib.sha256(unhexlify(string)).digest()).hexdigest()
    checksum = cs[:8]
    return checksum


# This function encodes a private key into a private key in WIF-compressed format
def generate_wif_privkey(private_key : str) -> bytes:
    private_key = '80' + private_key
    checksum = checksum_computation(private_key)
    private_key = private_key + checksum

    return b58encode(unhexlify(private_key))


# This function generates a WIF-format private key
def generate_wif_compressed_privkey(private_key: str) -> bytes:
    private_key = '80' + private_key + '01'
    checksum = checksum_computation(private_key)
    private_key = private_key + checksum

    return b58encode(unhexlify(private_key))


# This function returns an uncompressed public key
def uncompressed_pubkey(P: Point) -> str:
    x_coord = bytes_x_from_point(P).hex()
    y_coord = bytes_y_from_point(P).hex()
    public_key = '04' + x_coord + y_coord
    return public_key


# This function returns a compressed public key
def compressed_pubkey(P: Point) -> str:
    y_coord = Weierstrass.y(P)

    if y_coord % 2 == 1:
        public_key = '03' + bytes_x_from_point(P).hex()
    else:
        public_key = '02' + bytes_x_from_point(P).hex()

    return public_key

