#!/usr/bin/python

import math
from textwrap import wrap

''' mapper simply maps values to letters
 {'A': '00', 'B': '01' ... 'Z': '25' }
'''

def mapper():
    obj = {}
    for i in range(65, 91):
        if i < 74:
            obj[chr(i)] = "0" + str(i - 65)
        else:
            obj[chr(i)] = str(i - 65)
    obj['J'] = '09'
    obj['+'] = '26'
    return obj

letterMapObj = mapper()
print(letterMapObj)

'''======================================================
Normally you want a value from a dictionary, but this does
the opposite, it asks for a value and gets back a key
ex: key = 'A' value = '00'.  The reason a return '+' is
here is if I don't the program will crash if wrong multipler
or offset was supplied
========================================================'''
def getKeyFromValue(dictObj, value):
    key = ''
    for k, v in dictObj.items():
        if value == v:
            key = k
            break
    return key


'''=========================================================
A gcd calculator so I can determine if relatively prime or not
=========================================================='''
def findGCD(n1, n2):
    a = max(n1, n2)
    b = min(n1, n2)

    if a == b:
        return a

    r, q = 1, 1

    while r != 0:
        q = math.floor(a/b)
        r = a - (b * q)
        a = b
        b = r

    return a

'''============================================================
modified version of the gcd calculator that saves prior values
in order to eventually get the modulo inverse
==========================================================='''
def findModuloInverse(a,b):
    x = 0
    y = 1

    #as with all exteneded gcd's zero will eventually happen
    while a != 0:
        q = math.floor(b/a)
        r = q * y

        priorA = a
        a = b % a
        b = priorA  #swap values to compute q again

        priorY = y
        y = x - r
        x = priorY

    #in case negative modulo get non-negateve reside
    #this while loop will never run if already positve modulo

    while x < 1:
        x = x + 25252526

    return x

#ask for multiler check to see if it is relatively prime
#ie check if gcd = 1
multiplier = input("Input multiplier for block affine cipher to decrypt ")
multipler = int(multiplier)

gcd = findGCD(int(multiplier), 25252526)
if gcd != 1:
    print("The multiplier you entered is not relatively prime")
    print("terminating...")
    exit(0)

offset = input("Enter offset value for cipher ")
offset = int(offset)

modInverse = findModuloInverse(multipler, 25252526)
'''============================================================
using my mapper dictionary convert letter to a number
============================================================'''
def convertLetterToNumber(letter):
    return letterMapObj.get(letter)

'''==========================================================
takes a string number for example string '02114456' -> 2114456
============================================================'''
def convertStringNumberToActual(strNum):
    return int(strNum)

'''===========================================================
does opposite converts actual number to string number
This function also prepends the new string number with zeros if
need be so 12546 -> '00012546' 
============================================================'''
def convertActualNumberToStringNumber(actualNum):
    actualNum = int(actualNum)
    strNum = str(actualNum)
    zeros = ""
    prependAmt = (8 - len(strNum))
    while prependAmt > 0:
        zeros += "0"
        prependAmt -= 1
    return zeros + strNum

'''=============================================================
convert string number to word, uses python's wrapper library for
convience
============================================================='''
def convertStringNumberToWord(dictObj, strNumber):
    resultStr = ""
    arr = wrap(strNumber, 2)
    for i in range(0, len(arr)):
        if int(arr[i]) <= 25:
            resultStr += getKeyFromValue(dictObj, str(arr[i]))
        else:
            resultStr += "00"
    return resultStr

'''===========================================================
get my encrypted block of blocks from file save to an array.
Again, using the wrap library so it will make set of 8 len
string numbers each
==========================================================='''
def getEncryptedBlockOfBlocks(fileName):
    cipherStrNums = ""
    arr = []
    blockOfBlocks = []
    file = open(fileName, "r")
    for word in file:
        cipherStrNums = word

    for i in range(0, len(cipherStrNums)):
        arr = wrap(cipherStrNums, 8)

    #for i in range(0, len(arr)):
        #blockOfBlocks.append([arr[i]])

    return arr

'''================================================================
After obtaining my modular inverse, my multiplication and offset,
I'm now able to decrypt the blocks to plain text.  All my converstion
functions are used here to help me convert to appropriate type before
finally getting my plaintext
================================================================='''
def Decrypt(bigBlock, moduloInverse, offset):
    #C = mP + b(mod 25252526)
    actualNums = 0
    pStringNums = ""
    pStringText = ""
    pResult = ""

    for i in range(0, len(bigBlock)):
        actualNums = int(bigBlockOfBlocks[i])
        actualNums = ((modInverse * (actualNums - offset))) % 25252526
        pStringNums = convertActualNumberToStringNumber(actualNums)
        pStringText = convertStringNumberToWord(letterMapObj, pStringNums)
        pResult += pStringText

    return pResult


bigBlockOfBlocks = getEncryptedBlockOfBlocks("cipheroutput.txt")
Decrypt(bigBlockOfBlocks, modInverse, offset)
plainText = Decrypt(bigBlockOfBlocks, modInverse, offset)

'''===================================================================
This function simply takes the now decypted text and outputs it to the
plaintextoutput.txt file.
==================================================================='''
def writeNewPlainTextFile(fileName):
    file = open(fileName, "w")
    file.write(Decrypt(bigBlockOfBlocks, modInverse, offset))
    file.close()

writeNewPlainTextFile("plaintextoutput.txt")
