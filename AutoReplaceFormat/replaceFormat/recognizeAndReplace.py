#!usr/bin/env python

import os
import string
from sys import argv

def ReplaceStr(fileLine, oldStr, newStr):
    if fileLine.find(oldStr) != -1:
        # log info
        logFile.write("%s%s" % (fileLine,'\n'))

        fileLine = fileLine.replace(oldStr, newStr)

        # log info
        logFile.write("%s%s" % (fileLine,'\n'))
    return fileLine

def ReplaceStrInFile(fileName,oldStrTuple, newStrTuple):
    assert os.path.exists(fileName), "%s does not exist, please check it." % fileName\
    
    # 对文件名进行重新命名
    dirName = os.path.split(fileName)[0]
    relativeFileName = os.path.split(fileName)[1]
    
    # log info
    logFile.write("%s%s" % (relativeFileName,'\n'))

    # oldStrTuple[0] and newStrTuple[0] contain directory
    newDirName = dirName.replace(oldStrTuple[1], newStrTuple[1])

    # oldStrTuple[1] and newStrTuple[1] contain directory
    newFileName = relativeFileName.replace(oldStrTuple[0], newStrTuple[0])
    
    # get the new file name
    newFileName = os.path.join(newDirName, newFileName)

    # log info
    logFile.write("%s%s" % (newFileName,'\n'))

    fobjOld = open(fileName, 'r')
    fobjNew = open(newFileName, 'w')
    
    for fileLine in fobjOld:
        #  replaced words are placed  in the oldSrTuple beginning with index 2
        for i in range(2, len(oldStrTuple)):
            fileLine = ReplaceStr(fileLine, oldStrTuple[i], newStrTuple[i])
        fobjNew.write('%s' % fileLine)
 
    # close opened files
    fobjOld.close()
    fobjNew.close()

def ReplaceFiles(fileNameTuple, oldStrTuple, newStrTuple):
    xx = range(len(fileNameTuple))
    for i in xx:
        logFile.write("%s%s" % (commentStr,'\n'))
        ReplaceStrInFile(fileNameTuple[i], oldStrTuple, newStrTuple)
        logFile.write("%s%s" % (commentStr, '\n'))


def ReplaceFilesInDir(directoryName, oldStrTupleFile, newStrTupleFile):
    assert os.path.exists(directoryName), "%s does not exist, please check it." % directoryName
    assert os.path.exists(oldStrTupleFile), "%s does not exist, please check it." % oldStrTupleFile
    assert os.path.exists(newStrTupleFile), "%s does not exist, please check it." % newStrTupleFile

    fileNames = list(os.listdir(directoryName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(directoryName,fileNames[i])
    
    lineNumber = len(open(oldStrTupleFile,'rU').readlines())
    
    oldStrFile = open(oldStrTupleFile, 'r')
    newStrFile = open(newStrTupleFile, 'r')
    for i in range(lineNumber):
        oldStrTuple = oldStrFile.readline().split(',')
        newStrTuple = newStrFile.readline().split(',')
        ReplaceFiles(fileNames, oldStrTuple, newStrTuple)

    oldStrFile.close()
    newStrFile.close()

# if __name__ == '__main__':

directoryName   = "C:\\Users\\PitayaLi\\Desktop\\Blending\\initial"
oldStrTupleFile = "C:\\Users\\PitayaLi\\Desktop\\Blending\\oldStr.txt"
newStrTupleFile = "C:\\Users\\PitayaLi\\Desktop\\Blending\\newStr.txt"
logFile = open("info.log",'w')
commentStr = "---------------------------------------------------------------\n"
ReplaceFilesInDir(directoryName, oldStrTupleFile, newStrTupleFile)
logFile.close()
