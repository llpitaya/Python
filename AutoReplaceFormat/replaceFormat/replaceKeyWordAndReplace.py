#!usr/bin/env python

import os
import string
import re
import random
from sys import argv


def RecogizeKeyAndReplace(fileName, pattern, fileNameKeyWord,newDirName):
    assert os.path.exists(fileName), "%s does not exist, please check it." % fileName
    
    relativeFileName = os.path.split(fileName)[1]

    # oldStrTuple[1] and newStrTuple[1] contain directory
    newFileName = relativeFileName.replace(fileNameKeyWord[0], fileNameKeyWord[1])

    # get the new file name
    newFileName = os.path.join(newDirName, newFileName)

        
    oldSrciptFile = open(fileName, 'r')
    newScriptFile = open(newFileName,'w')
            
    keys = pattern.keys()
    for fileLine in oldSrciptFile:
        for i in range(len(keys)):
            if fileLine.find(keys[i])!=-1:
                if keys[i] == "TargetFeatures":
                    fileLine = fileLine.replace("RR=4X,PR=1X,",pattern[keys[i]])
                    break
                else:
                    fileLine = pattern[keys[i]]
                    break
        newScriptFile.write(fileLine)

    oldSrciptFile.close()
    newScriptFile.close()

def ReplaceFiles(fileNameTuple, pattern,fileNameKeyWord):
    xx = range(len(fileNameTuple))
    newDirName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\Results"
    for i in xx:
        RecogizeKeyAndReplace(fileNameTuple[i],pattern,fileNameKeyWord,newDirName)

def replaceFilesInDir(directoryName,pattern,newFileNameKeyWord):
    fileNames = list(os.listdir(directoryName))

    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(directoryName,fileNames[i])

    ReplaceFiles(fileNames,pattern,newFileNameKeyWord)


str1 = "RR=16X,PR=1X,"
str2 = "  Multisample       = 16\n"
oldFileName = r"RR4X_PR1X"
newFileName = r"RR16X_PR1X"
fileNameKeyWord = (oldFileName,newFileName)
dict1 = {"TargetFeatures":str1,"Multisample       =":str2}
directoryName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\initial"
replaceFilesInDir(directoryName,dict1,fileNameKeyWord)