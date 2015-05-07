from client import *
from rsa import *
import hashlib
from random import randint
NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP5/'
urlPartie = 'PAC-evaluation/'




p = 151294774789933025072687566708892443277656648381838678428807020127668640168447334520106356365974850510483026003735067529980120302172163936048454623514953870149878034774170184622330925170732983385533237558301854446727014150957375291920538730983905195363229827624535859279379045997068873777234891011559427742593
q = 153143534837305228478060526827261015438292073425849968394132911011788922031145645666781439100633041971898885955456521871419398799793905546075037912727779666871898794021533169868708261615367806141724285120380003554468052133474522998895363636660728840838252257361217149427175609383429734016080268171957234162837


blind_signature = {'blind-signature': 27497602923672477886830485966369263210945185713321524988825488332660023594520134177031923534139964837526505169793929366150314175734488868109201985319937396484918934545560440651306049347204002522783482576734670402553400188481821657651503870788054651486408671389355979512082943219309499312363972710059563326198355730007404525845282770291416592171092241644361997115527265002252059905654699380272374748330520628463234221627293806015494130364099450711879180048815537990515660857224660669209228770783532318459997065235861793741253472207265377183426870894455048591248920422631861619462462240387277694558178253367237857825418}

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m

def peteSignature(x,r,n):
    return x * modinv(r,n) % n

if __name__ == "__main__":
    category= 'GENERAL'
    server = Server(base_url=urlTp+urlPartie)
    getPK = server.query(url='PK')
    submission = getPK['submission']
    avis=submission[category]

    receipt = getPK['receipt']
    s = 41062873402#(str(randint(1,125697866022)))

    m = int(hashlib.sha256(str(s).encode()).hexdigest(),base=16)

    r = randint(2,avis['n'])

    rsa = RSA(e=529810294338137046962892494092996176509,p=p,q=q)
    #rsa = RSA(e=e)
    PK = rsa.getPubKey()

    # print("La clé publique : {0}".format(PK))
    SK = rsa.getPrivKey()
    # print()
    # print("La clé privée : {0}".format(SK))
    n = rsa.getN()

    blinded = pow(r,avis['e'],avis['n'])*m % avis['n']
    signBlinded = rsa.decrypt(c=blinded,SK=SK)
    print(signBlinded)
    print(blinded)
    #dictSign = {'category':category,'blinded':blinded,'signature':signBlinded}
    # resSign = server.query(url='publication-token/'+NOM,parameters=dictSign)
    # print(resSign)
    print(peteSignature(blind_signature['blind-signature'],r,avis['n']))
