from client import *
from random import randint

from fractions import gcd
NOM='yaker'

urlTp='http://pac.bouillaguet.info/TP5/'
urlPartie = 'RSA-reductions/'





def isqrt(n):
    """ renvoie le plus grand entier k tel que k^2 <= n. Méthode de Newton."""
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def factorN(n,phi):
    res1 = 0
    res2 = 0
    b = n - phi + 1
    sqrt = isqrt(b*b - 4*n)
    res1 = (-b - sqrt) // 2
    res2 = (-b + sqrt) // 2
    return res1,res2

def getTR(k):
    r = k
    t = 1
    while (r % 2) == 0:
        r //= 2
        t += 1
    return t,r
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


def hackPhi(e,d,n):
    k = e * d - 1
    t,r = getTR(k)
    for i in range(1,100):
        g = randint(0,n-1)
        y = pow(g,r,n)
        if (y == 1) or (y == n - 1):
            continue
        x = 0
        for j in range(1,t-1):
            x = y*y % n
            if x == 1:
                p = gcd(y-1,n)
                return p,n//q
            if x == n-1:
                break
            y = x
        if x == n-1:
            continue
    print("pas de facteurs")



if __name__ == "__main__":
    server = Server(base_url=urlTp+urlPartie)
    #Partie phi
    urlChallenge = 'phi/challenge/'+NOM
    start =  server.query(url=urlChallenge)
    phi=start['phi']

    e = start['e']
    n = start['n']
    p,q = factorN(n,phi)
    partiePhi = server.query(url='phi/check/'+NOM,parameters={'p':abs(p)})
    #Partie d
    urlChallenge = 'd/challenge/'+NOM
    start =  server.query(url=urlChallenge)
    e = start['e']
    n = start['n']
    d = start['d']
    p,q=hackPhi(e,d,n)
    print(p)
    print(q)
    # p,q=factorN(n,phi)
    partieD = server.query(url='d/check/'+NOM,parameters={'p':abs(p)})
    print(partieD)
