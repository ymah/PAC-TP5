from fractions import gcd
import random
import math


class RSA:


        def __init__(self,e=1,p=1,q=1,iNumBits=2048,iConfidence=32):
                self.__e=e
                self.__p=p
                self.__q=q
                self.__iNumBits=iNumBits
                self.__iConfidence = iConfidence
                self.__indicatrice = 1
                self.__n = self.__p*self.__q
                self.__d = self.modinv(self.__e,self.__indicatrice)


        def modinv(self,a, m):
                g, x, y = self.extended_gcd(a, m)
                if g != 1:
                        raise ValueError
                return x % m

        def extended_gcd(self,aa, bb):
                lastremainder, remainder = abs(aa), abs(bb)
                x, lastx, y, lasty = 0, 1, 1, 0
                while remainder:
                        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
                        x, lastx = lastx - quotient*x, x
                        y, lasty = lasty - quotient*y, y
                return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)




        def fermatTest(self,N):
                for i in range(2, N-1):
                        if N % i == 0:
                                return False
                        else:
                                return True

        def find_prime(self,iNumBits, iConfidence):
                #keep testing until one is found
                while(1):
                        #generate potential prime randomly
                        p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
                        #make sure it is odd
                        while( p % 2 == 0 ):
                                p = random.randint(2**(iNumBits-2),2**(iNumBits-1))

                        #keep doing this if the solovay-strassen test fails
                        while( not self.fermatTest(p) ):
                                p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
                                while( p % 2 == 0 ):
                                        p = random.randint(2**(iNumBits-2), 2**(iNumBits-1))
                        #if p is prime cryptptompute p = 2*p + 1
                        #if p is prime, we have succeeded; else, start over
                        p = p * 2 + 1
                        if self.fermatTest(p):
                                return p
                        else:
                                find_prime(iNumBits,iConfidence+1)


        def checkRandNum(self):
                if(self.__p == self.__q):
                        print("Echec de choix de p et q")
                        return False
                print("p different de q")
                if(self.__d.bit_length() != self.__iNumBits):
                        print("Echec de longeur de d")
                        return False
                print("longeur de d correcte")
                if((self.__n).bit_length() != self.__iNumBits ):
                        print("Echec de longeur de n")
                        return False
                print("longeur de n correcte")
                testED = self.modinv(self.__e*self.__d,self.__indicatrice)
                if testED == 1:
                        print("e*d egaux à 1  modulo phi")
                        if gcd(self.__indicatrice,self.__e) == 1:
                                print("e et d respectent les regles")
                                return True
                print("Echec Total")
                return False


        def generateKeys(self):
                while not self.checkRandNum() :
                        print('-> Nouvelle tentative')
                        self.__p = self.find_prime(self.__iNumBits//2, self.__iConfidence)
                        self.__q = self.find_prime(self.__iNumBits//2, self.__iConfidence)
                        self.__n = self.__p * self.__q
                        self.__indicatrice = (self.__p - 1) * (self.__q - 1)
                        self.__d = self.modinv(self.__e,self.__indicatrice)

        def getPubKey(self):
                return self.__n

        def getPrivKey(self):
                return self.__d

        def getN(self):
                return self.__n
        def modpow(self,base, exponent, mod):
        #Computes base^exponent mod mod using repeated squaring
                ans = 1
                index = 0
                while(1 << index <= exponent):
                        if(exponent & (1 << index)):
                                ans = (ans * base) % mod
                        index += 1
                        base = (base * base) % mod
                return ans

        def modexp(self,m,p,n):
                return self.modpow(m,p,n)


        def encrypt(self,m,PK=None,n=None):
                res = 0
                if PK == None:
                        if n == None:
                                res = self.modexp(m,self.__e,self.__n)
                        else:
                                res = self.modexp(m,self.__e,n)
                else:
                        if n == None:
                                res = self.modexp(m,PK,self.__n)
                        else:
                                res = self.modexp(m,PK,n)
                return res

        def decrypt(self,c,SK=None,n=None):
                res = 0
                if SK == None:
                        if n == None:
                                res = self.modexp(c,self.__d,self.__n)
                        else:
                                res = self.modexp(c,self.__d,n)
                else:
                        if n == None:
                                res = self.modexp(c,SK,self.__n)
                        else:
                                res = self.modexp(c,SK,n)
                return res
