#In questo file otterremo gli address per le transazioni bitcoin P2PKH P2SH, P2WPKH e infine vedremo come
#generare vanity addresses

import Weierstrass
import hashlib
from binascii import unhexlify
from base58 import b58encode
import bech32
import KeyFormats
import time


#This function generates a P2PKH address
def p2pkh_address(public_key : str) -> bytes:
    public_key_bytes = unhexlify(public_key)

    sha256 = hashlib.sha256()
    sha256.update(public_key_bytes)
    hash = sha256.digest()

    ripemd160 = hashlib.new('Ripemd160')
    ripemd160.update(hash)
    hash2 = ripemd160.hexdigest()
    #print('L\'address che compare nel locking script di una transazione p2pkh è', hash2)

    hash3 = '00' + hash2

    #Checksum computation
    hash3_bytes = unhexlify(hash3)
    sha256.update(hash3_bytes)
    hash4 = sha256.digest()
    sha256.update(hash4)
    hash5 = sha256.hexdigest()
    checksum = hash5[:8]

    hash_final = hash3 + checksum
    hash_final_bytes = unhexlify(hash_final)

    return b58encode(hash_final_bytes)

#This function generates a P2SH address
def p2sh_address(script : str) -> bytes:
    script_bytes = unhexlify(script)

    sha256 = hashlib.sha256()
    sha256.update(script_bytes)
    hash = sha256.digest()

    ripemd160 = hashlib.new('Ripemd160')
    ripemd160.update(hash)
    hash2 = ripemd160.hexdigest()
    print('The locking script address is', hash2)

    hash3 = '05' + hash2

    #Calcolo del checksum
    hash3_bytes = unhexlify(hash3)
    sha256.update(hash3_bytes)
    hash4 = sha256.digest()
    sha256.update(hash4)
    hash5 = sha256.hexdigest()
    checksum = hash5[:8]

    hash_final = hash3 + checksum
    hash_final_bytes = unhexlify(hash_final)

    return b58encode(hash_final_bytes)

#This function generates a P2WPKH address
def segwit_address(public_key : str) -> str:
    public_key_bytes = unhexlify(public_key)

    sha256 = hashlib.sha256()
    sha256.update(public_key_bytes)
    hash = sha256.digest()

    ripemd160 = hashlib.new('Ripemd160')
    ripemd160.update(hash)
    witness_program = ripemd160.hexdigest()
    print('The witness program is', witness_program)
    witness_program_bytes = unhexlify(witness_program)

    return bech32.encode('bc', 0, witness_program_bytes)


#Questa funzione genera vanity address
def vanity_address_generator(vanity_string : str):

    vanity_string = '1' + vanity_string
    vanity_string_length = len(vanity_string)

    private_key_counter = 2

    while private_key_counter <= Weierstrass.n:

        start = time.time()
        public_key = Weierstrass.pubkey_gen(private_key_counter)
        end = time.time()
        print('Il tempo richiesto per calcolare una chiave pubblica è di', end - start, 'secondi')
        public_key_str = KeyFormats.compressed_pubkey(public_key)
        address = p2pkh_address(public_key_str)
        address_string = address[:vanity_string_length]
        address_string = address_string.decode('utf-8')

        if vanity_string == address_string:
            return address

        private_key_counter = private_key_counter + 1










