# In questo file otterremo gli address per le transazioni bitcoin P2PKH P2SH, P2WPKH e infine vedremo come
# generare vanity addresses

import Weierstrass
import hashlib
from binascii import unhexlify, hexlify
from base58 import b58encode
import bech32
import KeyFormats
import time


# This function generates a P2PKH address
def p2pkh_address(public_key: str) -> bytes:
    public_key_bytes = unhexlify(public_key)

    sha256 = hashlib.sha256()
    sha256.update(public_key_bytes)
    hash_temp = sha256.digest()

    ripemd160 = hashlib.new('Ripemd160')
    ripemd160.update(hash_temp)
    hash2_temp = ripemd160.hexdigest()
    print('The locking script is', hash2_temp)

    hash3_temp = '00' + hash2_temp

    # Checksum computation
    checksum = KeyFormats.checksum_computation(hash3_temp)

    hash_final = hash3_temp + str(checksum)
    hash_final_bytes = unhexlify(hash_final)

    return b58encode(hash_final_bytes)


# This function generates a P2SH address
def p2sh_address(script: str) -> bytes:
    script_bytes = unhexlify(script)

    sha256 = hashlib.sha256()
    sha256.update(script_bytes)
    hash_temp = sha256.digest()

    ripemd160 = hashlib.new('Ripemd160')
    ripemd160.update(hash_temp)
    hash2_temp = ripemd160.hexdigest()
    print('The locking script address is', hash2_temp)

    hash3_temp = '05' + hash2_temp

    # Checksum computation
    checksum = KeyFormats.checksum_computation(hash3_temp)

    hash_final = hash3_temp + checksum
    hash_final_bytes = unhexlify(hash_final)

    return b58encode(hash_final_bytes)


# This function generates a P2WPKH address
def segwit_address(public_key: str) -> str:
    public_key_bytes = unhexlify(public_key)

    sha256 = hashlib.sha256()
    sha256.update(public_key_bytes)
    hash_temp = sha256.digest()

    ripemd160 = hashlib.new('Ripemd160')
    ripemd160.update(hash_temp)
    witness_program = ripemd160.hexdigest()
    print('The witness program is', witness_program)
    witness_program_bytes = unhexlify(witness_program)

    return bech32.encode('bc', 0, witness_program_bytes)


# This function generates vanity addresses
def vanity_address_generator(vanity_string: str):

    vanity_string = '1' + vanity_string
    vanity_string_length = len(vanity_string)

    private_key_counter = 2

    while private_key_counter <= Weierstrass.n:

        start = time.time()
        public_key = Weierstrass.pubkey_gen(private_key_counter)
        end = time.time()
        print('The time required to compute a public key is', end - start, 'seconds')
        public_key_str = KeyFormats.compressed_pubkey(public_key)
        address = p2pkh_address(public_key_str)
        address_string = address[:vanity_string_length]
        address_string = address_string.decode('utf-8')

        if vanity_string == address_string:
            return address

        private_key_counter = private_key_counter + 1










