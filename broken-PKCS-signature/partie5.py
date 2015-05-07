from client import *
from random import randint

from fractions import gcd
NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP5/'
urlPartie = 'broken-PKCS-signature/'


hash_OID= 0x3031300D060960864801650304020105000420


def checkSignature(s,n,e):
    theBytes = list(s)
    index = 0
    while index != 2:
        if theBytes[index] != 0x0001:
            print("echec")
            return False
        index+=1
    i = 0
    print(index)
    while True:
        if theBytes[index] == 0xFF or theBytes[index] == 0x00:
            i+=1
        if i < 7 and (theBytes[index] != 0xFF or theBytes[index] != 0x00):
            break
        index+=1
    index+=1
    print(index)
    if i < 7:
        print("echec")
        return False
    if theBytes[index] != 0x00:
        print("echec")
        return False
    index+=1
    print(index)


if __name__ == "__main__":
    server = Server(base_url=urlTp+urlPartie)
    getPK = server.query(url='/PK')
    n = getPK['n']
    e = getPK['e']
    checkSignature(b'000100000000',n,e)
