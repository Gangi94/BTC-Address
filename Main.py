import Weierstrass
import KeyFormats
import Address
import time


#Private_key examples (taken from the Mastering Bitcoin book)

#private_key = '1e99423a4ed27608a15a2616a2b0e9e52ced330ac530edcc32c8ffc6a526aedd'
private_key = '3aba4162c7251c891207b747840551a71939b0de081f85c4e44cf7c13e41daa6'
private_key_int = int(private_key, 16)

print('The private key is', private_key)
print('The private key (decimal) is', private_key_int)
print('The private key (WIF-format) is', KeyFormats.generate_wif_privkey(private_key))
print('The private key (WIF-compressed format) is', KeyFormats.generate_wif_compressed_privkey(private_key))
print()

#Computation of the public key
public_key = Weierstrass.pubkey_gen(private_key_int)

print('The public key (integer) is', public_key)
print('The uncompressed public key is ', KeyFormats.uncompressed_pubkey(public_key))
print('The compressed public key is', KeyFormats.compressed_pubkey(public_key))
print()

#Computation of the address
print('The Bitcoin address (b58check) related to the previous uncompressed public key is', Address.p2pkh_address(KeyFormats.uncompressed_pubkey(public_key)))
print('The Bitcoin address (b58check) related to the previous compressed public key is', Address.p2pkh_address(KeyFormats.compressed_pubkey(public_key)))
print()

#P2PKH address computation example
P2PKH_public_key = '0484ecc0d46f1918b30928fa0e4ed99f16a0fb4fde0735e7ade8416ab9fe423cc5412336376789d172787ec3457eee41c04f4938de5cc17b4a10fa336a8d752adf'

print('The P2PKH address is', Address.p2pkh_address(P2PKH_public_key))
print()

#P2SH address computation example
p2sh_script = '5141042f90074d7a5bf30c72cf3a8dfd1381bdbd30407010e878f3a11269d5f74a58788505cdca22ea6eab7cfb40dc0e07aba200424ab0d79122a653ad0c7ec9896bdf51ae'

print('The P2SH address is', Address.p2sh_address(p2sh_script))
print()

#segwit computation example
segwit_public_key = '029f59c6c043ce7bf41d6b2206077b3fff513fa06564ca143e36948b2c5cfaa32e'

print('The segwit address is', Address.segwit_address(segwit_public_key))
print()




#Calcolo del vanity address
vanity_string = 'k'

#start = time.time()
#print('Il vanity address che stiamo cercando è', Address.vanity_address_generator(vanity_string))
#end = time.time()
#print('Il tempo richiesto per ottenere il vanity address è stato di', end - start, 'secondi')