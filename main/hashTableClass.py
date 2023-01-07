import zlib
from nodeClass import node

"""
Hashing algorithms the python default and crc32
Uses linear probing for default python hashtable
Uses quadratic probing for crc32 python hashtable
"""
class HashTable:
    # initialize an empty dictionary, its hashing algo, and # of collisions
    def __init__(self):
        self.table = {}
        self.collision = 0

    # prints the address and items including the number of collisions made during insertion
    def printTable(self):
        if(len(self.table) > 0):
            print("Collisions during insertion " + str(self.collision))
        for i,v in self.table.items():
            print("Address: " + str(i))
            print(v.kmer,v.frequency)

    # clear the dictionary and reset collision count
    def deleteTable(self):
        self.collision = 0
        self.table.clear()

class DefaultHashTable(HashTable):

    def __init__(self):
        super().__init__()
    
    # inserts data to hashtable
    def insertData(self,text):

        #if default just hash using python builit in hashing function
        hashedValue = hash(text)

        # first time seeing the address
        if hashedValue not in self.table.keys():
            self.table[hashedValue] = node(text)
            
        # if collision occurs
        else:
            self.collision += 1
            while hashedValue in self.table.keys():
                if(self.table[hashedValue].kmer == text):
                    self.table[hashedValue].frequency += 1
                    return
                else:
                    hashedValue += 1
            self.table[hashedValue] = node(text)
    
    def searchData(self,text):

        #if default just hash using python builit in hashing function
        hashedValue = hash(text)

        while(hashedValue in self.table.keys()):
            # if data is the same just increment
            if(self.table[hashedValue].kmer == text):
                print("Found " + text + " at address " + str(hashedValue) + " it has a frequency of " + str(self.table[hashedValue].frequency))
                return
            hashedValue += 1
        print(text + " is Not found in table")
        return

class crc32HashTable(HashTable):
    def __init__(self):
        super().__init__()

    # algorithm to convert string to byte and use crc32 hash 
    def crc32Hash(self,text):
        byteString = text.encode('utf-8')
        return zlib.crc32(byteString)

    # inserts data to hashtable
    def insertData(self,text):

        #if crc32 convert to byte since it needs a byte string not a regular string
        hashedValue = self.crc32Hash(text)

        # first time seeing the address
        if hashedValue not in self.table.keys():
            self.table[hashedValue] = node(text)
            
        # if collision occurs
        else:
            quadraticProbe = 1
            self.collision += 1
            while hashedValue in self.table.keys():
                if(self.table[hashedValue].kmer == text):
                    self.table[hashedValue].frequency += 1
                    return
                else:
                    hashedValue += quadraticProbe ** 2
                    quadraticProbe += 1
            self.table[hashedValue] = node(text)
    
    def searchData(self,text):

        #if crc32 convert to byte since it needs a byte string not a regular string
        hashedValue = self.crc32Hash(text)
        quadraticProbe = 1
        while(hashedValue in self.table.keys()):
            # if data is the same just increment
            if(self.table[hashedValue].kmer == text):
                print("Found " + text + " at address " + str(hashedValue) + " it has a frequency of " + str(self.table[hashedValue].frequency))
                return
            hashedValue += quadraticProbe ** 2
            quadraticProbe += 1
        print(text + " is Not found in table")
        return