from fractions import gcd
import random
import math



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



class RSA:


    def __init__(self,e=1,p=1,q=1,iNumBits=2048,iConfidence=32):
        self.__e=e
        self.__p=p
        self.__q=q
        self.__iNumBits=iNumBits
        self.__iConfidence = iConfidence
        self.__indicatrice = 0
        self.__n = 0
        self.__d = 0


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

            #if p is prime compute p = 2*p + 1
            #if p is prime, we have succeeded; else, start over
            p = p * 2 + 1
            if self.fermatTest(p):
                return p

    def checkRandNum(self):
        if(self.__p == self.__q):
            return False
        if((self.__p*self.__q).bit_length() != self.__iNumBits ):
            return False
        if gcd(self.__indicatrice,self.__e) == 1:
            return True
        return False


    def generateKeys(self):
        #p is the prime
        #g is the primitve root
        #x is random in (0, p-1) inclusive
        #h = g ^ x mod p
        while not self.checkRandNum() :
            print('.',end="")
            self.__p = self.find_prime(self.__iNumBits//2, self.__iConfidence)
            self.__q = self.find_prime(self.__iNumBits//2, self.__iConfidence)
            self.__indicatrice = (self.__p - 1)*(self.__q - 1)
            self.__n = self.__p * self.__q
            self.__d = modinv(self.__e,self.__indicatrice)

    def getPubKey(self):
        return self.__p * self.__q

    def getPrivKey(self):
        return self.__d

    def modexp( self, base, exp, modulus ):
        return pow(base, exp, modulus)

    def encrypt(self,m):
        return self.modexp(m,self.__e,self.__n)

    def decrypt(self,c):
        return self.modexp(c,self.__d,self.__n)
