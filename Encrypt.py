#!/usr/bin/python

import re
import math
from textwrap import wrap

#just maps letters to numbers
#{'A': '00', 'B': '01' ... 'Z': 25 }
def mapper():
    obj = {}
    for i in range(65, 91):
        if i < 74:
            obj[chr(i)] = "0" + str(i - 65)
        else:
            obj[chr(i)] = str(i - 65)
    obj['J'] = '09'
    #obj['+'] = '26'
    return obj

letterMapObj = mapper()
print(letterMapObj)

''' ==============================================
Does as you would expect, strips special characters
and spaces from a given string
============================================== '''

def stripSpacesAndSpecialChars(str):
    resultStr = re.sub('[^a-zA-Z0-9]', '', str)
    return resultStr

def getKeyFromValue(dictObj, value):
    for k, v in dictObj.items():
        if value == v:
            return k


def findGCD(n1, n2):
    a = max(n1, n2)
    b = min(n1, n2)

    if a == b:
        return a

    r, q = 1, 1

    while r != 0:  #while remainder isn't zero
        q = math.floor(a/b)
        r = a - (b * q)
        a = b
        b = r

    return a

def convertLetterToNumber(letter):
    return letterMapObj.get(letter)

def convertLetterBlockToStringNumbers(block):
    str = ""
    for letter in block[0]:
        str += letterMapObj.get(letter)
    return str

def convertStringNumberToActual(strNum):
    return int(strNum)

def convertActualNumberToStringNumber(actualNum):
    actualNum = int(actualNum)
    strNum = str(actualNum)
    zeros = ""
    prependAmt = (8 - len(strNum))
    while prependAmt > 0:
        zeros += "0"
        prependAmt -= 1

    return zeros + strNum

def convertStringNumberToWord(dictObj, strNumber):
    resultStr = ""
    arr = wrap(strNumber, 2)
    for i in range(0, len(arr)):
        resultStr += getKeyFromValue(dictObj, str(arr[i]))
    return resultStr

'''=======================================================
Format the file correctly ex: "a-9b,,,cd eFg" to "ABCDEFG"
also assigns array to contents of plaintext file
======================================================='''
def formatFileToArray(fileName, stripFunc):
    bigArr = []
    file = open(fileName, "r")
    for word in file:
        #strip spaces and special chars if any
        word = stripFunc(word)
        word = word.upper()
        for letter in word:
            bigArr.append(letter)
    file.close()
    return bigArr

'''=======================================================
makes blocks of blocks but are singles. for example
[ ['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H' ]... ] 
now ultimately I want [ ["ABCD"], ["EFGH"] ... ].  That will
be handled in the next function, but I need these to be singles
for now so I can pad and break up blocks correctly, this is why
the function is called ugly.  Also this functions adds the
padding letter,  'A'
======================================================='''
def makeBlocksOfFourUgly(arr, paddingLetter):
    mainArr, block, lastBlock = [], [], []
    blockCount, endingIndex = 0, 0
    for i in range(0, len(arr)):
        block.append(arr[i])
        if(len(block) == 4):
            mainArr.append(block)
            block = []
            blockCount += 1
    endingIndex = ((blockCount * 4))
    while(len(arr) > endingIndex):
        lastBlock.append(arr[endingIndex])
        endingIndex += 1
    while(len(lastBlock) < 4):
        lastBlock.append(paddingLetter)

    allLettersPadding = True
    for i in range(0, len(lastBlock)):
        if(lastBlock[i] != paddingLetter):
            allLettersPadding = False
    if(not allLettersPadding):
        mainArr.append(lastBlock)
    return mainArr

'''=======================================================
turns singles into str chunks as mentioned before
I get [["ABCD"], ["DEFG"]] which is exactly what I want
========================================================'''
def makeBlocksOfFourCorrect(bigBlockArr):
    str = ""
    bigBlock = []
    for i in range(0, len(bigBlockArr)):
        str = ''.join(x for x in bigBlockArr[i])
        bigBlock.append([str])
    return bigBlock

''' =====================================================
encrypts the block, this is where all those conversions
functions come in handy.
======================================================='''
def Encrypt(block, mul, offset):
    stringNumber = convertLetterBlockToStringNumbers(block)
    actualNumber = int(convertStringNumberToActual(stringNumber))
    #C = mP + b(mod 25252526)
    encryptNumber = ((mul * actualNumber) + offset) % 25252526
    return encryptNumber

def writeToCipherFile(fileName, bigBlockOfBlocks, multi, offset):
    cipherNumber = 0
    cipherTextString = ""
    fullCipherTextStrNums = ""
    for i in range(0, len(bigBlockOfBlocks)):
        cipherNumber = Encrypt(bigBlockOfBlocks[i], multi, offset)
        cipherTextString = convertActualNumberToStringNumber(cipherNumber)
        fullCipherTextStrNums += cipherTextString
    file = open(fileName, "w")
    file.write(fullCipherTextStrNums)

fileArr = formatFileToArray("plaintext.txt", stripSpacesAndSpecialChars)
megaBlock = makeBlocksOfFourUgly(fileArr, "A")
megaBlock = makeBlocksOfFourCorrect(megaBlock)

multiplier = input("Input multiplier for block affine cipher ")
multiplier = int(multiplier)

gcd = findGCD(int(multiplier), 25252526)
if(gcd != 1): #is the multilier relatively prime?
    print("The multiplier you entered is not relatively prime")
    print("terminating...")
    exit(0)

offset = input("Enter offset value for cipher ")
offset = int(offset)

writeToCipherFile("cipheroutput.txt", megaBlock, multiplier, offset)











