#Questo script calcolerà chiavi pubbliche per una curva in forma di Weierstrass a partire da una chiave privata

#import typing
from typing import Tuple, Optional

Point = Tuple[int,int]

#Parametri pubblici per la curva secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
a = 0
#a = 7
#p = 13
#n = 11
#G = (5,6)


#Queste due funzioni restituiscono la coordinata x e y di un punto di una curva (rispettivamente)
def x(P : Point) -> int:
    return P[0]

def y(P):
    return P[1]

#Questa funzione somma due punti di una curva ellittica, cioè ci restituisce P3 = P1 + P2 = (x3, y3)
#Optional[x] significa che l'elemento x  a cui ci si sta riferendo è di tipo Point OPPURE None
def point_add(P1 : Optional[Point], P2 : Optional[Point]) -> Optional[Point]:
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

#Questa funzione calcola il punto R = dP
def point_mul(d : int, P : Point) -> Point:
    R = None

    for i in range(256):
        if (d >> i) & 1:
            R = point_add(R,P)

        P = point_add(P,P)

    return R

#Questa funzione restituisce una chiave pubblica a partire da una chiave privata
def pubkey_gen(private_key : int) -> Point:
    R = point_mul(private_key, G)

    assert R is not None
    return R









