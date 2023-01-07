"""
References:
https://www.geeksforgeeks.org/python-hash-method/#:~:text=Python%20hash()%20function%20is,while%20looking%20at%20a%20dictionary.
https://www.geeksforgeeks.org/implementation-of-hashing-with-chaining-in-python/
https://docs.python.org/3/library/zlib.html#zlib.crc32
https://www.geeksforgeeks.org/zlib-crc32-in-python/
https://www.geeksforgeeks.org/python-convert-string-to-bytes/
https://stackoverflow.com/questions/20041148/deleting-a-treedata-structure-in-python
https://www.geeksforgeeks.org/insertion-in-an-avl-tree/
https://www.programiz.com/dsa/avl-tree
"""
import random
import bstClass as bst
import pandas as pd
from pandas import DataFrame
from collections import defaultdict
from hashTableClass import DefaultHashTable
from hashTableClass import crc32HashTable
from datetime import datetime

def generateRandomString(n):
    sbstring = "acgt"
    result = ''.join(random.choice(sbstring) for _ in range(n))
    return result

def main():

    dataframes = []
    collisionDataFrames = []
    kSize = [5,6,7]
    nSize = [5**3,10**4,17**5]
    tests = 5
    htb1Time = []
    htb2Time = []
    bstTime = []
    htb1AverageTime = []
    htb2AverageTime = []
    bstAverageTime = []
    htb1Collisions = []
    htb2Collisions = []
    htb1 = DefaultHashTable()
    htb2 = crc32HashTable()
    avl = bst.AVL()

    for size in range(len(kSize)):

        # average time for each size of n
        htb1Mean = 0
        htb2Mean = 0
        bstMean = 0

        # temporary arrays to store time computed
        htb1TimeTemp = []
        htb2TimeTemp = []
        bstTimeTemp = []

        #temporary arrays to store collision count
        htb1CollisionsTemp = []
        htb2CollisionsTemp = []

        for j in range(tests): 

            words = []

            # canvas example 
            #String = "taccaccaccatag"
            #kmerSize = 6
            String = generateRandomString(nSize[size])
            kmerSize = kSize[size]

            for i in range(len(String)-kmerSize+1):
                words.append(String[i:i+kmerSize])

            wordSet = set(words)
            print(len(words) - len(wordSet))

            # creation  and search in default python hash function hashmap
            htb1StartTime = datetime.now()

            for kmer in words:
                htb1.insertData(kmer)

            #for kmer in wordSet:
                #htb1.searchData(kmer)

            htb1End = datetime.now()
            htb1TestTime = (htb1End - htb1StartTime).total_seconds() * 1000
            
            print("The time for default python hash table test #" + str(j+1) + " is: " + str(htb1TestTime) + "\n")
            htb1Mean += htb1TestTime
            htb1TimeTemp.append(htb1TestTime)
            htb1CollisionsTemp.append(htb1.collision)

            # creation  and search in crc32 hash function hashmap
            htb2StartTime = datetime.now()

            for kmer in words:
                htb2.insertData(kmer)

            #for kmer in wordSet:
                #htb2.searchData(kmer)

            htb2End = datetime.now()
            htb2TestTime = (htb2End - htb2StartTime).total_seconds() * 1000

            print("The time for crc32 hash table test #" + str(j+1) + " is: " + str(htb2TestTime) + "\n")
            htb2Mean += htb2TestTime
            htb2TimeTemp.append(htb2TestTime)
            htb2CollisionsTemp.append(htb2.collision)

            # creation  and search in bst implementation
            bstStartTime = datetime.now()

            for kmer in words:
                avl.insert(avl.getRoot(),bst.Node(kmer))

            #for kmer in wordSet:
                #avl.printSearchResult(avl.getRoot(), kmer)

            bstEnd = datetime.now()
            bstTestTime = (bstEnd - bstStartTime).total_seconds() * 1000

            print("The time for bst test #" + str(j+1) + " is: " + str(bstTestTime) + "\n")
            bstMean += bstTestTime
            bstTimeTemp.append(bstTestTime)
            
            # clear all data structures
            htb1.deleteTable()
            htb2.deleteTable()
            avl.deleteTree(avl.getRoot())

        # compute mean for each data structure
        htb1Mean /= tests
        htb2Mean /= tests
        bstMean /= tests

        # add test time to their respective arrays
        htb1Time.append(htb1TimeTemp)
        htb2Time.append(htb2TimeTemp)
        bstTime.append(bstTimeTemp)

        # add mean to their respective arrays
        htb1AverageTime.append(htb1Mean)
        htb2AverageTime.append(htb2Mean)
        bstAverageTime.append(bstMean)

        # add collisions to their respective arrays
        htb1Collisions.append(htb1CollisionsTemp)
        htb2Collisions.append(htb2CollisionsTemp)

    # construct dataframes
    for i in range(len(nSize)):
        dataframes.append(DataFrame({"Python hash": htb1Time[i], "CRC32": htb2Time[i], "BST" : bstTime[i]}))
        collisionDataFrames.append(DataFrame({"Python hash": htb1Collisions[i], "CRC32": htb2Collisions[i]}))

    AverageTimeDf = DataFrame({"Size": nSize, "Python hash": htb1AverageTime , "CRC32": htb2AverageTime, "BST" : bstAverageTime})


    # move to excel file
    filename = "Test Results.xlsx"
    with pd.ExcelWriter(filename) as writer:
        for i in range(len(dataframes)):
            sheetname = "length " + str(nSize[i]) 
            dataframes[i].to_excel(writer, sheet_name= sheetname ,index = False)
            collisionDataFrames[i].to_excel(writer, sheet_name= "Collisions " +sheetname ,index = False)
        AverageTimeDf.to_excel(writer, sheet_name = "Average Time", index = False)
        

if __name__ == "__main__":
    main()
