from fractions import gcd
import random
import math
import sys

class RSA:


        def __init__(self,e=1,p=1,q=1,iNumBits=2048,iConfidence=32):
                self.__e=e
                self.__p=p
                self.__q=q
                self.__iNumBits=iNumBits
                self.__iConfidence = iConfidence
                self.__indicatrice = (self.__p - 1) * (self.__q - 1)
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



        def rabin_miller(self,p):
                if(p<2):
                        return False
                if(p!=2 and p%2==0):
                        return False
                s=p-1
                while(s%2==0):
                        s = s>>1
                for i in range(10):
                        a=random.randrange(p-1)+1
                        temp=s
                        mod=pow(a,temp,p)
                        while(temp!=p-1 and mod!=1 and mod!=p-1):
                                mod=(mod*mod)%p
                                temp=temp*2
                        if(mod!=p-1 and temp%2==0):
                                return False
                return True

        def fermatTest(self,N):
                for i in range(2, N-1):
                        if N % i == 0:
                                return False
                        else:
                                return True

        def find_prime(self,iNumBits, iConfidence):
                #keep testing until one is found
                while(1):
                        p = random.randint( 2**(iNumBits-1), 2**(iNumBits) )
                        while( not self.rabin_miller(p) ):
                                p = random.randint( 2**(iNumBits-1), 2**(iNumBits) )
                                print('.',end='')
                                while( p % 2 == 0 ):
                                        print('+',end='')
                                        p = random.randint(2**(iNumBits-1), 2**(iNumBits))
                        #if p is prime cryptptompute p = 2*p + 1
                        #if p is prime, we have succeeded; else, start over
                        # print("Almost found...")
                        # p = p * 2 + 1
                        # if self.rabin_miller(p):
                        print("Found !!!")
                        return p
                        # else:
                        #         print("oh crap !!")
                        #         self.find_prime(iNumBits,iConfidence+1)


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
                        if self.__p == 1:
                                self.__p = self.find_prime(self.__iNumBits//2, self.__iConfidence)
                        if self.__q == 1:
                                self.__q = self.find_prime(self.__iNumBits//2, self.__iConfidence)
                        self.__n = self.__p * self.__q
                        self.__indicatrice = (self.__p - 1) * (self.__q - 1)
                        self.__d = self.modinv(self.__e,self.__indicatrice)
                print(self.__p,end="\n\n")
                print(self.__q,end="\n\n")
                print(self.__p*self.__q,end="\n\n")

        def getPubKey(self):
                return self.__e

        def getPrivKey(self):
                return self.__d

        def getN(self):
                return self.__n

        def modexp(self,m,p,n):
                return pow(m,p,n)


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
