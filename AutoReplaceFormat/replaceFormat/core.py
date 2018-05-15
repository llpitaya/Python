#!usr/bin/env python

import os
import string
from sys import argv

def ReplaceStr(fileLine, oldStr, newStr):
    if fileLine.find(oldStr) != -1:
        logFile.write("%s%s" % (fileLine,'\n'))
        fileLine = fileLine.replace(oldStr, newStr)
        logFile.write("%s%s" % (fileLine,'\n'))
    return fileLine

def ReplaceStrInFile(fileName,oldStrTuple, newStrTuple):
    assert os.path.exists(fileName), "%s does not exist, please check it." % fileName
    fobjOld = open(fileName, 'r')
    
    #对文件名进行重新命名
    dirName = os.path.split(fileName)[0]
    relativeFileName = os.path.split(fileName)[1]
    
    logFile.write("%s%s" % (relativeFileName,'\n'))

    newFileName = relativeFileName.replace(oldStrTuple[0], newStrTuple[0])
    # newFileName = newFileName.replace(oldStrTuple[1], newStrTuple[1])
    newFileName = os.path.join(dirName, newFileName)

    logFile.write("%s%s" % (newFileName,'\n'))

    fobjNew = open(newFileName, 'w')
    
    for fileLine in fobjOld:
        for i in range(1, len(oldStrTuple)):
            oldFileLine = fileLine
            fileLine = ReplaceStr(fileLine, oldStrTuple[i], newStrTuple[i])
            if oldFileLine != fileLine:
                break
        fobjNew.write('%s' % fileLine)
 
    fobjOld.close()
    fobjNew.close()
    # 删除原文件
    # os.remove(fileName)

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

    tempFileObj = open(oldStrTupleFile, 'r')
    oldStrTuple = tempFileObj.readline().split(',')
    tempFileObj.close()

    tempFileObj = open(newStrTupleFile, 'r')
    newStrTuple = tempFileObj.readline().split(',')
    tempFileObj.close()

    ReplaceFiles(fileNames, oldStrTuple, newStrTuple)

# if __name__ == '__main__':

directoryName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\R16G16B16A16_FLOAT"
oldStrTupleFile = "C:\\Users\\PitayaLi\\Desktop\\Blending\\oldStr.txt"
newStrTupleFile = "C:\\Users\\PitayaLi\\Desktop\\Blending\\newStr.txt"
logFile = open("info.log",'w')
commentStr = "---------------------------------------------------------------\n"
ReplaceFilesInDir(directoryName, oldStrTupleFile, newStrTupleFile)
logFile.close()
