#!usr/bin/env python

import os
import string
from sys import argv



def addLinesInFile(scriptName, functionName, patternStr):
    assert os.path.exists(scriptName), "%s does not exist, please check it." % scriptName
    assert os.path.exists(functionName), "%s does not exist, please check it." % functionName
    oldSrciptFile = open(scriptName, 'r')
    # 获取文件夹路径和文件名称
    dirName = os.path.split(scriptName)[0]
    relativeFileName = os.path.split(scriptName)[1]

    dirName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\finalResults"
    newFileName = os.path.join(dirName, relativeFileName)
    
    newScriptFile = open(newFileName,'w')

    flag = False
    isAdd = False
    number = 0
    for fileLine in oldSrciptFile:
        if isAdd == False and fileLine.find(patternStr) != -1:
            flag = True
        if isAdd == False and flag == True and (fileLine.find('{')!=-1 or fileLine.find('}')!=-1):
            number = number + 1

        newScriptFile.write('%s' % fileLine)

        if isAdd == False and number == 2:
            isAdd = True
            tempFile = open(functionName,'r')
            for tempLine in tempFile:
                newScriptFile.write(tempLine)
            tempFile.close()
    newScriptFile.close()


def replaceMultiLinesInFile(scriptName, functionName, patternStr):
    assert os.path.exists(scriptName), "%s does not exist, please check it." % scriptName
    assert os.path.exists(functionName), "%s does not exist, please check it." % functionName
    oldSrciptFile = open(scriptName, 'r')
    # 获取文件夹路径和文件名称
    dirName = os.path.split(scriptName)[0]
    relativeFileName = os.path.split(scriptName)[1]
    dirName  = "C:\\Users\\PitayaLi\\Desktop\\Blending\\results"
    newFileName = os.path.join(dirName, relativeFileName)
    
    newScriptFile = open(newFileName,'w')

    flag = False
    num = 0
    isAdd = False
    for fileLine in oldSrciptFile:
        if isAdd == False and fileLine.find(patternStr[0])!=-1 and fileLine.find(patternStr[1])!=-1:
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

def replaceFilesInDir(directoryName,ASMFile,RegFile):
    fileNames = list(os.listdir(directoryName))
    ASMPattern = ["CreatePixelShader","EU_ASM"]
    RegPattern = "MODEL_EXT_SETREGISTER"
    for i in range(len(fileNames)):
        fileNames[i] = os.path.join(directoryName,fileNames[i])
    
    for i in range(len(fileNames)):
        replaceMultiLinesInFile(fileNames[i],ASMFile,ASMPattern)

    # directoryName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\results"
    # fileNames = list(os.listdir(directoryName))
    # for i in range(len(fileNames)):
    #     fileNames[i] = os.path.join(directoryName,fileNames[i])
    
    # for i in range(len(fileNames)):
    #     addLinesInFile(fileNames[i],RegFile,RegPattern)

# if __name__ == '__main__':

logFile = open("info.log",'w')
ASMFileName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\ASM_SAMPLE_FREQUENCY.txt"
RegFileName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\Reg.txt"
directoryName = "C:\\Users\\PitayaLi\\Desktop\\Blending\\initial"
replaceFilesInDir(directoryName,ASMFileName,RegFileName)
commentStr = "---------------------------------------------------------------\n"
logFile.close()
