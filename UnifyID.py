import urllib2
import sympy
import math
import fractions

def requestBuilder(minimum, maximum):
    """
    Builds a request with all the necessary parameters.
    """
    randomIntegerOrg = 'https://www.random.org/integers/'
    parameters = '?num=1&min=' + str(minimum) + '&max=' + str(maximum)
    format = '&format=plain&rnd=new&col=1&base=10'
    return randomIntegerOrg + parameters + format

def getRandomNumber(minimum, maximum):
    """
    Generates one random number in the range between min and max.
    """
    requestParam = requestBuilder(minimum, maximum)
    print(requestParam)
    request = urllib2.Request(requestParam)
    try:
        randomNumber = urllib2.build_opener().open(request).read()
    except urllib2.HTTPError as e:
        print(e)
    return int(randomNumber)

def getPrimeRandoms(minimum, maximum):
    """
    Finds two distinct primes p and q.
    Returns them as a list (twoDistinctPrimes).
    """
    twoDistinctPrimes = []
    while len(twoDistinctPrimes) < 2:
        randomNumber = getRandomNumber(minimum, maximum)
        if sympy.isprime(randomNumber) and randomNumber not in twoDistinctPrimes:
            twoDistinctPrimes.append(randomNumber)
    return twoDistinctPrimes

def computePublicKeyPair():
    """
    Finds a public key pair (e, n) where n = p*q and
    gcd(e, (p-1)(q-1)) = 1. e is called publicKey in
    the code. Returns, [e, n, totient]
    """
    publicKeyPair = []
    distincRandoms = getPrimeRandoms(2**14, 2**15-1)
    p, q = int(distincRandoms[0]), int(distincRandoms[1])
    n = p*q
    totient = (p-1)*(q-1)
    publicKeyCandidate = getRandomNumber(2, n)
    while fractions.gcd(publicKeyCandidate, totient) != 1:
        publicKeyCandidate = getRandomNumber(2, n)
    publicKey = publicKeyCandidate

    return [publicKey, n, totient]


"""
The following two functions are copied from
(gcd, findModInverse)
# Cryptomath Module
# http://inventwithpython.com/hacking (BSD Licensed)
"""
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1
    if gcd(a, m) != 1:
        return None # no mod inverse if a & m aren't relatively prime
    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def computeRSAKeyPair():
    """
    Finds a private key pair (d, n) where n = p*q and
    de conj 1 mod((p-1)(q-1)). d is called privateKey
    in the code.
    Returns an RSA Key Pair in the form of
    [[public key pair], [private key pair]].
    """
    publicKeyPair = computePublicKeyPair()
    e = publicKeyPair[0]
    n = publicKeyPair[1]
    totient = publicKeyPair[2]
    privateKey = findModInverse(e, totient)

    return [(publicKeyPair[0], n), (privateKey, n)]

print computeRSAKeyPair()
