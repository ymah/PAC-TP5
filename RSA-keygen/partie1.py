from client import *
from rsa import *


NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP5/'
urlPartie = 'RSA-keygen/'











if __name__ == "__main__":
    server = Server(base_url=urlTp+urlPartie)
    urlChallenge = 'challenge/'+NOM
    getE =  server.query(url=urlChallenge)
    print(getE,end="\n\n")
    e = getE['e']
    p = 151294774789933025072687566708892443277656648381838678428807020127668640168447334520106356365974850510483026003735067529980120302172163936048454623514953870149878034774170184622330925170732983385533237558301854446727014150957375291920538730983905195363229827624535859279379045997068873777234891011559427742593
    q = 153143534837305228478060526827261015438292073425849968394132911011788922031145645666781439100633041971898885955456521871419398799793905546075037912727779666871898794021533169868708261615367806141724285120380003554468052133474522998895363636660728840838252257361217149427175609383429734016080268171957234162837
    rsa = RSA(e=e,p=p,q=q)
    #rsa = RSA(e=e)
    rsa.generateKeys()
    PK = rsa.getPubKey()
    print()
    # print("La clé publique : {0}".format(PK))
    SK = rsa.getPrivKey()
    # print()
    # print("La clé privée : {0}".format(SK))
    n = rsa.getN()
    # print("La valeur de N : {0}".format(n))
    print(n)
    urlKey='PK/'+NOM
    dictKey={'n':n,'e':e}
    getCipher = server.query(url=urlKey,parameters=dictKey)
    cipher = getCipher['ciphertext']
    plain = rsa.decrypt(c=cipher)
    solution = {'m':plain}
    resFinal = server.query(url='confirmation/'+NOM,parameters=solution)
    print(resFinal)
