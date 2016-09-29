# playfairCipher.py
# chapter 3 programming practice exercises.
# This program encrypts and decrypts messages using the playfair cipher.



# Helper Functions

def removeSpaces(message):
    ''' Takes a string as input and returns the same string with spaces removed.'''
    newMessage = ''
    for ch in message:
        if ch != ' ':
            newMessage += ch
    return newMessage



def removeDupes(message):
    ''' Takes a string as input and returns a new string with all duplicate letters removed.'''
    message = message.lower()
    newMessage = ''
    for ch in message:
        if ch not in newMessage:
            newMessage += ch
    return newMessage



def trimAlphabet(message):
    ''' Takes a string as input, removes duplicates from the string, returns a string with
    all letters of the alphabet excluding those letters in the message.'''
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    message = message.lower()
    newMessage = removeDupes(message)
    newAlphabet = ''
    
    for ch in alphabet:
        if ch not in newMessage and ch != 'q':
            newAlphabet += ch
            
    return newAlphabet



def buildEmptyTable(n):
    ''' Builds a list of n empty lists'''
    
    table = []
    for i in range(n):
        table.append([])
    return table    



def buildKeyTable(keyWord):
    ''' Builds the playfair key table from the key word.'''
    
    # remove spaces, duplicates from keyword
    keyWord = removeDupes(keyWord)
    keyWord = removeSpaces(keyWord)
    
    # set-up the empty 5 by 5 table
    keyTable = buildEmptyTable(5)
    
    # fill-in the key table with keyword values
    i = 0
    for i in range(len(keyWord)):
        row = i // 5
        keyTable[row].append(keyWord[i])
        i += 1
        
    # fill-in the key table with alphabet values
    trimmedAlpha = trimAlphabet(keyWord)
    
    for ch in trimmedAlpha:
        row = i // 5
        keyTable[row].append(ch)
        i += 1
    
    return keyTable



def fixConsecutive(message):
    '''Fixes issue with consecutive letters by adding an x after the first instance of a duplicate.'''

    newMessage = message[0]
    i = 1
    while i < len(message):
        if message[i] == message[i - 1]:
            newMessage += 'x'
            newMessage += message[i]
        else:
            newMessage += message[i]
        i += 1
    
    return newMessage
        


def createDigrams(message):
    '''Convert the message to a list of digrams to use with the key table for encryption.'''
    message = removeSpaces(message)
    message = fixConsecutive(message)
    digramList = []
    
    # if odd number of characters, add initials to make it even
    if len(message) % 2 == 1:
        message = message + 'rwb'
    
    # add digrams as lists to the master digram list
    lowBound = 0
    highBound = 2
    while highBound < len(message) + 1:
        thisDigram = [message[lowBound:highBound]]
        digramList.append(thisDigram)
        lowBound += 2
        highBound += 2
    
    return digramList



# Encryption Functions

def sameRowEnc(digram, keyTable):
    '''Takes a list digram and list keyTable as input.
    Returns the digram's replacement letters from the keyTable.
    Apply this function when digram letters are in the same row.'''
    
    digramText = digram[0].lower()
    
    cipherLetter1 = ''
    cipherLetter2 = ''
    
    for i in range(len(keyTable)):
        for j in range(len(keyTable[i])):
            if keyTable[i][j] == digramText[0]:                
                cipherLetter1 = keyTable[i][(j + 1) % 5]
            elif keyTable[i][j] == digramText[1]:
                cipherLetter2 = keyTable[i][(j + 1) % 5]
    
    return cipherLetter1 + cipherLetter2
    
                

def sameColEnc(digram, keyTable):
    '''Takes a list digram and list keyTable as input.
    Returns the digram's replacement letters from the keyTable.
    Apply this function when digram letters are in the same column.'''
        
    digramText = digram[0].lower()
    
    cipherLetter1 = ''
    cipherLetter2 = ''
    
    for i in range(len(keyTable)):
        for j in range(len(keyTable[i])):
            if keyTable[i][j] == digramText[0]:                
                cipherLetter1 = keyTable[(i + 1) % 5][j]
            elif keyTable[i][j] == digramText[1]:
                cipherLetter2 = keyTable[(i + 1) % 5][j]
    
    return cipherLetter1 + cipherLetter2    



def diffRowColEnc(digram, keyTable):
    '''Takes a list digram and list keyTable as input.
    Returns the digram's replacement letters from the keyTable.
    Apply this function when digram letters are in different columns and rows.'''
           
    digramText = digram[0].lower()
    
    cipherLetter1 = ''
    cipherLetter2 = ''
    cipherPoint1 = ()
    cipherPoint2 = ()
    
    # capture the two known points
    for i in range(len(keyTable)):
        for j in range(len(keyTable[i])):
            if keyTable[i][j] == digramText[0]:                
                cipherPoint1 = (i, j)
            elif keyTable[i][j] == digramText[1]:
                cipherPoint2 = (i, j)
            
    cipherLetter1 = keyTable[(cipherPoint1[0] + 1) % 5][(cipherPoint2[1] + 1) % 5]
    cipherLetter2 = keyTable[(cipherPoint2[0] + 1) % 5][(cipherPoint1[1] + 1) % 5]
    
    return cipherLetter1 + cipherLetter2    
    



def cipherGram(digram, tablePoints, keyword):
    '''Takes a list of tuples for the points in the keyTable that match
    the letters in a digram.  Determines if they share the same row or column (or neither),
    and returns the corresponding cipher string.'''
    
    keyTable = buildKeyTable(keyword)
    cipherDigram = ''
    
    point1Row = tablePoints[0][0]
    point1Col = tablePoints[0][1]
    point2Row = tablePoints[1][0]
    point2Col = tablePoints[1][1]
    
    if point1Row == point2Row:
        cipherDigram = sameRowEnc(digram, keyTable)
    elif point1Col == point2Col:
        cipherDigram = sameColEnc(digram, keyTable)
    elif point1Row != point2Row and point1Col != point2Col:
        cipherDigram = diffRowColEnc(digram, keyTable)
    
    return cipherDigram
        
        


def playfairEncrypt(message, keyword):
    '''Takes the message and keywords as inputs.  Encrypts the message.'''
    
    keyTable = buildKeyTable(keyword)
    digrams = createDigrams(message)
    
    cipherText = ''
    
    for item in digrams:
        digramText = item[0].lower()
        cipherCol1 = 0
        cipherRow1 = 0
        cipherCol2 = 0
        cipherRow2 = 0
    
        for i in range(len(keyTable)):
            for j in range(len(keyTable[i])):
                if keyTable[i][j] == digramText[0]:                
                    cipherCol1 = j
                    cipherRow1 = i
                elif keyTable[i][j] == digramText[1]:
                    cipherCol2 = j
                    cipherRow2 = i
                
        tablePoints = [(cipherRow1, cipherCol1), (cipherRow2, cipherCol2)]
        cipherDigram = cipherGram(item, tablePoints, keyword)
        
        cipherText += cipherDigram
        
    return cipherText



# Decryption Functions

def sameRowDec(digram, keyTable):
    '''Takes a list digram and list keyTable as input.
    Returns the digram's replacement letters from the keyTable.
    Apply this function when digram letters are in the same row.'''
    
    digramText = digram[0].lower()
    
    plainLetter1 = ''
    plainLetter2 = ''
    
    for i in range(len(keyTable)):
        for j in range(len(keyTable[i])):
            if keyTable[i][j] == digramText[0]:                
                plainLetter1 = keyTable[i][(j - 1) % 5]
            elif keyTable[i][j] == digramText[1]:
                plainLetter2 = keyTable[i][(j - 1) % 5]
    
    return plainLetter1 + plainLetter2



def sameColDec(digram, keyTable):
    '''Takes a list digram and list keyTable as input.
    Returns the digram's replacement letters from the keyTable.
    Apply this function when digram letters are in the same column.'''
        
    digramText = digram[0].lower()
    
    plainLetter1 = ''
    plainLetter2 = ''
    
    for i in range(len(keyTable)):
        for j in range(len(keyTable[i])):
            if keyTable[i][j] == digramText[0]:                
                plainLetter1 = keyTable[(i - 1) % 5][j]
            elif keyTable[i][j] == digramText[1]:
                plainLetter2 = keyTable[(i - 1) % 5][j]
    
    return plainLetter1 + plainLetter2    



def diffRowColDec(digram, keyTable):
    '''Takes a list digram and list keyTable as input.
    Returns the digram's replacement letters from the keyTable.
    Apply this function when digram letters are in different columns and rows.'''
           
    digramText = digram[0].lower()
    
    plainLetter1 = ''
    plainLetter2 = ''
    plainPoint1 = ()
    plainPoint2 = ()
    
    # capture the two known points
    for i in range(len(keyTable)):
        for j in range(len(keyTable[i])):
            if keyTable[i][j] == digramText[0]:                
                plainPoint1 = (i, j)
            elif keyTable[i][j] == digramText[1]:
                plainPoint2 = (i, j)
            
    plainLetter1 = keyTable[(plainPoint1[0] - 1) % 5][(plainPoint2[1] - 1) % 5]
    plainLetter2 = keyTable[(plainPoint2[0] - 1) % 5][(plainPoint1[1] - 1) % 5]
    
    return plainLetter1 + plainLetter2 



def plainGram(digram, tablePoints, keyword):
    '''Takes a list of tuples for the points in the keyTable that match
    the letters in a digram.  Determines if they share the same row or column (or neither),
    and returns the corresponding cipher string.'''
    
    keyTable = buildKeyTable(keyword)
    plainDigram = ''
    
    point1Row = tablePoints[0][0]
    point1Col = tablePoints[0][1]
    point2Row = tablePoints[1][0]
    point2Col = tablePoints[1][1]
    
    if point1Row == point2Row:
        plainDigram = sameRowDec(digram, keyTable)
    elif point1Col == point2Col:
        plainDigram = sameColDec(digram, keyTable)
    elif point1Row != point2Row and point1Col != point2Col:
        plainDigram = diffRowColDec(digram, keyTable)
    
    return plainDigram
        


def playfairDecrypt(cipherText, keyword):
    '''Takes the message and keywords as inputs.  Encrypts the message.'''
    
    keyTable = buildKeyTable(keyword)
    digrams = createDigrams(cipherText)
    
    plainText = ''
    
    for item in digrams:
        digramText = item[0].lower()
        plainCol1 = 0
        plainRow1 = 0
        plainCol2 = 0
        plainRow2 = 0
    
        for i in range(len(keyTable)):
            for j in range(len(keyTable[i])):
                if keyTable[i][j] == digramText[0]:                
                    plainCol1 = j
                    plainRow1 = i
                elif keyTable[i][j] == digramText[1]:
                    plainCol2 = j
                    plainRow2 = i
                
        tablePoints = [(plainRow1, plainCol1), (plainRow2, plainCol2)]
        plainDigram = plainGram(item, tablePoints, keyword)
        
        plainText += plainDigram
        
    return plainText
  
    

def main():
    message = 'The Fox Jumped Over the Bridge'
    keyword = 'dogfight'
    encMessage = playfairEncrypt(message, keyword)
    decMessage = playfairDecrypt(encMessage, keyword)
    print("Encrypted Message:", encMessage)
    print("Decrypted Message:", decMessage)
    

main()







