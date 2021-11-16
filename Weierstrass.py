# This script computes a public key on the secp256k1 curve starting from a private key

from typing import Tuple, Optional

Point = Tuple[int, int]

# Public parameters for the secp256k1 curve
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
a = 0


# These two functions return the x-coordinate and the y-coordinate of a point P, respectively
def x(P: Point) -> int:
    return P[0]


def y(P: Point) -> int:
    return P[1]


# This functions sums two points on a Short Weierstrass Elliptic curve: P3 = P1 + P2 = (x3, y3)
# Optional[x] means that the x element can be of type Point or None (in this particular example)
def point_add(P1: Optional[Point], P2: Optional[Point]) -> Optional[Point]:
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    if (x(P1) == x(P2)) and (y(P1) != y(P2)):
        return None
    if P1 == P2:
        lam = ((3 * x(P1)**2 + a) * pow(2 * y(P1), p - 2, p)) % p
    else:
        lam = ((y(P2) - y(P1)) * pow(x(P2) - x(P1), p - 2, p)) % p

    x3 = (lam**2 - x(P1) - x(P2)) % p
    y3 = (lam * (x(P1) - x3) - y(P1)) % p

    return x3, y3


# This function computes the point R = dP = P + ... + P (d times)
def point_mul(d: int, P: Point) -> Point:
    R = None

    for i in range(256):
        if (d >> i) & 1:
            R = point_add(R,P)

        P = point_add(P,P)

    return R


# This function computes a public key starting from a private key
def pubkey_gen(private_key: int) -> Point:
    R = point_mul(private_key, G)
    assert R is not None
    return R









