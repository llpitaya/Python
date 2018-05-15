#!usr/bin/env python

import os
import string
import re
import random
from sys import argv

def genRTWriteMaskBasedOnFormat(scriptName):
    pattern = r'_R\d+G\d+B\d+A\d+'
    if re.search(pattern,scriptName) is not None:
        # 4个channel
        newFileLine = "  RenderTargetWriteMask = 0x%x,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF\n" % random.randint(1,14)
        return newFileLine
    
    pattern = r'_R\d+G\d+B\d+'
    if re.search(pattern,scriptName) is not None:
        # 3个channel
        newFileLine = "  RenderTargetWriteMask = 0x%x,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF\n" % random.randint(1,14)
    
    pattern = r'_R\d+G\d+'
    if re.search(pattern,scriptName) is not None:
        # 4个channel
        newFileLine = "  RenderTargetWriteMask = 0x%x,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF\n" % random.randint(1,3)
        return newFileLine
    
    newFileLine = "  RenderTargetWriteMask = 0x%x,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF\n" % 15                                                                                                
    return newFileLine

def randomRTWriteMask(scriptName,patternStr, newDirName):
    assert os.path.exists(scriptName), "%s does not exist, please check it." % scriptName
    
    relativeFileName = os.path.split(scriptName)[1]
    newFileName = os.path.join(newDirName, relativeFileName)
    
    oldSrciptFile = open(scriptName, 'r')
    newScriptFile = open(newFileName,'w')

    isFindRTWriteMask = False
    newFileLine = ""
    for fileLine in oldSrciptFile:
        if fileLine.find(patternStr) != -1:
            if isFindRTWriteMask == True:
                newScriptFile.write(newFileLine)
                continue
            newFileLine = genRTWriteMaskBasedOnFormat(relativeFileName)
            newScriptFile.write(newFileLine)
            isFindRTWriteMask = True
            continue
        newScriptFile.write(fileLine)

    oldSrciptFile.close()
    newScriptFile.close()

def replaceMultiLinesInFile(scriptName, functionName, patternStr, newDirName):
    assert os.path.exists(scriptName), "%s does not exist, please check it." % scriptName
    assert os.path.exists(functionName), "%s does not exist, please check it." % functionName
    oldSrciptFile = open(scriptName, 'r')
    # 获取文件夹路径和文件名称
    relativeFileName = os.path.split(scriptName)[1]
    newFileName = os.path.join(newDirName, relativeFileName)
    
    newScriptFile = open(newFileName,'w')

    flag = False
    num = 0
    isAdd = False
    for fileLine in oldSrciptFile:
        if isAdd == False and fileLine.find(patternStr)!=-1:
           flag = True
           continue
        if flag == True and isAdd == False and (fileLine.find('{') != -1 or fileLine.find('}') != -1):
            num = num + 1
            continue
        if num == 2 and isAdd == False:
            tempFile = open(functionName, 'r')
            for tempLine in tempFile:
                newScriptFile.write(tempLine)
            tempFile.close()
            isAdd = True
        elif num == 1 and isAdd == False and flag == True:
            pass
        else:
            newScriptFile.write(fileLine)
    newScriptFile.close()

def replaceFilesInDir(directoryName,file1,pattern1,file2,pattern2):
    fileNames = list(os.listdir(directoryName))

    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(directoryName,fileNames[i])
    
    newDirName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\MiddleResults"
    for i in range(len(fileNames)):
        if fileNames[i].find("INT") != -1:
            replaceMultiLinesInFile(fileNames[i],file1[0],pattern1,newDirName)
        else :
            replaceMultiLinesInFile(fileNames[i],file1[1],pattern1,newDirName)
            

    directoryName = newDirName
    newDirName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\FinalResults"
   
    fileNames = list(os.listdir(directoryName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(directoryName,fileNames[i])
    
    for i in range(len(fileNames)):
        if fileNames[i].find("INT") != -1:
            replaceMultiLinesInFile(fileNames[i],file2[0],pattern2,newDirName)
        else :
            replaceMultiLinesInFile(fileNames[i],file2[1],pattern2,newDirName)
    
    directoryName = newDirName
    newDirName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\Results"
    fileNames = list(os.listdir(directoryName))
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(directoryName,fileNames[i])
    
    RTWriteMask = "RenderTargetWriteMask"
    for i in range(len(fileNames)):
        randomRTWriteMask(fileNames[i],RTWriteMask,newDirName)


# if __name__ == '__main__':

logFile = open("info.log",'w')
vertexBufFileName_UINT  = "C:\\Users\\PitayaLi\\Desktop\\Blending\\vertexBuf_UINT.txt"
vertexBufFileName_FLOAT = "C:\\Users\\PitayaLi\\Desktop\\Blending\\vertexBuf_FLOAT.txt"
vertexBufFileName = (vertexBufFileName_UINT,vertexBufFileName_FLOAT)

clearColorFileName_UINT = "C:\\Users\\PitayaLi\\Desktop\\Blending\\clearColor_UINT.txt"
clearColorFileName_SINT = "C:\\Users\\PitayaLi\\Desktop\\Blending\\clearColor_FLOAT.txt"
clearColorFileName = (clearColorFileName_UINT,clearColorFileName_SINT)

vertexBufPattern = ("Load_Buffer \"VertexBuffer\"")
clearColorPattern = ('ClearRenderTargetView')
directoryName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\initial"
replaceFilesInDir(directoryName, vertexBufFileName,vertexBufPattern,clearColorFileName,clearColorPattern)


commentStr = "---------------------------------------------------------------\n"
logFile.close()