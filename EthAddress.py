import random
import time
import ecdsa
from binascii import hexlify, unhexlify
import sha3
import rlp


def private_key_gen():
    return hexlify(ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1).to_string())


def public_key_gen(k: str):
    k = ecdsa.SigningKey.from_string(unhexlify(k), curve=ecdsa.SECP256k1)
    K = k.get_verifying_key().to_string()
    return hexlify(K)


def account_address_gen(K: str):
    keccak = sha3.keccak_256()
    #keccak_hash = keccak.new(digest_bits=256)
    keccak.update(unhexlify(K))
    print(K)
    hash = keccak.hexdigest()
    # get last 20bytes, the last 40hex
    return '0x' + hash[24:]


def EIP55encode(address: str):
    checksum = ""
    address = address.replace('0x', '')

    keccak = sha3.keccak_256()
    # get the first 40 hex digit that correspond to 20 bytes
    keccak.update(address.encode())
    mask = keccak.hexdigest()[:40]

    for i, digit in enumerate(address):
        if digit in '0123456789':
            # We can't upper-case the decimal digits
            checksum += digit
        elif digit in 'abcdef':
            # Check if the corresponding hex digit in the hash is 8 or higher
            if int(mask[i], 16) > 7:
                checksum += digit.upper()
            else:
                checksum += digit

    return '0x' + checksum


# return True if there are any errors
def detectEIP55errors(address_to_check: str):
    address_to_check = address_to_check.replace('0x', '')
    address_lower_case = address_to_check.lower()

    checksum = EIP55encode(address_lower_case)

    if checksum != address_to_check:
        return True
    else:
        return False


def stub_get_transaction_count(address: str):
    # get number of not pending transaction for that address
    return random.randrange(100)


def contract_account_address_gen(address: str, tx_count: int):
    address = address.replace('0x', '')
    input_for_CA = rlp.encode([unhexlify(address), tx_count])
    keccak = sha3.keccak_256()
    contract_address = keccak.update(input_for_CA).hexdigest()[24:]

    return '0x' + contract_address


if __name__ == "__main__":
    # example of usage
    book_key = b'f8f8a2f43c8376ccb0871305060d7b27b0554d2cc72bccf41b2705608452f315'
    k = private_key_gen()
    K = public_key_gen(k)

    address = account_address_gen(K)
    eip55_address = EIP55encode(address)

    wrong_address = '0x001d3F1ef827552Ae1114027BD3ECF1f086bA0E9'
    if detectEIP55errors(wrong_address):
        print("Error found")
    else:
        print("EIP55 compliant")

    random.seed()
    nonce = stub_get_transaction_count(address)
    contract_address = contract_account_address_gen(address, nonce)

    forum_addr = '0x6ac7ea33f8831ea9dcc53393aaa88b25a785dbf0'
    expected1 = "0x343c43a37d37dff08ae8c4a11544c718abb4fcf8"
    contract1 = contract_account_address_gen(forum_addr, 1)

    if expected1 != contract1:
        print("Error in contract address generation")
