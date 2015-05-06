from client import *
import hashlib
import base64
from fractions import gcd
from random import randint
NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP5/'
urlPartie = 'id-based-signature/'




def getDigest(m,s):
    hex_s = base64.b16decode(str(s).encode())
    print(hex_s)


def computeI(s,t):
    m_byte = s.encode()
    t_hexa = "{0:0512x}".format(t)
    print(len(t_hexa))
    print(t_hexa)
    t_byte = base64.b16decode(t_hexa, casefold=True)
    print("======")
    tmp = m_byte + t_byte
    hash_obj = hashlib.sha256(tmp).hexdigest()
    return hash_obj



if __name__ == "__main__":
    server = Server(base_url=urlTp+urlPartie)
    #Partie phi
    urlChallenge = 'KDC/PK'
    start =  server.query(url=urlChallenge)
    n = start['n']
    e = start['e']
    getSK = server.query(url='KDC/keygen/'+NOM)
    SK = getSK['secret-key']
    r = randint(1,n-1)
    t = pow(r,e,n)
    res = computeI(NOM,t)

    s = SK*pow(r,int(res,base=16),n) % n
    print(res)
    success = server.query(url='check/'+NOM,parameters={'s':s,'t':t,'m':NOM})
    print(success)
