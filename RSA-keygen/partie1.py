from client import *
from rsa import *


NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP5/'
urlPartie = 'RSA-keygen/'











if __name__ == "__main__":
    server = Server(base_url=urlTp+urlPartie)
    urlChallenge = 'challenge/'+NOM
    e =  server.query(url=urlChallenge)
    rsa = RSA(e=e['e'])
    rsa.generateKeys()
    PK = rsa.getPubKey()
    # print()
    # print("La clé publique : {0}".format(PK))
    SK = rsa.getPrivKey()
    # print()
    # print("La clé privée : {0}".format(PK))
    print()
    enc = rsa.encrypt(42)
    print(enc)
    dec = rsa.decrypt(enc)
    print(dec)
    if( dec == 42):
        print("ok")
    else:
        print("ko")
