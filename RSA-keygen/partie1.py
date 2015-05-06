from client import *
from rsa import *


NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP5/'
urlPartie = 'RSA-keygen/'











if __name__ == "__main__":
    server = Server(base_url=urlTp+urlPartie)
    urlChallenge = 'challenge/'+NOM
    e =  server.query(url=urlChallenge)
    print(e,end="\n\n")
    rsa = RSA(e=e['e'])
    rsa.generateKeys()
    PK = rsa.getPubKey()
    print()
    print("La clé publique : {0}".format(PK))
    SK = rsa.getPrivKey()
    print()
    print("La clé privée : {0}".format(SK))
    n = rsa.getN()
    print("La valeur de N : {0}".format(n))

    enc = rsa.encrypt(42,PK,n)
    print("enc = {0}".format(enc))
    print()
    dec = rsa.decrypt(enc,SK,n)
    print("dec = {0}".format(dec))
    if( dec == 42):
        print("ok")
    else:
        print("ko")
